#include <FastLED.h>

#define LED_PIN     8
#define NUM_LEDS    150
#define CHIPSET     WS2811
#define COLOR_ORDER GRB
#define BRIGHTNESS  128
#define LED_INDEX   66  // Just one LED to blink

CRGB leds[NUM_LEDS];

void setup() {
  // Start serial communication
  Serial.begin(9600);
  while (!Serial); // Wait for Serial Monitor (especially useful on Leonardo, etc.)
  Serial.println("Arduino is connected and setup is complete.");

  // Initialize LED strip
  FastLED.addLeds<CHIPSET, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS);
  FastLED.setBrightness(BRIGHTNESS);

  // Turn all LEDs off initially
  fill_solid(leds, NUM_LEDS, CRGB::Red); //turn on
  FastLED.show();
}

void loop() {
  // Blink red LED
  //leds[LED_INDEX] = CRGB::Red;
  //FastLED.show();
  //delay(500);

  //leds[LED_INDEX] = CRGB::Black;
  //FastLED.show();
 // delay(500);
}
