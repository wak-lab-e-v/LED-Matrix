// ESP32 Dev Module
// CPU 240MHz
// Partition Scheme:  Huge APP 4MB
#define ETH01
#include <Arduino.h>
#ifdef ETH01
  #include <ETH.h>
  const char* udpAddress = "192.168.1.200"; // Ziel-IP-Adresse
#else
  #include "WiFi.h"
  #include <SPI.h>
  #include <driver/spi_master.h>
  #include <deque>
#endif

#include <WiFiUdp.h>
#include "default.h"

#include "ssid.h"
#ifdef ETH01
  // Feste IP-Konfiguration
  IPAddress local_IP(192, 168, 1, 100); // Setze hier deine feste IP-Adresse
  IPAddress gateway(192, 168, 1, 1);     // Setze hier dein Gateway
  IPAddress subnet(255, 255, 255, 0);    // Setze hier dein Subnetz
#else
  int status = WL_IDLE_STATUS;
#endif
char server[20];
#define MATRIX_WIDTH  56  
#define MATRIX_HEIGHT 32
#define UDP_DELAY  57

#define UDP_PORT 21324
#define SOCKET_PORT 1337

// Input vom Server ist Default 60x33
#define GOPIXEL_WIDTH  60  
#define GOPIXEL_HEIGHT 33
#define ENABLE_GO_SERVER false

WiFiUDP udp;
#ifdef ETH01
  #define UDP_BUFFERSIZE 1000
  #define MAX_PAKET 985
#else
  #define UDP_BUFFERSIZE 2048
  #define WS2812_PWM_ZERO 0xC0 //0b11000000
  #define WS2812_PWM_ONE 0xF8 //0b11111000
#endif

 
#define BITMAP_SIZE    0x3000 
uint8_t udp_buffer[UDP_BUFFERSIZE];



//LED_BUILTIN
#define LED_PIN 13   // MOSI
#define LED_TYPE    WS2812B
#define COLOR_ORDER RGB
static const uint16_t  NUM_LEDS = (MATRIX_WIDTH*MATRIX_HEIGHT); // 1980 // 512
static const uint16_t  LED_TRIBLES = NUM_LEDS*3;
static const uint16_t  GOPIXEL_TRIBLES = GOPIXEL_WIDTH * GOPIXEL_HEIGHT *3;
//static const uint32_t UDP_DELAY = 20; //((59000 / 1980) * NUM_LEDS) / 1000;
#ifdef ETH01
  static const uint32_t BUFFER_SIZE = NUM_LEDS * 3;
  uint8_t* led_grb_buf;
#else
  #define ONBOARD_LED 2
  static const uint32_t BUFFER_SIZE = NUM_LEDS * 24;
  uint8_t* led_stream_buf;
#endif
uint8_t* defaultbild;
uint8_t* bitmapbuffer;
uint16_t bitmappointer;
#ifndef ETH01
  const uint8_t spi_bus = HSPI;
  spi_device_handle_t spi_handle;
  std::deque<spi_transaction_t> transactions;
  int queue_size {1};
#endif

uint32_t Default_offset;
uint32_t myTime, starttime, UDP_Timer, Web_Timer, Web_ReConnect_Timer;
boolean downloadactive;
uint8_t  UDP_Timeout = 20;
boolean Econnected = false;
uint16_t LED_Pointer;
uint32_t width, height;
boolean ledState;
#ifndef ETH01 
  WiFiClient client;
#else
  #define UART1_TX_PIN 17
  #define UART1_RX_PIN 16 // RX-Pin, falls benötigt
  #define SEND_ENABLE  33
#endif  
boolean Connected;

/* Similar to above, but for an 8-bit gamma-correction table.
   Copy & paste this snippet into a Python REPL to regenerate:
import math
gamma=2.6
for x in range(256):
    print("{:3},".format(int(math.pow((x)/255.0,gamma)*255.0+0.5))),
    if x&15 == 15: print
*/
static const uint8_t PROGMEM _GammaTable[256] = {
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  1,  1,  1,  1,  1,
    1,  1,  1,  1,  2,  2,  2,  2,  2,  2,  2,  2,  3,  3,  3,  3,
    3,  3,  4,  4,  4,  4,  5,  5,  5,  5,  5,  6,  6,  6,  6,  7,
    7,  7,  8,  8,  8,  9,  9,  9, 10, 10, 10, 11, 11, 11, 12, 12,
   13, 13, 13, 14, 14, 15, 15, 16, 16, 17, 17, 18, 18, 19, 19, 20,
   20, 21, 21, 22, 22, 23, 24, 24, 25, 25, 26, 27, 27, 28, 29, 29,
   30, 31, 31, 32, 33, 34, 34, 35, 36, 37, 38, 38, 39, 40, 41, 42,
   42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57,
   58, 59, 60, 61, 62, 63, 64, 65, 66, 68, 69, 70, 71, 72, 73, 75,
   76, 77, 78, 80, 81, 82, 84, 85, 86, 88, 89, 90, 92, 93, 94, 96,
   97, 99,100,102,103,105,106,108,109,111,112,114,115,117,119,120,
  122,124,125,127,129,130,132,134,136,137,139,141,143,145,146,148,
  150,152,154,156,158,160,162,164,166,168,170,172,174,176,178,180,
  182,184,186,188,191,193,195,197,199,202,204,206,209,211,213,215,
  218,220,223,225,227,230,232,235,237,240,242,245,247,250,252,255};
  
static uint8_t    gamma8(uint8_t x) {
    return pgm_read_byte(&_GammaTable[x]); // 0-255 in, 0-255 out
  }

#ifdef ETH01
void UART_Output_byte(const uint8_t value, uint8_t* one_byte_buffer)
{
  one_byte_buffer[0] = value;
}
#else
void SPI_Output_octet(const uint8_t value, uint8_t* eight_byte_buffer) {
    //uint16_t offset = value * 8;
    uint8_t mask = 0x80;
    for (int i=0;i<8;i++)
    {
      eight_byte_buffer[i] = (value & mask) ? WS2812_PWM_ONE : WS2812_PWM_ZERO;
      mask = mask >> 1;
    }
}
#endif


void dumpMemory(byte *Array , int Size)
{
    int  index1 = 0, index2 = 0;
    char ch;
    int nEnd = Size / 16;
    
    for (int n = 0; n < nEnd; ++n){
      if (index1 < 4096)
        Serial.print('0');
      if (index1 < 256)
        Serial.print('0');
      if (index1 < 16)
        Serial.print('0');
      Serial.print(index1,HEX); 
      Serial.print(':');
      Serial.print(' ');
        
      for (unsigned char m = 0; m < 16; ++m)
      {
        if (Array[index1] < 16)
          Serial.print('0');
        Serial.print(Array[index1],HEX);
        Serial.print(' ');
        index1++;  
      }
      Serial.print(' ');
      for (unsigned char m = 0; m < 16; ++m)
      {
          ch = (char) Array[index2];
          Serial.print((ch >= ' ' && ch < 127) ? ch : '.');
          index2++;
      }
      Serial.println();
    }
}

#ifndef ETH01
void SetupWebClient(void)
{
  if (client.connect(server, 80)) {
    Serial.println("connected to server");
    // Make a HTTP request:
    client.println("GET /pic/Matrix.bmp HTTP/1.1");
    client.println("<META HTTP-EQUIV=\"CACHE-CONTROL\" CONTENT=\"NO-CACHE\">");
    client.println("Host: www.hildeonline.de");
    client.println("Connection: close");
    client.println();
  }
}
  
void SetupDMA(void)
{
  spi_device_interface_config_t if_cfg {0,0,0,0,0,0,0,0,0,0,0,0,0,0}; // spi_master.h
  spi_host_device_t host {HSPI_HOST}; // spi_types.h
  spi_bus_config_t bus_cfg {-1,-1,-1,-1,-1,0,0,0}; // spi_common.h
                 
  // to use DMA buffer, use these methods to allocate buffer
  led_stream_buf = (uint8_t*)heap_caps_malloc(BUFFER_SIZE, MALLOC_CAP_DMA);
  // Clear Buffer
  memset(led_stream_buf, WS2812_PWM_ZERO, BUFFER_SIZE);
 
  if_cfg.mode = SPI_MODE1;
  //if_cfg.clock_speed_hz = SPI_MASTER_FREQ_8M;  // too fast for bread board...
  if_cfg.clock_speed_hz = 7000000;             // seems Best for 800kHzW S2812
  if_cfg.queue_size = 1;                      // transaction queue size
  if_cfg.flags = SPI_DEVICE_NO_DUMMY;
  if_cfg.pre_cb = NULL;
  if_cfg.post_cb = NULL;
  if_cfg.spics_io_num = (spi_bus == VSPI) ? SS : 15;
  
  bus_cfg.max_transfer_sz = BUFFER_SIZE;
  bus_cfg.sclk_io_num = (spi_bus == VSPI) ? SCK : 14;
  bus_cfg.miso_io_num = (spi_bus == VSPI) ? MISO : 12;
  bus_cfg.mosi_io_num = (spi_bus == VSPI) ? MOSI : 13;
  bus_cfg.quadwp_io_num = -1;
  bus_cfg.quadhd_io_num = -1;
  bus_cfg.flags = 0;
  bus_cfg.intr_flags = 0;
  
  host = (spi_bus == HSPI) ? HSPI_HOST : VSPI_HOST;
  Serial.println("SPI Bus starten");
  Serial.println(host);
  esp_err_t e = spi_bus_initialize(host, &bus_cfg, 2);  // 1 or 2 only
  if (e == ESP_OK) {
    Serial.println("SPI Bus Initialisiert.");
  }
  e = spi_bus_add_device(host, &if_cfg, &spi_handle);
  if (e == ESP_OK) {
    Serial.println("SPI Device Initialisiert.");
  }
}
#endif

#ifndef ETH01
int ScanNetwork()
{
  int result = -1;
  int Wlans = sizeof(WLAN) / sizeof(WLAN[0]);
  int n = WiFi.scanNetworks();
  Serial.println(sizeof(WLAN[0]));
  Serial.println("scan done");
  if (n == 0) {
    Serial.println("no networks found");
  } else {
    Serial.print(n);
    Serial.println(" networks found");
    for (int i = 0; i < n; ++i) {
      // Print SSID and RSSI for each network found
      Serial.print(i + 1);
      Serial.print(": ");
      Serial.print(WiFi.SSID(i));
      for (int j=0;j<Wlans;j++)
        if (!WiFi.SSID(i).compareTo(WLAN[j].ssid) && ((j<result) or (result < 0))) // lieber höchse prio auf obersten Router (result < 0))
          result = j;
      Serial.print(" (");
      Serial.print(WiFi.RSSI(i));
      Serial.print(")");
      Serial.println((WiFi.encryptionType(i) == 3) ? " " : "*");
      delay(10);
    }
  }
  Serial.println("");

  return result;
}
#endif 

#ifdef ETH01
void SetupETH(void)
{
  // Ethernet initialisieren
  //if (!ETH.begin()) {
  //  Serial.println("ETH failed to begin");
  //  return;
  //}

  // Ethernet initialisieren
  ETH.begin();

  // Versuche, eine IP-Adresse über DHCP zu beziehen
  Serial.println("Trying to obtain IP address via DHCP...");
  unsigned long startTime = millis();
  while (millis() - startTime < 10000) { // 10 Sekunden warten
    if ((ETH.localIP() != IPAddress(0, 0, 0, 0))) {
      Serial.println("ETH connected via DHCP");
      Serial.print("IP Address: ");
      Serial.println(ETH.localIP());
      udp.begin(UDP_PORT);
      Serial.println("UDP Begin");
      Econnected = true;
      return; // Erfolgreich verbunden, keine feste IP nötig
    }
    delay(100);
  }

  // Wenn DHCP fehlschlägt, setze die feste IP-Adresse
  Serial.println("DHCP failed, setting static IP...");
  if (!ETH.config(local_IP, gateway, subnet)) {
    Serial.println("ETH config failed");
    return;
  }

  // Warten, bis die Verbindung hergestellt ist
  while (ETH.localIP() == IPAddress(0, 0, 0, 0)) {
    delay(100);
    Serial.println("Waiting for ETH link...");
  }

  Serial.println("ETH connected with static IP");
  Serial.print("IP Address: ");
  Serial.println(ETH.localIP());
  udp.begin(UDP_PORT);
  Serial.println("UDP Begin");
  Econnected = true;
}


void SerialTransfer(const uint8_t* tx_buf, const size_t size)
{
  digitalWrite(SEND_ENABLE, LOW); 
  digitalWrite(SEND_ENABLE, HIGH);
  Serial1.write(tx_buf,size);
}

#else
void SetupWiFi(void)
{  
  WiFi.disconnect(true);
  WiFi.onEvent(WiFiEvent);
  int knownNetwork = ScanNetwork();
  //Initiate connection
  if (knownNetwork >= 0)
  {
    Serial.print("Try to connected to ");
    Serial.println(WLAN[knownNetwork].ssid);
    WiFi.begin(WLAN[knownNetwork].ssid, WLAN[knownNetwork].password);
    Serial.println("");
    myTime = millis();
    UDP_Timer = myTime + 20000;
    Web_Timer = myTime + 20000;
    Web_ReConnect_Timer = myTime + 20000;
    // Wait for connection
    while ((WiFi.status() != WL_CONNECTED) && (myTime < (UDP_Timer + 1000*UDP_Timeout))) {
      delay(500);
      Serial.print(".");
      myTime = millis();
    }
    Serial.println("");
    Serial.print("Connected to ");
    Serial.println(WLAN[knownNetwork].ssid);
    Serial.println(WiFi.localIP());
  }
  else 
  {
    Serial.println("");
    Serial.print("No known Networks in ssid.h ");
  }
  
  if (knownNetwork <= 1)
    strcpy(server, LOCAL_SERVER); 
  else
    strcpy(server, SERVER);
}


void DMATransfer(const uint8_t* tx_buf, const size_t size)
{
    /* ISt eh voll aber rx interessiert nicht */

    if (transactions.size() > 0) {
      transactions.pop_front(); 
    }
    //transactions.pop_front();
    transactions.emplace_back(spi_transaction_t());
    transactions.back().flags = 0;
    // transactions.back().cmd = ;
    // transactions.back().addr = ;
    transactions.back().length = 8 * size;  // in bit size
    // transactions.back().user = ;
    transactions.back().tx_buffer = tx_buf;
    transactions.back().rx_buffer = NULL;

    esp_err_t e = spi_device_queue_trans(spi_handle, &transactions.back(), portMAX_DELAY);
    if (e != ESP_OK) {
      printf("[ERROR] SPI device transmit failed : %d\n", e);
    }
}
#endif

void doDemo()
{
  uint8_t  brigness;
  for (uint16_t i=0;i<NUM_LEDS;i++) 
  {
    //Serial.print(i);
    if (LED_Pointer % 58 == i % 58)
      brigness = 30;
    else 
      brigness = 0;
    #ifdef ETH01
    UART_Output_byte(brigness,led_grb_buf+((i*3+0))); // G
    UART_Output_byte(brigness,led_grb_buf+((i*3+1))); // R
    UART_Output_byte(brigness,led_grb_buf+((i*3+2))); // B
    #else
    SPI_Output_octet(brigness,led_stream_buf+(8*(i*3+0))); // G
    SPI_Output_octet(brigness,led_stream_buf+(8*(i*3+1))); // R
    SPI_Output_octet(brigness,led_stream_buf+(8*(i*3+2))); // B
    #endif
  }
  LED_Pointer++;
  if (LED_Pointer >= NUM_LEDS)
    LED_Pointer = 0;
}



void doDemoPride()
{
  uint8_t  brigness;
  for (uint16_t i=0;i<NUM_LEDS;i++) 
  {
    //Serial.print(i);
    if (LED_Pointer % 58 == i % 58)
      brigness = 30;
    else 
      brigness = 0;
    #ifdef ETH01
    UART_Output_byte(brigness,led_grb_buf+((i*3+0))); // G
    UART_Output_byte(brigness,led_grb_buf+((i*3+1))); // R
    UART_Output_byte(brigness,led_grb_buf+((i*3+2))); // B
    #else
    SPI_Output_octet(brigness,led_stream_buf+(8*(i*3+0))); // G
    SPI_Output_octet(brigness,led_stream_buf+(8*(i*3+1))); // R
    SPI_Output_octet(brigness,led_stream_buf+(8*(i*3+2))); // B
    #endif
  }
  LED_Pointer++;
  if (LED_Pointer >= NUM_LEDS)
    LED_Pointer = 0;
}

uint8_t ASCI2byte(uint8_t *buffer)
{
  uint8_t result;
  if (buffer[0] & 0x40)
    result = 9 + (buffer[0] & 0xF);
  else  
    result =     (buffer[0] & 0xF);
    
  if (buffer[1] & 0x40)
    return (result << 4) + 9 + (buffer[1] & 0xF);
  else  
    return (result << 4) +     (buffer[1] & 0xF);
}



void doChaosBinary(uint8_t *buffer, const size_t size, uint32_t width, uint32_t height)
{
  uint16_t matrixsize = GOPIXEL_WIDTH*GOPIXEL_HEIGHT; 
  uint16_t i,j,idx;
  uint8_t brigness_r,brigness_g,brigness_b;
  uint8_t  segment;
  uint8_t  x,y,x2;
  x = 0;
  y = 0; 
  for (i=0;i<matrixsize;i++)
  {
    
    if ((x < width) and (y < height))
    {
      j = 3*i;
      brigness_r = gamma8(buffer[j]);
      brigness_g = gamma8(buffer[j+1]);
      brigness_b = gamma8(buffer[j+2]);  
      segment = int(x / 8);
      
      if (y % 2 == 0)
        x2 = x;
      else
         x2 = 7-x;
      
      #ifdef ETH01
      idx = 3 * (255+(segment*256)-(x2%8)-(y*8));
      if (brigness_g > 60) brigness_g = 60;
      if (brigness_r > 60) brigness_r = 60;
      if (brigness_b > 60) brigness_b = 60;
      
      if (idx <= (BUFFER_SIZE-3))
      {
              
        UART_Output_byte(brigness_g,led_grb_buf+((idx))); // G
        UART_Output_byte(brigness_r,led_grb_buf+((idx+1))); // R
        UART_Output_byte(brigness_b,led_grb_buf+((idx+2))); // B
      }
      
      #else  
      idx = 24 * (255+(segment*256)-(x2%8)-(y*8));
      if (brigness_g > 60) brigness_g = 60;
      if (brigness_r > 60) brigness_r = 60;
      if (brigness_b > 60) brigness_b = 60;
      
      if (idx <= (BUFFER_SIZE-24))
      {
        SPI_Output_octet(brigness_g,led_stream_buf+(idx));
        SPI_Output_octet(brigness_r,led_stream_buf+(idx+8));
        SPI_Output_octet(brigness_b,led_stream_buf+(idx+16));
      }
      #endif
    } 
    
    
    x += 1;
    if (x >= GOPIXEL_WIDTH) 
    {
      x = 0;
      y += 1;
    }
       
  }
}
  
void doBinary(uint8_t *buffer, const size_t size, uint32_t width, uint32_t height)
{
  uint16_t matrixsize = width*height;
  uint8_t brigness_r,brigness_g,brigness_b;
  uint16_t i = 0,j, index, Pixelnr, Lineend= 0;
  if (3*matrixsize < size)
  for (i=0;i<matrixsize;i++)
  {
    j = 3*i;
    brigness_r = gamma8(buffer[j]);
    brigness_g = gamma8(buffer[j+1]);
    brigness_b = gamma8(buffer[j+2]);
    Pixelnr = i;
    #ifdef ETH01
    if ((int(Pixelnr / width) & 1)) // ungerade
    {
      if (Lineend == 0)
      {
        Lineend = Pixelnr+width;
      }
      Lineend--;  
      index = Lineend * 3;  
    }
    else
    {
      index = 3*Pixelnr;
      Lineend = 0;
    }
    
    if (brigness_g > 60) brigness_g = 60;
    if (brigness_r > 60) brigness_r = 60;
    if (brigness_b > 60) brigness_b = 60;
    
    if (index <= (BUFFER_SIZE-3))
    {
      UART_Output_byte(brigness_g,led_grb_buf+(index));
      UART_Output_byte(brigness_g,led_grb_buf+(index+1));
      UART_Output_byte(brigness_g,led_grb_buf+(index+2));
    }

    
    #else
    if ((int(Pixelnr / width) & 1)) // ungerade
    {
      if (Lineend == 0)
      {
        Lineend = Pixelnr+width;
      }
      Lineend--;  
      index = Lineend * 24;  
    }
    else
    {
      index = 24*Pixelnr;
      Lineend = 0;
    }
    
    if (brigness_g > 60) brigness_g = 60;
    if (brigness_r > 60) brigness_r = 60;
    if (brigness_b > 60) brigness_b = 60;
    
    if (index <= (BUFFER_SIZE-24))
    {
      SPI_Output_octet(brigness_g,led_stream_buf+(index));
      SPI_Output_octet(brigness_r,led_stream_buf+(index+8));
      SPI_Output_octet(brigness_b,led_stream_buf+(index+16));
    }
    #endif
  } 
}
void doDefaultFrames() // Start Bilder
{
  
  for (int i = 0; i< (LED_TRIBLES); i++)
    defaultbild[i+4] = myGraphic[i+Default_offset];
  doNeo(defaultbild, 4+LED_TRIBLES);
  Default_offset += LED_TRIBLES;
  if (Default_offset >= sizeof(myGraphic))
    Default_offset = 0;
}

void doNeo(uint8_t *buffer, const size_t size)
{
  if (buffer[0] == 4)
  {
    int16_t offest = ((buffer[3] + (buffer[2]  << 8)) * 3)-4;
    uint8_t  brigness;
    int8_t   RGB_correct=1;
    for (uint16_t i=4;i<size;i++)
    {
      brigness = buffer[i+RGB_correct];
      if (!RGB_correct)
        RGB_correct = 1;
      else if (RGB_correct == 1)
        RGB_correct = -1;
      else RGB_correct = 0;
                  
      if (brigness > 0x3f) //  Heiligkeit immer noch auf 63 begrenzen 2,6A Ruhe + (0,362 * 63 * 2000)
        brigness = 0x3f;
      #ifdef ETH01
      UART_Output_byte(brigness,led_grb_buf+(offest+i));
      #else
      SPI_Output_octet(brigness,led_stream_buf+(8*(offest+i)));
      #endif
    }
  }
  else   
  {
    int16_t offest = ((buffer[3] + (buffer[2]  << 8)) * 3)-6;
    uint16_t code, j;
    uint8_t   r,g,b;
    for (uint16_t i=4;i<size;i++)
    {
      
      if (!(i % 2))
      {
        code = (buffer[i+1] + (buffer[i]  << 8));
        r = (code >> 10) & 0x3e;
        g = (code >> 5)  & 0x3f;
        b = (code << 1)  & 0x3f;

        j = i / 2; 
        #ifdef ETH01
        UART_Output_byte(g,led_grb_buf+(offest+j*3+0));
        UART_Output_byte(r,led_grb_buf+(offest+j*3+1));
        UART_Output_byte(b,led_grb_buf+(offest+j*3+2));
        #else
        SPI_Output_octet(g,led_stream_buf+(8*(offest+j*3+0))); // G
        SPI_Output_octet(r,led_stream_buf+(8*(offest+j*3+1))); // R
        SPI_Output_octet(b,led_stream_buf+(8*(offest+j*3+2))); // B
        #endif
      }
    }
  }   
}

uint16_t SearchBitmapHeader(byte *Array , int Size, uint32_t *width,  uint32_t *height)
{
  for (int i = 0;i<Size;i++)
  {
     if ((Array[i] == 0x0D) && (Array[i+1] == 0x0A) && (Array[i+2] == 0x0D) && (Array[i+3] == 0x0A) && (Array[i+4] == 0x42) && (Array[i+5] == 0x4D))
     {
       int offset = i+4;
       *width  = (uint32_t) Array[offset+18];
       *height = (uint32_t) Array[offset+22];
       return offset;
     }  
  }
}
void setup() {
  // put your setup code here, to run once:
  
  #ifndef ETH01
  pinMode(ONBOARD_LED, OUTPUT);
  client.setTimeout(100); // Connection
  #endif
  Serial.begin(115200);
  
  #ifdef ETH01
    pinMode(SEND_ENABLE, OUTPUT);
    // Highspeed UART1 konfigurieren
    Serial1.begin(4000000, SERIAL_8N1, UART1_RX_PIN, UART1_TX_PIN);
    led_grb_buf = (uint8_t*)heap_caps_malloc(BUFFER_SIZE, MALLOC_CAP_8BIT); // Reserviere im SRAM
    memset(led_grb_buf, 0, BUFFER_SIZE);
    SetupETH();
  #else  
    SetupDMA();
    SetupWiFi();
  #endif  
  
  myTime = millis();
  UDP_Timer = myTime + 20000;
  Web_Timer = myTime + 20000;
  Web_ReConnect_Timer = myTime + 20000;
  starttime = myTime;
  
  LED_Pointer = 0;
  Connected = false;
  downloadactive = false;
  Serial.println("Allocate bitmapbuffer");
  bitmapbuffer =  (uint8_t*)heap_caps_malloc(BITMAP_SIZE, MALLOC_CAP_8BIT);
  bitmappointer = 0;
  Serial.println("Allocate defaultbild");
  defaultbild =  (uint8_t*)heap_caps_malloc(4+LED_TRIBLES, MALLOC_CAP_8BIT);
  defaultbild[0] = 4;
  defaultbild[1] = 1;
  defaultbild[2] = 0;
  defaultbild[3] = 0;
  Default_offset = 0;
  
}

void loop(){
  uint16_t buffersize;

  myTime = millis();
  udp.parsePacket();
  if((buffersize = udp.read(udp_buffer, UDP_BUFFERSIZE)) > 0){
    //Serial.println("GotUDP"); // Vorsicht nicht zu viele
    doNeo(udp_buffer, buffersize);
    UDP_Timer   = myTime;
    UDP_Timeout = udp_buffer[1];
  }

  #ifndef ETH01  
  if (myTime > (UDP_Timer + 1000*UDP_Timeout))
  {
    if (ENABLE_GO_SERVER)
    {

      if (!Connected && (myTime > Web_ReConnect_Timer + 12000))
      {
        Serial.println("connected to server");
        Serial.print(WiFi.localIP());
        Serial.print(" -> ");
        Serial.println(server);
        if (client.connect(server, SOCKET_PORT)) {
          client.println("GM");
          Serial.println("GM");
          Connected = true;
          downloadactive = true;
          bitmappointer = 0;
          Web_Timer   = myTime;
        }
        Web_ReConnect_Timer = myTime;
      }
      
      
      while (Connected && downloadactive && client.available() && (millis() < Web_Timer + 10000)) {
        //char c = client.read();
        if (bitmappointer < BITMAP_SIZE)
        {
          bitmapbuffer[bitmappointer++] = client.read();
        } 
      }

      if (bitmappointer > GOPIXEL_TRIBLES)   
      {
        while (client.available()) 
          client.read();
        downloadactive = false;
      }
      
      if (Connected and (myTime > Web_Timer + 10000))
      {
        downloadactive = false;
        Serial.println("disconnecting from server.");
        client.stop();
        Connected = false;
      }
      
        // if the server's disconnected, stop the client:
      if (Connected && (!downloadactive || !client.connected())) {
        if ((bitmappointer >= GOPIXEL_TRIBLES) && (bitmappointer < GOPIXEL_TRIBLES+6))
        {
          if (MATRIX_WIDTH == 56)
            doChaosBinary(bitmapbuffer, BITMAP_SIZE, MATRIX_WIDTH, MATRIX_HEIGHT);
          else
            doBinary(bitmapbuffer, BITMAP_SIZE, MATRIX_WIDTH, MATRIX_HEIGHT);
        }
        Connected = client.connected();
        if (Connected)
        {
          client.println("GM");
          Serial.println("GM pushed");
          Serial.println(bitmappointer);
          downloadactive = true;
          bitmappointer = 0;
          Web_Timer   = myTime;
        }
      }
    }
  }
  #endif



  
  if (myTime >= (starttime + UDP_DELAY)) // 17 fps
  { 
//    Serial.print(myTime);
//    Serial.print(" ");
//    Serial.print(UDP_Timer);
//    Serial.print(" ");
//    Serial.print(Web_ReConnect_Timer);
//    Serial.print(" ");
//    Serial.println(Web_Timer);
       
    
    if ((myTime > (UDP_Timer + 1000*UDP_Timeout)) && (myTime > Web_Timer + 20000)) //  && (myTime >= (starttime + 59))) // 
    {
      doDefaultFrames();
      //Serial.println("doDefaultFrames");
    }
    starttime = myTime;
    //Serial.println("DMA");
    #ifdef ETH01
      SerialTransfer(led_grb_buf, BUFFER_SIZE);
    #else
      DMATransfer(led_stream_buf, BUFFER_SIZE);
    #endif
    if (ledState == LOW) {
      ledState = HIGH;
    } else {
      ledState = LOW;
    }
    #ifndef ETH01
    digitalWrite(ONBOARD_LED, ledState);
    #endif
    // set the LED with the ledState of the variable:
    
  }
}

#ifndef ETH01  
//wifi event handler
void WiFiEvent(WiFiEvent_t event){
    switch(event) {
      case SYSTEM_EVENT_STA_GOT_IP:
          //When connected set 
          Serial.print("WiFi connected! IP address: ");
          Serial.println(WiFi.localIP());  
          //initializes the UDP state
          udp.begin(WiFi.localIP(),UDP_PORT);
          Econnected = true;
          break;
      case SYSTEM_EVENT_STA_DISCONNECTED:
          Serial.println("WiFi lost connection");
          Econnected = false;
          break;
    }
}
#endif
