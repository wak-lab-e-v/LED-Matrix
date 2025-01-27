library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

-- Ich möchte über einen FPGA in VHDL eine WS2812 steuern. Dazu muss ich bits mit einem Timing ausgeben. 
-- Ich habe 24MHz Takt und muss für ein 0 Bit 0.3µs High (7Takte) und 0.75µs (18Takte) Low ausgeben. 
-- Für eine 1 0.7µs  (17Takte) High und und 0,35µs (8 Takte) Low. anlegen. Und dann pit für bit das eingangsbyte verarbeiten.

entity WS2812_Controller is
    Port (
        clk         : in  STD_LOGIC;  -- 24 MHz Takt
        reset       : in  STD_LOGIC;  -- Reset-Signal
        data_out    : out STD_LOGIC;  -- Ausgang für WS2812
        start       : in  STD_LOGIC;  -- Startsignal für die Übertragung
        done        : out STD_LOGIC;
        rgb_data    : in  STD_LOGIC_VECTOR(15 downto 0)  -- RGB-Daten (8 Bit)
    );
end WS2812_Controller;

architecture Behavioral of WS2812_Controller is
    type state_type is (IDLE, SEND_BIT, SEND_BIT_HIGH_1, SEND_BIT_HIGH_0, SEND_BIT_LOW_1, SEND_BIT_LOW_0);
    signal state       : state_type := IDLE;
    signal bit_index   : integer := 0;
    signal clk_div     : STD_LOGIC_VECTOR(4 downto 0) := (others => '0');  -- 5-Bit Zähler für Taktzyklen
    signal sending     : boolean := false;  -- Flag, um den Sendevorgang zu steuern

    constant zeros : STD_LOGIC_VECTOR(31 downto 0) := (others => '0');  -- Konstante für Nullwerte
begin

    process(clk, reset)
    begin
        if reset = '1' then
            state <= IDLE;
            data_out <= '0';
            bit_index <= 0;
            clk_div <= (others => '0');
            sending <= false;
            done    <= '0';
        elsif rising_edge(clk) then
            case state is
                when IDLE =>
                    if start = '1' then
                        bit_index <= 0;
                        sending <= true;
                        state <= SEND_BIT;
                    end if;
                    done    <= '0';
                    
                when SEND_BIT =>
                    if sending then
                        if bit_index < 16 then
                            if rgb_data(15 - bit_index) = '1' then -- MSB zuerst
                                data_out <= '1';  -- High für '1'
                                clk_div <= (others => '0');  -- Zähler für die High-Zeit zurücksetzen
                                state <= SEND_BIT_HIGH_1;  -- Gehe zum High-Zustand für '1'
                            else
                                data_out <= '1';  -- High für '0'
                                clk_div <= (others => '0');  -- Zähler für die High-Zeit zurücksetzen
                                state <= SEND_BIT_HIGH_0;  -- Gehe zum High-Zustand für '0'
                            end if;
                        else
                            bit_index <= 0;
                            data_out <= '0';  -- Alle Bits gesendet, setze Ausgang auf Low
                            sending <= false;  -- Sendevorgang beenden
                            done    <= '1';
                            state   <= IDLE;  -- Zurück zum IDLE-Zustand
                        end if;
                    end if;

                when SEND_BIT_HIGH_1 =>
                    if clk_div < "10001" then  -- 18 Takte für High (10001 in binär)
                        clk_div <= clk_div + (zeros(clk_div'length - 1 downto 1) & "1");
                    else
                        data_out <= '0';  -- Setze Ausgang auf Low
                        clk_div <= (others => '0');
                        state <= SEND_BIT_LOW_1;  -- Gehe zum Low-Zustand für '1'
                    end if;

                when SEND_BIT_LOW_1 =>
                    if clk_div < "01000" then  -- 8 Takte für Low (01000 in binär)
                        clk_div <= clk_div + (zeros(clk_div'length - 1 downto 1) & "1");
                    else
                        bit_index <= bit_index + 1;  -- Nächstes Bit
                        state <= SEND_BIT;  -- Zurück zum SEND_BIT-Zustand
                    end if;

                when SEND_BIT_HIGH_0 =>
                    if clk_div < "01000" then  -- 8 Takte für High (01111 in binär)
                        clk_div <= clk_div + (zeros(clk_div'length - 1 downto 1) & "1");
                    else
                        data_out <= '0';  -- Setze Ausgang auf Low
                        clk_div <= (others => '0');
                        state <= SEND_BIT_LOW_0;  -- Gehe zum Low-Zustand für '1'
                    end if;

                when SEND_BIT_LOW_0 =>
                    if clk_div < "10010" then  -- 18 Takte für Low (01000 in binär)
                        clk_div <= clk_div + (zeros(clk_div'length - 1 downto 1) & "1");
                    else
                        bit_index <= bit_index + 1;  -- Nächstes Bit
                        state <= SEND_BIT;  -- Zurück zum SEND_BIT-Zustand
                    end if;
                    
                when others =>
                    state    <= IDLE; 
                    done     <= '0';
                    data_out <= '0';  -- Alle Bits gesendet, setze Ausgang auf Low
                    sending <= false;  -- Sendevorgang beenden
             -- Anweisungen für alle anderen Werte
        end case;
      end if;
    end process;
 end Behavioral;
 
 
 
    
    
    