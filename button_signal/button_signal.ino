  const int buttonPin = 8;

  void setup() {
    pinMode(buttonPin, INPUT_PULLUP);  // enables internal pull-up
    pinMode(LED_BUILTIN, OUTPUT);
    Serial.begin(9600);
  }

  void loop() {
    digitalWrite(LED_BUILTIN, HIGH);
    delay(500);
    digitalWrite(LED_BUILTIN, LOW);
    delay(500);
    int state = digitalRead(buttonPin);
    if (state == LOW) {  // pressed
      Serial.println("Button pressed!");
    } else {
      Serial.println("Not pressed");
    }
  }
