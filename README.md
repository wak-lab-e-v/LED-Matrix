# LED-Matrix
repro for some scripts, tools and stuff around our LED-Matrix

## ESP32
Server/Client for ESP32


## media
Some scripts look for media files here. Clone the repro and add your personel content here.
A couple of images are included.

## doc
Maybe TLTR




## Python UDP
Python Scripts for UDP communication between PC -> ESP32 
### Play Gif, jpg, png, mp4
selet a Directory to play ones by ones
call PlayDir('./')


### Duplicate Desktop
You need *pyautogui* for screenshot Desktop
call Desktop()

## Simulation
Some Python scripts to simulate the LED Matrix on your system. 

## Python Pixelserver
Python scripts for our matrixserver


## Installation

```
pip3 install -r requirements.txt
```

Edit the file `MatrixHost.ini` with your [gopixelflut](https://github.com/wak-lab-e-v/gopixelflut) Server ip address, or the [ESP32](ESP32/) matrix udp server ip.
