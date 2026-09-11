#include <mcp_can.h>
#include <SPI.h>

#define ENC_A 2
#define ENC_B 3
// #define CAN_CS 10

volatile int counter = 0;
int lastCounter = 0;

const float wheelRadius = 0.28; // In metres
const int pulsesPerRevolution = 600;
const unsigned long interval = 100; // Every 300ms we calculate the speed

unsigned long elapsed_time = 0;

// MCP_CAN CAN(CAN_CS);

void read_encoder();

void setup() { 
pinMode(ENC_A, INPUT_PULLUP); 
pinMode(ENC_B, INPUT_PULLUP); 

attachInterrupt(digitalPinToInterrupt(ENC_A), read_encoder, CHANGE); 
attachInterrupt(digitalPinToInterrupt(ENC_B), read_encoder, CHANGE); 

Serial.begin(9600);

// while (CAN_OK != CAN.begin(CAN_500KBPS)) {
// Serial.println("CAN init failed, retrying...");
// delay(100);
// }
// Serial.println("CAN init success");
 }

void loop() { 
unsigned long current_time = millis(); 
if (current_time - elapsed_time >= interval) { 
int delta = counter - lastCounter; 
lastCounter = counter; 
elapsed_time = current_time; 

float revolutions = (float)delta / pulsesPerRevolution; 
float displacement = 2 * PI * wheelRadius * revolutions; 
float speed = displacement / 0.1; // سرعة = مسافة ÷ الزمن

Serial.print("Speed: "); 
Serial.print(speed); 
Serial.println("m/s"); 

byte data[4]; 
memcpy(data, &speed, 4); 
// CAN.sendMsgBuf(0x100, 0, 4, data); 
 }
}

// ============ Encoder ISR ============
unsigned long _lastIncReadTime = micros();
unsigned long _lastDecReadTime = micros();
int _pauseLength = 25000;
int _fastIncrement = 1;

void read_encoder() { 
static uint8_t old_AB = 3; 
static int8_t encval = 0; 
static const int8_t enc_states[] = {0,-1,1,0,1,0,0,-1,-1,0,0,1,0,1,-1,0}; 

old_AB <<= 2; 

if (digitalRead(ENC_B)) old_AB |= 0x02; 
if (digitalRead(ENC_A)) old_AB |= 0x01; 

encval += enc_states[old_AB & 0x0f]; 

if (encval > 3) { 
int change = 1; 
if ((micros() - _lastIncReadTime) < _pauseLength) 
change *= _fastIncrement; 
_lastIncReadTime = micros(); 
counter += change; 
encval = 0; 
} 
else if (encval < -3) { 
int change = -1; 
if ((micros() - _lastDecReadTime) < _pauseLength) 
change *= _fastIncrement; 
_lastDecReadTime = micros(); 
counter += change; 
encval = 0; 
 }
}
