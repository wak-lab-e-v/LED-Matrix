#include <ETH.h>
#include <WiFiUdp.h>
// https://dl.espressif.com/dl/package_esp32_index.json

#define UART1_TX_PIN 17
#define UART1_RX_PIN 16 // RX-Pin, falls benötigt
#define SEND_ENABLE  33
#define LED_COUNT (56*32*3)
#define MAX_PAKET 985
WiFiUDP udp;
#define UDP_BUFFERSIZE 2048 
char udp_buffer[UDP_BUFFERSIZE];

const int localPort = 21324; // Port, auf dem UDP-Pakete empfangen werden
int Current_LED; 
unsigned long previousMillis = 0; // Speichert die letzte Zeit

void setup() {

  pinMode(SEND_ENABLE, OUTPUT);
  Serial.begin(115200);
  
  // UART1 konfigurieren
  Serial1.begin(4000000, SERIAL_8N1, UART1_RX_PIN, UART1_TX_PIN);

  // Ethernet initialisieren
  ETH.begin();
  
  // Warten, bis eine IP-Adresse zugewiesen wurde
  while (ETH.localIP() == IPAddress(0, 0, 0, 0)) {
    delay(100);
    Serial.print(".");
  }
  
  Serial.print("IP-Adresse: ");
  Serial.println(ETH.localIP());

  // UDP starten
  udp.begin(localPort);
  Serial.println("Ethernet und UDP bereit.");
}

void loop() {
  // Überprüfen, ob UDP-Pakete empfangen wurden
  unsigned long currentMillis = millis(); // Aktuelle Zeit in Millisekunden
  int packetSize = udp.parsePacket();
  if (packetSize) {

    int len = udp.read(udp_buffer, UDP_BUFFERSIZE);
    if (len > 0) {
      //udp_buffer[len] = 0; // Null-Terminierung
      Serial.printf("Empfangen: %i\n", len);
      
      // Sende das empfangene Paket über UART1
      if ((Current_LED == 0) || ((previousMillis + 50) < currentMillis))
      {
        digitalWrite(SEND_ENABLE, LOW);
        Current_LED = 0;
        digitalWrite(SEND_ENABLE, HIGH); 
      }
      previousMillis = currentMillis;
      Serial1.write(udp_buffer,len);
      Current_LED += len;
      if (Current_LED >= LED_COUNT)
      {
        digitalWrite(SEND_ENABLE, LOW);
        Current_LED = 0;
      }  
    }
  }
  
  // Hier kannst du weitere Logik hinzufügen, falls nötig
}
