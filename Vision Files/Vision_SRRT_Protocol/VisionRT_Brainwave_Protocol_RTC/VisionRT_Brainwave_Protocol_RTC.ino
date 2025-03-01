#include <Wire.h>
#include <RTClib.h>
#include <FastLED.h>

#define LED_PIN     8

#define BUTTON_PIN_LEFT  5     // Left button
#define BUTTON_PIN_MID   4     // Middle button
#define BUTTON_PIN_RIGHT 6     // Right button

// Assign color codes
#define COLOR_WHITE CRGB::White
#define COLOR_GREEN CRGB::Green
#define COLOR_BLUE  CRGB::Blue
#define COLOR_RED   CRGB::Red

// LED strip
#define NUM_LEDS    150
#define CHIPSET     WS2811
#define COLOR_ORDER GRB
CRGB leds[NUM_LEDS];

#define BRIGHTNESS  128

int PTRIAL_MAX = 25;
int TRIAL_MAX = 100 + PTRIAL_MAX;
int ledIndex = 66;  // Index of the LED to be used on the strip
CRGB color;

int trialVariable = 1; // Simple Reflex Visual
int motorState1 = LOW;
int motorState2 = LOW;
int motorState3 = LOW;

// Button variables
int buttonPin3 = 6;
int buttonState3 = LOW;
int buttonPin1 = 5;
int buttonState1 = LOW;
int buttonPin2 = 4;
int buttonState2 = LOW;

// Data Variables
int StimType;
int Guess;
bool Correct;
int numCorrect = 0;

// Object
RTC_DS3231 rtc; 
long randDelay;
DateTime startTime;
DateTime currentTime;
unsigned long startMicros;
unsigned long ObjShowTime;
unsigned long ReactionTime;

// Function to return a random color
CRGB getRandomColor() {
  int colorChoice = random(trialVariable);
  if (colorChoice == 0){ return COLOR_WHITE;}
  if (colorChoice == 1){ return COLOR_GREEN;}
  else return COLOR_BLUE;
}

// The setup function runs once when you press reset or power the board
void setup() {
  delay(3000);  // Power-up safety delay

  Wire.begin();  // Initialize I2C communication
  Serial.begin(9600);  // Intialize serial communication
 
  // Setup RTC
  if (!rtc.begin()){
    Serial.println("Couldn't find RTC");
    while (1);  // Halt program
  } 

  // Set the RTC with current time if it lost power
  if (rtc.lostPower()){
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  }
  
  do {
      currentTime = rtc.now();
  } while (currentTime.second() == rtc.now().second());
  startTime = rtc.now();
  startMicros = micros();
  Serial.print(startTime.unixtime());
  Serial.print(".000,");
  Serial.println(startMicros);
  
  // Setup for LED and button 
  FastLED.addLeds<CHIPSET, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection(TypicalSMD5050);
  FastLED.setBrightness(BRIGHTNESS);

  // Initialize LEDs to be off
  for (int i = 0; i < NUM_LEDS; i++) {
    leds[i] = CRGB::Black;
  }
  FastLED.show();

  // Initialize button pins as input
  pinMode(buttonPin1, INPUT);
  pinMode(buttonPin2, INPUT);
  pinMode(buttonPin3, INPUT);

  // Flash the LED 3 times before the start
  for (int i = 0; i <= 2; i++) {
    leds[ledIndex] = CRGB::Red;
    FastLED.show();
    delay(250);
    leds[ledIndex] = CRGB::Black;
    FastLED.show();
    delay(250);
  }

  delay(2000);

  // Print the header for the results
  Serial.println("ObjShowTime,ReactionTime,StimType,Guess,Correct");
  randomSeed(analogRead(A0)); 
}

// Wait for a random period between 0.5 and 1.5 seconds
void loop() {
  
  buttonState1 = digitalRead(buttonPin1);
  buttonState2 = digitalRead(buttonPin2);
  buttonState3 = digitalRead(buttonPin3);
  if (numCorrect < PTRIAL_MAX) {  
    if (motorState1 == LOW && buttonState1 == 0 && motorState2 == LOW && buttonState2 == 0 && motorState3 == LOW && buttonState3 == 0) {
      color = getRandomColor();
      leds[ledIndex] = color;
      FastLED.show();
      if (color == COLOR_WHITE) {      
        motorState1 = HIGH;
        motorState2 = LOW;
        motorState3 = LOW;
        StimType = 1;
      }
      else if (color == COLOR_GREEN) {  
        motorState1 = LOW;
        motorState2 = HIGH;
        motorState3 = LOW;
        StimType = 2;
      }
      else {
        motorState1 = LOW;
        motorState2 = LOW;
        motorState3 = HIGH;
        StimType = 3;
      }
    }

    if (buttonState1 == HIGH || buttonState2 == HIGH || buttonState3 == HIGH) {
      if (buttonState1 == HIGH) {
        Guess = 1;
        digitalWrite(buttonPin1, 0);
        buttonState1 = LOW;
      }
      else if (buttonState2 == HIGH) {
        Guess = 2;
        digitalWrite(buttonPin2, 0);
        buttonState2 = LOW;
      }
      else {
        Guess = 3;
        digitalWrite(buttonPin3, 0);
        buttonState3 = LOW;
      }
      if (StimType == Guess) {
        Correct = true;
        leds[ledIndex] = CRGB::Black;
        FastLED.show();
        delay(150);
        leds[ledIndex] = COLOR_GREEN;
        FastLED.show();
        delay(150);
        leds[ledIndex] = CRGB::Black;
        FastLED.show();
        delay(150);
        numCorrect++;
      }
      else {
        Correct = false;
        leds[ledIndex] = CRGB::Black;
        FastLED.show();
        delay(150);
        leds[ledIndex] = COLOR_RED;
        FastLED.show();
        delay(150);
        leds[ledIndex] = CRGB::Black;
        FastLED.show();
        delay(150);
      }
      leds[ledIndex] = CRGB::Black;
      FastLED.show();
      if (motorState1 == HIGH) {
        motorState1 = LOW;
      }
      else if (motorState2 == HIGH)
      {
        motorState2 = LOW;
      }
      else
      {
        motorState3 = LOW;
      }
      randDelay = random(500, 1500);
      delay(randDelay);
    }
    // Check if trial limit reached, flash LEDs to signal end of experiment
    if (numCorrect == PTRIAL_MAX) {
      for (int i = 0; i < 3; i++) {
        leds[ledIndex] = CRGB::Red;
        FastLED.show();
        delay(250);
        leds[ledIndex] = CRGB::Black;
        FastLED.show();
        delay(250);
      }
      delay(2000);
    }
  }
  else {
    if (motorState1 == LOW && buttonState1 == 0 && motorState2 == LOW && buttonState2 == 0 && motorState3 == LOW && buttonState3 == 0) {
      color = getRandomColor();
      leds[ledIndex] = color;
      FastLED.show();
      if (color == COLOR_WHITE) {      
        motorState1 = HIGH;
        motorState2 = LOW;
        motorState3 = LOW;
        StimType = 1;
      }
      else if (color == COLOR_GREEN) {  
        motorState1 = LOW;
        motorState2 = HIGH;
        motorState3 = LOW;
        StimType = 2;
      }
      else {
        motorState1 = LOW;
        motorState2 = LOW;
        motorState3 = HIGH;
        StimType = 3;
      }
      ObjShowTime = micros();
    }

    if (buttonState1 == HIGH || buttonState2 == HIGH || buttonState3 == HIGH) {
      ReactionTime = micros();
      if (buttonState1 == HIGH) {
        Guess = 1;
        digitalWrite(buttonPin1, 0);
        buttonState1 = LOW;
      }
      else if (buttonState2 == HIGH) {
        Guess = 2;
        digitalWrite(buttonPin2, 0);
        buttonState2 = LOW;
      }
      else {
        Guess = 3;
        digitalWrite(buttonPin3, 0);
        buttonState3 = LOW;
      }
      if (StimType == Guess) {
        Correct = true;
        numCorrect++;
      }
      else {
        Correct = false;
      }
      Serial.print(ObjShowTime);
      Serial.print(",");
      Serial.print(ReactionTime);
      Serial.print(",");
      Serial.print(StimType);
      Serial.print(",");
      Serial.print(Guess);
      Serial.print(",");
      Serial.println(Correct);
      leds[ledIndex] = CRGB::Black;
      FastLED.show();
      if (motorState1 == HIGH) {
        motorState1 = LOW;
      }
      else if (motorState2 == HIGH)
      {
        motorState2 = LOW;
      }
      else
      {
        motorState3 = LOW;
      }
      randDelay = random(500, 1500);
      delay(randDelay);
    }
    // Check if trial limit reached, flash LEDs to signal end of experiment
    if (numCorrect == TRIAL_MAX) {
      for (int i = 0; i < 3; i++) {
        leds[ledIndex] = CRGB::Red;
        FastLED.show();
        delay(250);
        leds[ledIndex] = CRGB::Black;
        FastLED.show();
        delay(250);
      }
      // End the program
      exit(0);
    }
  }
}
