// Nano CTRL for Pon Controller
// released under the GPLv3 license 
// 
// Boarverwalter Arduino Nano installieren
// Arduino Nano mit mindesten 8MHz laufen lassen
// ARDUINO NANO
//                        _____  
//                   +---|     |---+
//  13  PB5 SCK  D13 |O  |     |  O| D12 MISO   PB4 12
//              3,3V |O  |_____|  O| D11 MOSI  ~PB3 11
//               REF |O           O| D10  SS   ~PB2 10
//  14  PC0       A0 |O   /    \  O| D9        ~PB1  9
//  15  PC1       A1 |O  /ATmega\ O| D8         PB0  8
//  16  PC2       A2 |O  \ 328P / O| D7         PD7  7
//  17  PC3       A3 |O   \    /  O| D6        ~PD6  6
//  18  PC4 SDA   A4 |O           O| D5        ~PD5  5
//  19  PC5 SCL   A5 |O    IOI    O| D4         PD4  4
//      ADC6      A6 |O   Reset   O| D3  INT1  ~PD3  3
//      ADC7      A7 |O           O| D2  INT0   PD2  2  -  433 Out
//                5V |O           O| GND
//      PC6      RST |O  5V  GND  O| RST        PC6  
//               GND |O   O O O   O| D1   RX    PD0  0
//               VIN |O  1O O O   O| D0   TX    PD1  1
//                   +-------------+
//
//
#include <SoftwareSerial.h>
#include "CRC16.h"
#include "CRC.h"

CRC16 crc;

#define PIN_CLK1            3
#define PIN_CW1             4
#define PIN_BT1             5

#define PIN_CLK2            6
#define PIN_CW2             7
#define PIN_BT2             8



SoftwareSerial mySerial(1,2,1);  //rx, tx, inverse_logic
byte EnableSender;
byte Encoder2, Encoder1;
byte Encoder2_old, Encoder1_old;
byte Repeat = 0;
byte Buffer[5];
int countdown;

unsigned int calcCRC8(unsigned char crc, unsigned char c, unsigned char mask);
int DoEncoder(byte Number, byte CW_PIN, byte CLK_PIN);

void setup() {
  pinMode(PIN_CLK1, INPUT);
  pinMode(PIN_CW1, INPUT);
  pinMode(PIN_BT1, INPUT);
  pinMode(PIN_CLK2, INPUT);
  pinMode(PIN_CW2, INPUT);
  pinMode(PIN_BT2, INPUT);
  
  pinMode(0,INPUT);
  //setup_watchdog(3); //64ms
  delay(1000);
  mySerial.begin(4800);
  Serial.begin(38400);
  Serial.println("Send X to this Nano to activate the protocoll");
  Serial.println("PACKET: 0xAD  ENC1   ENC2   CRC16");
  EnableSender = false;
  Repeat = 3;
  countdown = 2000;
  crc16(Buffer, 3, 0x1021, 0, 0, false, false);
}


void loop() {

  if (Serial.available() > 0)
  {
    char incomingByte = Serial.read();
    Serial.println((char)incomingByte, DEC);
    if (incomingByte == char('X'))
    {
      EnableSender = false; 
      Serial.println("Sender daktiviert");
    }    
  }

//   Serial.print(digitalRead(PIN_CLK1));
//   Serial.print(" ");
//      Serial.print(digitalRead(PIN_CW1));
//   Serial.print(" ");
//      Serial.print(digitalRead(PIN_BT1));
//   Serial.print(" ");
//      Serial.print(digitalRead(PIN_CLK2));
//   Serial.print(" ");
//      Serial.print(digitalRead(PIN_CW2));
//   Serial.print(" ");
//      Serial.println(digitalRead(PIN_BT2));
  
  Encoder1 = ((DoEncoder(0, PIN_CW1, PIN_CLK1) >> 1) & 0xFE) + !digitalRead(PIN_BT1);
  Encoder2 = ((DoEncoder(1, PIN_CW2, PIN_CLK2) >> 1) & 0xFE) + !digitalRead(PIN_BT2);
  
  byte CRC8 = 0;
  Buffer[0] = 0xAD;
  Buffer[1] = Encoder1;
  Buffer[2] = Encoder2;
  crc.reset();
  crc.setPolynome(0x1021);
  crc.add(Buffer, 3);
  *(uint16_t *) &Buffer[3] = crc.getCRC();
  
  if (countdown-- <= 0)
  {
    countdown = 200;
    // Encoder1 += 1;
    if (EnableSender)
    {
      if (Repeat)
        mySerial.write(&Buffer[0], 5);
    }
    else
    {
      if (Repeat)
        Serial.write(&Buffer[0], 5);
      //Serial.print(*(uint8_t *) &Buffer[0], HEX);     Serial.print(" ");
      //Serial.print(*(uint8_t *) &Buffer[1], HEX);     Serial.print(" ");
      //Serial.print(*(uint8_t *) &Buffer[2], HEX);     Serial.print(" ");
      //Serial.println(*(uint16_t *) &Buffer[3], HEX);
    }  
  
    if ((Encoder1_old == Encoder1) && (Encoder2_old == Encoder2))
    {
      if (Repeat)
         Repeat--;
    }
    else
    {
      Repeat = 1;
      //countdown = 1;
    }  
    Encoder1_old = Encoder1;
    Encoder2_old = Encoder2;
  }

    

     
  //Serial.println(CRC8);
  //Serial.write(Buffer, 3);
  //system_sleep();
  //delay(delayval); // Delay for a period of time (in milliseconds).
  //delay(150);
}


//----------------------------------

int DoEncoder(byte Number, byte CW_PIN, byte CLK_PIN)
{
  uint8_t CW  = digitalRead(CW_PIN);
  uint8_t CLK = digitalRead(CLK_PIN);
    
  static uint8_t Last_CW[3];
  static uint8_t Last_CLK[3];
  static int Position[3];
 

  if ((CW == Last_CLK[Number]) && (CLK != Last_CW[Number]))
    Position[Number] += 1;
  else if ((CW != Last_CLK[Number]) && (CLK == Last_CW[Number]))
    Position[Number] -= 1;

  Last_CW[Number] = CW;
  Last_CLK[Number] = CLK;
  return Position[Number];
 
}


unsigned int calcCRC8(unsigned char crc, unsigned char c, unsigned char mask)
{
  // MSB first
  unsigned char i;
  for(i=0;i<8;i++)
  {
    if((crc ^ c) & 0x80) { crc=(crc<<1)^mask; }
    else crc<<=1;
    c<<=1;
  }
  return (crc);
}


//void crcInit(void)
//{
//    unsigned short  remainder;
//    int    dividend;
//    unsigned char  bit;
//
//    for (dividend = 0; dividend < 256; ++dividend)
//    {
//        remainder = dividend << 4;
//
//        for (bit = 8; bit > 0; --bit)
//        {
//            if (remainder & 0x800)
//            {
//                remainder = (remainder << 1) ^ 0x180D; //Polynomio of CRC-12
//            }
//            else
//            {
//                remainder = (remainder << 1);
//            }
//        }
//       crcTable[dividend] = remainder;
//    }
//
//}


//unsigned short crcFast(unsigned char const message[], int nBytes)
//{
//    unsigned short remainder = 0x0000;
//    unsigned char  data;
//    int  byte;
//
//    /*
//     * Divide the message by the polynomial, a byte at a time.
//     */
//    for (byte = 0; byte < nBytes; ++byte)
//    {
//        data = message[byte] ^ (remainder >> 4);
//    remainder = crcTable[data] ^ (remainder << 8);
//    }
//
//    /*
//     * The final remainder is the CRC.
//     */
//    return (remainder ^ 0);
//
//}
