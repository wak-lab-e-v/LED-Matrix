library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

entity WS2812_BRAM is
    generic (
        g_LED_Count : std_logic_vector(12 downto 0) := "1010100000000" -- 3*0x0700
    );
    port (
        i_Clk       : in  std_logic;                     -- Eingangs-Takt
        
        -- WS2812 Ports
        o_WS2812    : out std_logic;                     -- Ausgang für WS2812-Daten
        o_Done      : out std_logic;                     -- Signal, das anzeigt, dass die Übertragung abgeschlossen ist
        
        -- BRAM Ports
        clk        : out  std_logic;                     -- Takt für BRAM
        oce        : out  std_logic;                     -- Output Enable für BRAM A
        ce         : out  std_logic;                     -- Chip Enable für BRAM A
        reset      : out  std_logic;                     -- Reset für BRAM A
        wre        : out std_logic;                     -- Write Enable für BRAM A
        ad         : out std_logic_vector(11 downto 0); -- Adresse für BRAM A
        din        : out std_logic_vector(15 downto 0);  -- Dateninput für BRAM A
        dout       : in std_logic_vector(15 downto 0)   -- Datenoutput für BRAM A
    );
end WS2812_BRAM;

architecture Behavioral of WS2812_BRAM is

    signal ws_data : std_logic_vector(15 downto 0); -- Daten für WS2812
    signal ws_Low  : std_logic_vector(7 downto 0);
    signal ws_Hi   : std_logic_vector(7 downto 0);
    signal address : std_logic_vector(11 downto 0) := (others => '0'); -- Adresse für BRAM
    signal led_count : std_logic_vector(13 downto 0) := (others => '0');  -- Zähler für die Anzahl der LEDs
    signal start_ws : std_logic := '0'; -- Startsignal für WS2812
    signal read_enable : std_logic := '1'; -- Leseaktivierung für BRAM
    signal douta_reg : std_logic_vector(15 downto 0); -- Register für BRAM-Daten
    signal Delay  : std_logic_vector(11 downto 0) := (others => '0'); 
    signal Next_Byte : std_logic;
    signal Start  : std_logic;

    constant zeros : STD_LOGIC_VECTOR(31 downto 0) := (others => '0');  -- Konstante für Nullwerte

    component WS2812_Controller
       Port (
        clk         : in  STD_LOGIC;  -- 24 MHz Takt
        reset       : in  STD_LOGIC;  -- Reset-Signal
        data_out    : out STD_LOGIC;  -- Ausgang für WS2812
        start       : in  STD_LOGIC;  -- Startsignal für die Übertragung
        done        : out STD_LOGIC;
        rgb_data    : in  STD_LOGIC_VECTOR(15 downto 0)  -- RGB-Daten (8 Bit)
        );
    end component;

begin
    o_Done <= Next_Byte; 
    -- Instanziierung des WS2812-Controllers
    ws2812_instance: WS2812_Controller
        port map (
            clk         => i_Clk,
            reset       => '0',
            rgb_data    => ws_data, -- Daten für WS2812
            data_out    => o_WS2812,
            start       => start_ws, -- Startsignal für WS2812
            done        => Next_Byte
        );

    clk        <= i_Clk;
    oce        <= '1';
    ce         <= '1';
    reset      <= '0';
    wre        <= '0'; -- Schreibaktivierung deaktiviert (nur lesen)
    ad         <= address; -- Adresse für BRAM
    din        <= (others => '0'); -- Dateninput (nicht verwendet beim Lesen)
    douta_reg  <= dout; -- Datenoutput von BRAM
 

  -- Logik zum Lesen von Daten aus dem BRAM und Senden an den WS2812-Controller
  process(i_Clk)
  begin
    if rising_edge(i_Clk) then
        if Start = '1' then 
            if led_count < g_LED_Count then -- Angenommen, wir haben 256 LEDs
                ws_data <= douta_reg(7 downto 0) & douta_reg(15 downto 8); -- douta_reg; -- Lade die RGB-Daten aus dem BRAM
                start_ws <= '1'; -- Starte die Übertragung an den WS2812
                address <= led_count(12 downto 1); -- Erhöhe die Adresse
                if Next_Byte = '1' then
                  led_count <= led_count + (zeros(led_count'length - 1 downto 2) & "10");  -- Erhöhe den LED-Zähler
                end if;
            else
                start_ws <= '0'; -- Stoppe die Übertragung, wenn alle LEDs gesendet wurden
                Start    <= '0';
            end if;
            Delay    <= X"000"; -- 60µs
        else
            start_ws  <= '0'; -- Stoppe die Übertragung, wenn kein Startsignal gegeben wird
            led_count <= zeros(led_count'length - 1 downto 0);
            address   <= zeros(address'length - 1 downto 0); 
            if Delay < X"8A0" then
              Delay <= Delay + X"001";
            else
              Start <= '1';
            end if;
              
        end if;
    end if;
  end process;
end Behavioral;            