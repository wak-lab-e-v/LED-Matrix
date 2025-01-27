library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

entity Top_Level is
    port (
        i_Clk       : in  std_logic;                     -- Eingangs-Takt
        i_Reset_n   : in  std_logic;                     
        i_RX_Serial : in  std_logic;                     -- Eingangs-Seriell für UART
        o_TX_Serial : out  std_logic;
        i_RX_Start  : in  std_logic;                     -- Startsignal für die WS2812-Übertragung
        o_WS2812    : out std_logic;                     -- Ausgang für WS2812-Daten
        o_OnboardRGB : out std_logic_vector(2 downto 0);   --  110 B, 101 R, 011 G
        o_Done      : out std_logic                      -- Signal, das anzeigt, dass die Übertragung abgeschlossen ist
    );
end Top_Level;

architecture Behavioral of Top_Level is

    -- Signaldeklarationen für die Ports
    signal GCLK       : std_logic;
    
    -- BRAM Ports für UART_RX
    signal bram_clk_b  : std_logic;
    signal bram_oce_b : std_logic;
    signal bram_ce_b  : std_logic;
    signal bram_reset_b : std_logic;
    signal bram_wre_b : std_logic;
    signal bram_ad_b  : std_logic_vector(11 downto 0);
    signal bram_din_b   : std_logic_vector(15 downto 0);
    signal bram_dout_b  : std_logic_vector(15 downto 0);
    
    -- Ports für WS2812_BRAM
    signal ws2812_clk  : std_logic;
    signal ws2812_done  : std_logic;
    
    -- BRAM Ports für WS2812_BRAM
    signal bram_clk_a  : std_logic;
    signal bram_oce_a : std_logic;
    signal bram_ce_a  : std_logic;
    signal bram_reset_a : std_logic;
    signal bram_wre_a : std_logic;
    signal bram_ad_a  : std_logic_vector(11 downto 0);
    signal bram_din_a   : std_logic_vector(15 downto 0);
    signal bram_dout_a  : std_logic_vector(15 downto 0);
   

    -- Komponenten-Deklarationen
    component UART_RX_BRAM
        generic (
            g_CLKS_PER_BIT : integer
        );
        port (
            i_Clk       : in  std_logic;
            i_RX_Serial : in  std_logic;
            o_TX_Serial : out  std_logic;
            i_RX_Start  : in std_logic;
            
            -- BRAM Ports
            clk          : out  std_logic;                     -- Takt für BRAM
            oce          : out  std_logic;                     -- Output Enable für BRAM A
            ce           : out  std_logic;                     -- Chip Enable für BRAM A
            reset        : out  std_logic;                     -- Reset für BRAM A
            wre          : out std_logic;                     -- Write Enable für BRAM A
            ad           : out std_logic_vector(11 downto 0); -- Adresse für BRAM A
            din        : out std_logic_vector(15 downto 0);  -- Dateninput für BRAM A
            dout       : in std_logic_vector(15 downto 0)   -- Datenoutput für BRAM A
            );
    end component;

    component WS2812_BRAM
        port (
            i_Clk       : in  std_logic;                     -- Eingangs-Takt
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
    end component;

    component Gowin_DPB
        Port (
            douta   : out STD_LOGIC_VECTOR(15 downto 0);
            doutb   : out STD_LOGIC_VECTOR(15 downto 0);
            clka    : in  STD_LOGIC;
            ocea    : in  STD_LOGIC;
            cea     : in  STD_LOGIC;
            reseta  : in  STD_LOGIC;
            wrea    : in  STD_LOGIC;
            clkb    : in  STD_LOGIC;
            oceb    : in  STD_LOGIC;
            ceb     : in  STD_LOGIC;
            resetb  : in  STD_LOGIC;
            wreb    : in  STD_LOGIC;
            ada     : in  STD_LOGIC_VECTOR(11 downto 0);
            dina    : in  STD_LOGIC_VECTOR(15 downto 0);
            adb     : in  STD_LOGIC_VECTOR(11 downto 0);
            dinb    : in  STD_LOGIC_VECTOR(15 downto 0)
        );
    end component;
    
    component Gowin_rPLL
    Port (
         clkout : out STD_LOGIC;
         clkin  : in  STD_LOGIC
    );
    end component;

begin
    clock_dll : Gowin_rPLL
    port map (
       clkout => GCLK,
       clkin  => i_Clk
    );

    -- Instanziierung von UART_RX
    uart_rx_inst: UART_RX_BRAM
        generic map (
            g_CLKS_PER_BIT => 6  -- Beispielwert, anpassen je nach Bedarf
        )
        port map (
            i_Clk        => GCLK,
            i_RX_Serial  => i_RX_Serial,
            o_TX_Serial  => o_TX_Serial,
            i_RX_Start   => i_RX_Start,
            
            -- BRAM Ports
            clk        => bram_clk_b,
            oce        => bram_oce_b,
            ce         => bram_ce_b,
            reset      => bram_reset_b,
            wre        => bram_wre_b,
            ad         => bram_ad_b,
            din        => bram_din_b,
            dout       => bram_dout_b
        );

    -- Instanziierung von WS2812_BRAM
    ws2812_bram_inst: WS2812_BRAM
        port map (
            i_Clk       => GCLK,
            o_WS2812    => o_WS2812,  -- Beispiel, hier könnte ein Signal zugewiesen werden
            o_Done      => ws2812_done,
            
            -- BRAM Ports
            clk        => bram_clk_a,
            oce        => bram_oce_a,
            ce         => bram_ce_a,
            reset      => bram_reset_a,
            wre        => bram_wre_a,
            ad         => bram_ad_a,
            din        => bram_din_a,
            dout       => bram_dout_a
        );
        
    RAM : Gowin_DPB
        port map (
            doutb   => bram_dout_b,
            douta   => bram_dout_a,
            clka    => bram_clk_a,
            ocea    => bram_oce_a,
            cea     => bram_ce_a,
            reseta  => bram_reset_a,
            wrea    => bram_wre_a,
            clkb    => bram_clk_b,
            oceb    => bram_oce_b,
            ceb     => bram_ce_b,
            resetb  => bram_reset_b,
            wreb    => bram_wre_b,
            ada     => bram_ad_a,
            dina    => bram_din_a,
            adb     => bram_ad_b,
            dinb    => bram_din_b
        );     

end Behavioral;