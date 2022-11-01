/* EE16A Toucscreen 3
   Capacitive Touchscreen Simulation
   Seiya Ono Sp '19
*/

int ledPin = P2_5;
int touch = 255;
int step_size = 5;
const int buttonPin = P2_1;
int buttonState;
int lastButtonState = LOW;
long lastDebounceTime = 0;
long debounceDelay = 50;
void setup()  {
  Serial.begin(9600);
  pinMode(buttonPin, INPUT_PULLUP);
  pinMode(ledPin, OUTPUT);
}

void loop()  {
  int reading = digitalRead(buttonPin);
  if (!buttonState) {
    Serial.println("Touch Detected!");
  }
  if (reading != lastButtonState)lastDebounceTime = millis();
  if ((millis() - lastDebounceTime) > debounceDelay) buttonState = reading;
  lastButtonState = reading;

  touch = !buttonState ?  50 : 255;
  for (int fadeValue = 0 ; fadeValue <= touch; fadeValue += step_size) {
    analogWrite(ledPin, fadeValue);
  }
  for (int fadeValue = touch ; fadeValue >= 0; fadeValue -= step_size) {
    analogWrite(ledPin, fadeValue);
  }
}


