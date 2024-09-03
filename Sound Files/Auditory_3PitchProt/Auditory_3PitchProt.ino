#include <Wire.h>
#include <RTClib.h>


int TRIAL_MAX = 100;

int trialVariable = 3; // 3 Pitch
int motorPin1 = 11;
int motorPin2 = 12;
int motorState1 = LOW;
int motorState2 = LOW;
int motorState3 = LOW;
int motorPick;
int toneVar[3] = {262, 660, 1568};

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
int numCorrect;

// Object
RTC_DS3231 rtc; 
int trialNum = 0;
long randDelay;
DateTime startTime;
DateTime currentTime;
unsigned long startMicros;
unsigned long ObjShowTime;
unsigned long ReactionTime;

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
    Serial.println("RTC lost power, let's set the time!");
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

  // Initialize button pins as input
  pinMode(buttonPin1, INPUT);
  pinMode(buttonPin2, INPUT);
  pinMode(buttonPin3, INPUT);
  pinMode(motorPin1, OUTPUT);

  // Flash the LED 3 times before the start
  for (int i = 0; i <= 2; i++) {
    tone(motorPin1, 262, 250);
    delay(250);
    tone(motorPin1, 660, 250);
    delay(250);
    tone(motorPin1, 1568, 250);
    delay(250);
  }

  // Print the header for the results
  Serial.println("trialNum,ObjShowTime,ReactionTime,StimType,Guess,Correct");
  randomSeed(analogRead(A0)); 
  delay(3000);
}

// Wait for a random period between 1 and 2.5 seconds
void loop() {
  
  buttonState1 = digitalRead(buttonPin1);
  buttonState2 = digitalRead(buttonPin2);
  buttonState3 = digitalRead(buttonPin3);
  if (motorState1 == LOW && buttonState1 == 0 && motorState2 == LOW && buttonState2 == 0 && motorState3 == LOW && buttonState3 == 0) {
    motorPick = random(trialVariable);
    tone(motorPin1, toneVar[motorPick]);
    if (motorPick == 0) {      
      motorState1 = HIGH;
      motorState2 = LOW;
      motorState3 = LOW;
      StimType = 1;
    }
    else if (motorPick == 1) {  
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
    trialNum++;
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
    Serial.print(trialNum);
    Serial.print(",");
    Serial.print(ObjShowTime);
    Serial.print(",");
    Serial.print(ReactionTime);
    Serial.print(",");
    Serial.print(StimType);
    Serial.print(",");
    Serial.print(Guess);
    Serial.print(",");
    Serial.println(Correct);
    noTone(motorPin1);
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
      tone(motorPin1, 262, 250);
      delay(250);
      tone(motorPin1, 330, 250);
      delay(250);
      tone(motorPin1, 392, 250);
      delay(250);
    }
    // End the program
    exit(0);
  }
}
