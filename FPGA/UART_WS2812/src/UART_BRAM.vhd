library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

entity UART_RX_BRAM is
    generic (
        g_CLKS_PER_BIT : integer
    );
    port (
        i_Clk       : in  std_logic;                     -- Eingangs-Takt
        i_RX_Serial : in  std_logic;                     -- Eingangs-Seriell
        o_TX_Serial : out  std_logic;
        i_RX_Start  : in std_logic;                       -- Signal, das anzeigt, dass ein Byte empfangen wurde
        
       
        -- BRAM Ports
        clk          : out  std_logic;                     -- Takt für BRAM
        oce          : out  std_logic;                     -- Output Enable für BRAM A
        ce           : out  std_logic;                     -- Chip Enable für BRAM A
        reset        : out  std_logic;                     -- Reset für BRAM A
        wre          : out std_logic;                     -- Write Enable für BRAM A
        ad           : out std_logic_vector(11 downto 0); -- Adresse für BRAM A
        din          : out std_logic_vector(15 downto 0);  -- Dateninput für BRAM A
        dout         : in std_logic_vector(15 downto 0)    -- Datenoutput für BRAM A
    );
end UART_RX_BRAM;

architecture Behavioral of UART_RX_BRAM is

    signal rx_byte : std_logic_vector(7 downto 0);
    signal ram_word  : std_logic_vector(15 downto 0);
    signal RX_DV : std_logic := '0';
    signal byte_count : std_logic_vector(12 downto 0) := (others => '0'); -- Zähler für die Anzahl der geschriebenen Bytes
 
     constant zeros : STD_LOGIC_VECTOR(32 downto 0) := (others => '0');  -- Konstante für Nullwerte
   
    component UART_RX
        generic (
            g_CLKS_PER_BIT : integer
        );
        port (
            i_Clk       : in  std_logic;
            i_RX_Serial : in  std_logic;
            o_TX_Serial : out  std_logic;
            o_RX_DV     : out std_logic;
            o_RX_Byte   : out std_logic_vector(7 downto 0)
        );
    end component;
    

begin
    clk <= i_Clk;
    din <= ram_word; 
    oce <= '1';
    ce <= '1';
    reset <= '0';
    -- Instanziierung des UART-Empfängers
    uart_receiver: UART_RX
        generic map (
            g_CLKS_PER_BIT => g_CLKS_PER_BIT
        )
        port map (
            i_Clk       => i_Clk,
            i_RX_Serial => i_RX_Serial,
            o_TX_Serial => o_TX_Serial,
            o_RX_DV     => RX_DV,
            o_RX_Byte   => rx_byte
        );

    -- Logik zum Schreiben in den BRAM
    process(i_Clk, i_RX_Start)
    begin
        if (i_RX_Start = '0') then
           byte_count <= (others => '0');
        elsif rising_edge(i_Clk) then
            if RX_DV = '1' then
                wre <= '1';
                ad <= byte_count(12 downto 1);
                if (byte_count(0)) = '0' then
                  if rx_byte > X"80"  then
                    ram_word(7 downto 0) <=  X"80";
                  else
                    ram_word(7 downto 0) <= rx_byte; -- Daten für BRAM
                  end if;
                else 
                  if rx_byte > X"80"  then
                    ram_word(15 downto 8) <=  X"80";
                  else
                    ram_word(15 downto 8) <= rx_byte; -- Daten für BRAM
                  end if;
                end if;
                byte_count <= byte_count + (zeros(byte_count'length - 1 downto 1) & "1"); -- Zähler erhöhen
            else
                wre <= '0';
            end if;
        end if;
    end process;


end Behavioral;