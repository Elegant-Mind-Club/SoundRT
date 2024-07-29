// Reaction time experiment of one LED.
// LED will flash 3 times before the start of the experiment.
int trialMax = 100;
int numCorrect = 0;
int numMotors = 3;  // 3 INPUT RT TEST
int trialNum = 0;

// LED variables
int motorPick;
int motorPin1 = 12;
int motorPin3 = 11;
int motorPin2 = 10;

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
long newT;
long oldT;
long deltaT;

// The setup function runs once when you press reset or power the board
void setup() {
  // initialize analog pins as an output.
  pinMode(motorPin1, OUTPUT);
  pinMode(motorPin2, OUTPUT);
  pinMode(motorPin3, OUTPUT);

  // Initialize button pins as input.
  pinMode(buttonPin1, INPUT);
  pinMode(buttonPin2, INPUT);
  pinMode(buttonPin3, INPUT);

  // Intialize serial communication.
  Serial.begin(9600);

  Serial.println("Prepare. Reaction time measurements will begin shortly!");
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

  randomSeed(analogRead(A0));
  randDelay = random(3000, 6000);
  delay(randDelay);
}

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

    // Turn the LED on and record time, trial has begun.
    if (motorPick == 0) {
      digitalWrite(motorPin1, HIGH);
      oldT = millis();
      motorState1 = HIGH;
      motorState2 = LOW;
      motorState3 = LOW;
    } else if (motorPick == 1) {
      digitalWrite(motorPin2, HIGH);
      oldT = millis();
      motorState1 = LOW;
      motorState2 = HIGH;
      motorState3 = LOW;
    } else {
      digitalWrite(motorPin3, HIGH);
      oldT = millis();
      motorState1 = LOW;
      motorState2 = LOW;
      motorState3 = HIGH;
    }
  }

  // Criteria for trial end.
  if (motorState1 == HIGH && buttonState1 == HIGH) {
    numCorrect++;
    trialNum++;

    // Record time when button was pressed and turn off LED
    newT = millis();
    digitalWrite(motorPin1, 0);

    // Print to console the time differnce between LED turn off to button pressed.
    deltaT = newT - oldT;
    Serial.print(trialNum);
    Serial.print(";1;");
    Serial.println(deltaT);

    // Reset trial and wait a random amount of time for next trial.
    motorState1 = LOW;
    randDelay = random(1000, 3000);
    delay(randDelay);
  } else if (motorState2 == HIGH && buttonState2 == HIGH) {
    numCorrect++;
    trialNum++;

    // Record time when button was pressed and turn off LED
    newT = millis();
    digitalWrite(motorPin2, 0);

    // Print to console the time differnce between LED turn off to button pressed.
    deltaT = newT - oldT;
    Serial.print(trialNum);
    Serial.print(";2;");
    Serial.println(deltaT);

    // Reset trial and wait a random amount of time for next trial.
    motorState2 = LOW;
    randDelay = random(1000, 3000);
    delay(randDelay);
  } else if (motorState3 == HIGH && buttonState3 == HIGH) {
    numCorrect++;
    trialNum++;

    // Record time when button was pressed and turn off LED
    newT = millis();
    digitalWrite(motorPin3, 0);

    // Print to console the time differnce between LED turn off to button pressed.
    deltaT = newT - oldT;
    Serial.print(trialNum);
    Serial.print(";3;");
    Serial.println(deltaT);

    // Reset trial and wait a random amount of time for next trial.
    motorState3 = LOW;
    randDelay = random(1000, 3000);
    delay(randDelay);
  } 
  else if (buttonState1 == HIGH || buttonState2 == HIGH || buttonState3 == HIGH) {
    trialNum++;
    if (motorState3 == HIGH) {
      digitalWrite(motorPin3, 0);
      // Print to console the time differnce between LED turn off to button pressed.
      Serial.print(trialNum);
      Serial.print(";2;");
      Serial.println(0);
      motorState3 = LOW;
    } else if (motorState2 == HIGH) {
      digitalWrite(motorPin2, 0);
      // Print to console the time differnce between LED turn off to button pressed.
      Serial.print(trialNum);
      Serial.print(";2;");
      Serial.println(0);
      motorState2 = LOW;
    } else if (motorState1 == HIGH) {
      digitalWrite(motorPin1, 0);
      // Print to console the time differnce between LED turn off to button pressed.
      Serial.print(trialNum);
      Serial.print(";1;");
      Serial.println(0);
      motorState1 = LOW;
    }


    // Reset trial and wait a random amount of time for next trial.
    randDelay = random(1000, 3000);
    delay(randDelay);
  }
  if (numCorrect == trialMax) {
    for (int i = 0; i <= 2; i++) {
      digitalWrite(motorPin1, HIGH);
      digitalWrite(motorPin2, HIGH);
      // digitalWrite(motorPin3, HIGH);
      delay(250);
      digitalWrite(motorPin1, LOW);
      digitalWrite(motorPin2, LOW);
      // digitalWrite(motorPin3, LOW);
      delay(250);
    }
    exit(0);
  }
}
