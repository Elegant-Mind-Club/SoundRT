#include <FastLED.h>

#define LED_PIN     8
#define BUTTON_PIN  5  // use the middle button

// Information about the LED strip itself
#define NUM_LEDS    150
#define CHIPSET     WS2811
#define COLOR_ORDER GRB
CRGB leds[NUM_LEDS];

#define BRIGHTNESS  90
#define TRIAL_MAX   10 

int ledIndex = 66;  // Index of the LED to be used on the strip

// Reaction time experiment of one LED. 
// LED will flash 3 times before the start of the experiment.
int numCorrect= 0;
int trialNum = 0;

// Time variables
long randDelay;
long ObjShowTime;
long ReactionTime;

// The setup function runs once when you press reset or power the board
void setup() {
  delay( 3000 ); // power-up safety delay
  // It's important to set the color correction for your LED strip here,
  // so that colors can be more accurately rendeRed through the 'temperature' profiles
  FastLED.addLeds<CHIPSET, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection( TypicalSMD5050 );
  FastLED.setBrightness( BRIGHTNESS );

// Initialize LEDs to be off
  for (int i = 0; i < NUM_LEDS; i++) {
    leds[i] = CRGB::Black;
  }
  FastLED.show();

  // Initialize button pins as input.
  pinMode(BUTTON_PIN, INPUT);

  // Intialize serial communication.
  Serial.begin(9600);

  // Flash the LED 3 times before the start
  for (int i = 0; i <= 2; i++) {
    leds[ledIndex] = CRGB::White;
    FastLED.show();
    delay(250);
    leds[ledIndex] = CRGB::Black;
    FastLED.show();
    delay(250);
  }

  // Print the header for the results
  Serial.println("trialNum, ObjShowTime, ReactionTime");
  randomSeed(analogRead(A0)); 
}

// Wait for a random period between 1 and 2.5 seconds
void loop() {
   randDelay = random(1000, 2500);
   delay(randDelay);

   leds[ledIndex] = CRGB::Red;
   FastLED.show();
   ObjShowTime = millis();

   while(digitalRead(BUTTON_PIN) == LOW) {
     // Wait for the button to be pressed
   }

   ReactionTime = millis() - ObjShowTime;
   trialNum++;

   leds[ledIndex] = CRGB::Black;
   FastLED.show();

   Serial.print(trialNum);
   Serial.print(",");
   Serial.print(ObjShowTime);
   Serial.print(",");
   Serial.print(ReactionTime);
   Serial.println();
   
   randDelay = random(500, 1500);
   delay(randDelay);
  
  if (trialNum == TRIAL_MAX) {
    for (int i = 0; i < 3; i++) {
      leds[ledIndex] = CRGB::White;
      FastLED.show();
      delay(250);
      leds[ledIndex] = CRGB::Black;
      FastLED.show();
      delay(2000);
    }
    // End the program
    exit(0);
  }
}
