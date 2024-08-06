#include <FastLED.h>

#define LED_PIN     8

// Red = Power; White = Ground; Green = Data

// Information about the LED strip itself
#define NUM_LEDS    150
#define CHIPSET     WS2811
#define COLOR_ORDER GRB
CRGB leds[NUM_LEDS];

#define BRIGHTNESS  90

int eccentricities[] = {-15,0,15}; //angles corresponding to LED stimulus
int eccIndices[] = {46,66,85}; //LED strip index for each eccentricity
int motorPick;
int ledNum;


// Reaction time experiment of one LED. 
// LED will flash 3 times before the start of the experiment.
int trialMax = 150;  // 150 = Complex, 150 = Simple
int numCorrect= 0;
int numMotors = 3;  // 3 = Complex, 1 = Simple
int trialNum = 0;

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
long ObjShowTime;
long ReactionTime;

// The setup function runs once when you press reset or power the board
void setup() {

  delay( 3000 ); // power-up safety delay
  // It's important to set the color correction for your LED strip here,
  // so that colors can be more accurately rendeRed through the 'temperature' profiles
  FastLED.addLeds<CHIPSET, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection( TypicalSMD5050 );
  FastLED.setBrightness( BRIGHTNESS );

  for (int i = 0; i < NUM_LEDS; i++) {
    leds[i] = CRGB::Black;
    FastLED.show();
  }

  // Initialize button pins as input.
  pinMode(buttonPin1, INPUT);
  pinMode(buttonPin2, INPUT);
  pinMode(buttonPin3, INPUT);

  // Intialize serial communication.
  Serial.begin(9600);

  for (int i = 0; i <= 2; i++) {
    leds[eccIndices[0]] = CRGB::White;
    FastLED.show();
    leds[eccIndices[1]] = CRGB::White;
    FastLED.show();
    leds[eccIndices[2]] = CRGB::White;
    FastLED.show();
    delay(250);
    leds[eccIndices[0]] = CRGB::Black;
    FastLED.show();
    leds[eccIndices[1]] = CRGB::Black;
    FastLED.show();
    leds[eccIndices[2]] = CRGB::Black;
    FastLED.show();
    delay(250);
  }
  Serial.println("ObjShowTime, ReactionTime, StimType, Guess, Correct");
  randomSeed(analogRead(A0)); 
  randDelay = random(3000, 6000);
  delay(randDelay);
}

/*delay(1000); //duration that light is on
      leds[eccIndices[anglePick]] = CRGB::Black;
      FastLED.show();
    
    // Turn the LED on and record time, trial has begun.
    if (motorPick == 0) {      
      ledNum = eccentricities[motorPick];
      leds[eccIndices[motorPick]] = CRGB::White;
      FastLED.show();
      oldT = millis();
      motorState1 = HIGH;
      motorState2 = LOW;
      motorState3 = LOW;
    }
    else if (motorPick == 1) {
      ledNum = eccentricities[motorPick];
      leds[eccIndices[motorPick]] = CRGB::White;
      FastLED.show();   
      motorState1 = LOW;
      motorState2 = HIGH;
      motorState3 = LOW;
    }
    else {
      ledNum = eccentricities[motorPick];
      leds[eccIndices[motorPick]] = CRGB::White;
      FastLED.show();
      motorState1 = LOW;
      motorState2 = LOW;
      motorState3 = HIGH;
    }
  } */
// the loop function runs over and over again forever
void loop() {

  //Always check to see if button is being pressed.
  buttonState1 = digitalRead(buttonPin1);
  buttonState2 = digitalRead(buttonPin2);
  buttonState3 = digitalRead(buttonPin3);

  // Critera for trial start.
  if (motorState1 == LOW && buttonState1 == LOW && motorState2 == LOW && buttonState2 == LOW && motorState3 == LOW && buttonState3 == LOW) {

    // Pick a random RGB color.
    motorPick = random(0, numMotors);
    ledNum = eccentricities[motorPick];
    leds[eccIndices[motorPick]] = CRGB::White;
    FastLED.show();
    // Turn the LED on and record time, trial has begun.
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
    ObjShowTime = millis();
  }

  // Criteria for trial end.
  if (buttonState1 == HIGH || buttonState2 == HIGH || buttonState3 == HIGH) {
    ReactionTime = millis();
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
    Serial.print(ObjShowTime);
    Serial.print(",");
    Serial.print(ReactionTime);
    Serial.print(",");
    Serial.print(StimType);
    Serial.print(",");
    Serial.print(Guess);
    Serial.print(",");
    Serial.println(Correct);
    leds[eccIndices[motorPick]] = CRGB::Black;
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
  if (numCorrect == trialMax) {
    for (int i = 0; i <= 2; i++) {
      leds[eccIndices[0]] = CRGB::White;
      FastLED.show();
      leds[eccIndices[1]] = CRGB::White;
      FastLED.show();
      leds[eccIndices[2]] = CRGB::White;
      FastLED.show();
      delay(250);
      leds[eccIndices[0]] = CRGB::Black;
      FastLED.show();
      leds[eccIndices[1]] = CRGB::Black;
      FastLED.show();
      leds[eccIndices[2]] = CRGB::Black;
      FastLED.show();
      delay(250);
    }
    exit(0);
  }
}
