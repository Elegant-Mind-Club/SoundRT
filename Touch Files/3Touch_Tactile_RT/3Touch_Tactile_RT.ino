#include <Wire.h>
#include <RTClib.h>

int PTRIAL_MAX = 25;
int trialMax = 100 + PTRIAL_MAX;
int numCorrect = 0;
int numMotors = 3;  // 3 INPUT RT TEST

// LED variables
int motorPick;
int motorPin1 = 13;
int motorPin3 = 2;
int motorPin2 = 3;

// LED power states
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

// Time variables
long randDelay;
long StimType;
long Guess;
bool Correct;

// Object
RTC_DS3231 rtc; 
DateTime startTime;
DateTime currentTime;
unsigned long startMicros;
unsigned long ObjShowTime;
unsigned long ReactionTime;

// The setup function runs once when you press reset or power the board
void setup() {
  // initialize analog pins as an output.
  delay(3000);
  pinMode(motorPin1, OUTPUT);
  pinMode(motorPin2, OUTPUT);
  pinMode(motorPin3, OUTPUT);

  // Initialize button pins as input.
  pinMode(buttonPin1, INPUT);
  pinMode(buttonPin2, INPUT);
  pinMode(buttonPin3, INPUT);

  // Intialize serial communication.

  Wire.begin();  // Initialize I2C communication
  Serial.begin(9600);  // Intialize serial communication

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

  for (int i = 0; i <= 2; i++) {
    digitalWrite(motorPin1, HIGH);
    digitalWrite(motorPin2, HIGH);
    digitalWrite(motorPin3, HIGH);
    delay(250);
    digitalWrite(motorPin1, LOW);
    digitalWrite(motorPin2, LOW);
    digitalWrite(motorPin3, LOW);
    delay(250);
  }

  Serial.println("ObjShowTime,ReactionTime,StimType,Guess,Correct");
  randomSeed(analogRead(A0)); 
  delay(random(3000, 6000));
}

// the loop function runs over and over again forever
void loop() {

  //Always check to see if button is being pressed.
  buttonState1 = digitalRead(buttonPin1);
  buttonState2 = digitalRead(buttonPin2);
  buttonState3 = digitalRead(buttonPin3);
  if (numCorrect < PTRIAL_MAX) {
    if (motorState1 == LOW && buttonState1 == LOW && motorState2 == LOW && buttonState2 == LOW && motorState3 == LOW && buttonState3 == LOW) {

      // Pick a random RGB color.
      motorPick = random(0, numMotors);
      // Turn the LED on and record time, trial has begun.
      if (motorPick == 0) {
        digitalWrite(motorPin1, HIGH);
        motorState1 = HIGH;
        motorState2 = LOW;
        motorState3 = LOW;
        StimType = 1;
      } 
      else if (motorPick == 1) {
        digitalWrite(motorPin2, HIGH);
        motorState1 = LOW;
        motorState2 = HIGH;
        motorState3 = LOW;
        StimType = 2;
      } 
      else {
        digitalWrite(motorPin3, HIGH);
        motorState1 = LOW;
        motorState2 = LOW;
        motorState3 = HIGH;
        StimType = 3;
      }
      ObjShowTime = micros();
    }

    // Criteria for trial end.
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
      if (motorState1 == HIGH) {
        digitalWrite(motorPin1, 0);
        motorState1 = LOW;
      }
      else if (motorState2 == HIGH)
      {
        digitalWrite(motorPin2, 0);
        motorState2 = LOW;
      }
      else
      {
        digitalWrite(motorPin3, 0);
        motorState3 = LOW;
      }
      randDelay = random(500, 1500);
      delay(randDelay);
    }
    if (numCorrect == PTRIAL_MAX) {
      for (int i = 0; i <= 2; i++) {
        digitalWrite(motorPin1, HIGH);
        digitalWrite(motorPin2, HIGH);
        digitalWrite(motorPin3, HIGH);
        delay(250);
        digitalWrite(motorPin1, LOW);
        digitalWrite(motorPin2, LOW);
        digitalWrite(motorPin3, LOW);
        delay(250);
      }
      delay(random(3000,6000));
    }
  }
  else {
    if (motorState1 == LOW && buttonState1 == LOW && motorState2 == LOW && buttonState2 == LOW && motorState3 == LOW && buttonState3 == LOW) {
      // Pick a random RGB color.
      motorPick = random(0, numMotors);
      // Turn the LED on and record time, trial has begun.
      if (motorPick == 0) {
        digitalWrite(motorPin1, HIGH);
        motorState1 = HIGH;
        motorState2 = LOW;
        motorState3 = LOW;
        StimType = 1;
      } 
      else if (motorPick == 1) {
        digitalWrite(motorPin2, HIGH);
        motorState1 = LOW;
        motorState2 = HIGH;
        motorState3 = LOW;
        StimType = 2;
      } 
      else {
        digitalWrite(motorPin3, HIGH);
        motorState1 = LOW;
        motorState2 = LOW;
        motorState3 = HIGH;
        StimType = 3;
      }
      ObjShowTime = micros();
    }
      // Criteria for trial end.
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
      if (motorState1 == HIGH) {
        digitalWrite(motorPin1, 0);
        motorState1 = LOW;
      }
      else if (motorState2 == HIGH)
      {
        digitalWrite(motorPin2, 0);
        motorState2 = LOW;
      }
      else
      {
        digitalWrite(motorPin3, 0);
        motorState3 = LOW;
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
      randDelay = random(500, 1500);
      delay(randDelay);
    }
    if (numCorrect == trialMax) {
        for (int i = 0; i <= 2; i++) {
          digitalWrite(motorPin1, HIGH);
          digitalWrite(motorPin2, HIGH);
          digitalWrite(motorPin3, HIGH);
          delay(250);
          digitalWrite(motorPin1, LOW);
          digitalWrite(motorPin2, LOW);
          digitalWrite(motorPin3, LOW);
          delay(250);
        }
        exit(0);
    }
  
  }
}
