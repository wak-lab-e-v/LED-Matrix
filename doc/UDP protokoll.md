
Drive WS2812 with ESP32, DMA and UDP


## Uses the WLED UDP Realtime Control 
### Protokoll 4 DNRGB
Byte 0 = 4

Byte 1 = Don't care

Byte 2 = Start index high byte

Byte 3 = Start index low byte

Byte 4 + n*3 	Red Value

Byte 5 + n*3 	Green Value

Byte 6 + n*3 	Blue Value

..
..
..

### Protokoll 5 DN16B
Color16:
5 Bit Rot 
6 Bit Grün
5 Bit Blue 

Color16 = (Red & 0x1f) << 11 + (Green & 0x3f) << 5 + (Blue & 0x1f)

Byte 0 = 5

Byte 1 = Don't care

Byte 2 = Start index high byte

Byte 3 = Start index low byte

Byte 4 + n*2 	Color16 High

Byte 5 + n*2 	Color16 Low

..
..
..