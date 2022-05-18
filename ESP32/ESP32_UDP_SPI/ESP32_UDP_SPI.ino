// ESP32 Dev Module
#include <Arduino.h>
#include "WiFi.h"
#include <WiFiUdp.h>
#include <SPI.h>
#include <driver/spi_master.h>
#include <deque>

#include "ssid.h"

#define UDP_PORT 21324

WiFiUDP udp;
#define UDP_BUFFERSIZE 2048 
uint8_t udp_buffer[UDP_BUFFERSIZE];

#define WS2812_PWM_ZERO 0xC0 //0b11000000
#define WS2812_PWM_ONE 0xF8 //0b11111000
#define ONBOARD_LED 2
//LED_BUILTIN
#define LED_PIN 13   // MOSI
#define LED_TYPE    WS2812B
#define COLOR_ORDER RGB
#define NUM_LEDS 1800 // 512

static const uint32_t BUFFER_SIZE = NUM_LEDS * 24;
uint8_t* led_stream_buf;
const uint8_t spi_bus = HSPI;
spi_device_handle_t spi_handle;
std::deque<spi_transaction_t> transactions;
int queue_size {1};

uint32_t myTime, starttime, UDP_Timer;
uint8_t  UDP_Timeout = 20;
boolean connected = false;
uint16_t LED_Pointer;

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
  
void SPI_Output_octet(const uint8_t value, uint8_t* eight_byte_buffer) {
    //uint16_t offset = value * 8;
    uint8_t mask = 0x80;
    for (int i=0;i<8;i++)
    {
      eight_byte_buffer[i] = (value & mask) ? WS2812_PWM_ONE : WS2812_PWM_ZERO;
      mask = mask >> 1;
      //eight_byte_buffer[i] = pgm_read_byte(&_BitTable[offset++]); 
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
        if (!WiFi.SSID(i).compareTo(WLAN[j].ssid) && (result < 0))
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
    UDP_Timer = myTime;
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
    SPI_Output_octet(brigness,led_stream_buf+(8*(i*3+0))); // G
    SPI_Output_octet(brigness,led_stream_buf+(8*(i*3+1))); // R
    SPI_Output_octet(brigness,led_stream_buf+(8*(i*3+2))); // B
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
    SPI_Output_octet(brigness,led_stream_buf+(8*(i*3+0))); // G
    SPI_Output_octet(brigness,led_stream_buf+(8*(i*3+1))); // R
    SPI_Output_octet(brigness,led_stream_buf+(8*(i*3+2))); // B
  }
  LED_Pointer++;
  if (LED_Pointer >= NUM_LEDS)
    LED_Pointer = 0;
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
                  
      if (brigness > 40) 
        brigness = 40;
      SPI_Output_octet(brigness,led_stream_buf+(8*(offest+i)));
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
        r = (code >> 11) & 0x1f;
        g = (code >> 5)  & 0x3f;
        b = code  & 0x1f;
//        Serial.print(i);
//        Serial.print(" ");
//        Serial.print(buffer[i] );
//        Serial.print(" ");
//        Serial.print(buffer[i+1]);
//        Serial.print(" ");
//        Serial.print(r );
//        Serial.print(" ");
//        Serial.print(g );
//        Serial.print(" ");
//        Serial.print(b);
//        Serial.print(" ");
//        Serial.println(code);

        j = i / 2; 
        SPI_Output_octet(g,led_stream_buf+(8*(offest+j*3+0))); // G
        SPI_Output_octet(r,led_stream_buf+(8*(offest+j*3+1))); // R
        SPI_Output_octet(b,led_stream_buf+(8*(offest+j*3+2))); // B
      }
    }
  }   
}

void setup() {
  // put your setup code here, to run once:
  pinMode(ONBOARD_LED, OUTPUT);
  
  Serial.begin(115200);
  SetupDMA();

  SetupWiFi();
  starttime = myTime;
  LED_Pointer = 0;
}

void loop(){
  uint16_t buffersize;
  myTime = millis();
  udp.parsePacket();
  if((buffersize = udp.read(udp_buffer, UDP_BUFFERSIZE)) > 0){
    doNeo(udp_buffer, buffersize);
    UDP_Timer   = myTime;
    UDP_Timeout = udp_buffer[1];
  }
  if ((myTime > (UDP_Timer + 1000*UDP_Timeout)) && (myTime >= (starttime + 59)))
    doDemo();
  
  if (myTime >= (starttime + 59)) // 17 fps
  { 
    starttime = myTime;
    //Serial.println("DMA");
    DMATransfer(led_stream_buf, BUFFER_SIZE);
  }
}

//wifi event handler
void WiFiEvent(WiFiEvent_t event){
    switch(event) {
      case SYSTEM_EVENT_STA_GOT_IP:
          //When connected set 
          Serial.print("WiFi connected! IP address: ");
          Serial.println(WiFi.localIP());  
          //initializes the UDP state
          udp.begin(WiFi.localIP(),UDP_PORT);
          connected = true;
          break;
      case SYSTEM_EVENT_STA_DISCONNECTED:
          Serial.println("WiFi lost connection");
          connected = false;
          break;
    }
}
