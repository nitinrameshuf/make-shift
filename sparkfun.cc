#include <Servo.h>

Servo myServo;
int servoPin = 7;
int ledPin = LED_BUILTIN; // Onboard LED pin (usually built-in)

void setup() {
    Serial.begin(9600);  // Serial communication at 9600 baud
    myServo.attach(servoPin);
    pinMode(ledPin, OUTPUT);  // Set LED pin as output
    Serial.println("Waiting for joystick value (0-26400):");
}

void loop() {
    if (Serial.available()) {
        digitalWrite(ledPin, HIGH);  // 🔥 Turn ON LED when serial input starts

        String input = Serial.readStringUntil('\n');  
        input.trim();  

        if (input.length() == 0) {
            digitalWrite(ledPin, LOW); // Turn OFF LED if no useful data
            return;
        }

        int joystickValue = input.toInt();  

        // Constrain joystick value safely
        joystickValue = constrain(joystickValue, 0, 26400);

        // Map joystick (0–26400) to angle (0–180)
        int angle = map(joystickValue, 0, 26400, 0, 180);

        // Optional: Center deadzone smoothing
        int center = 13200;  // Center of joystick
        if (abs(joystickValue - center) < 500) {
            angle = 90;
        }

        // Fine-tune servo movement
        if (angle == 0) {
            Serial.println("Fine-tuning 0-degree position...");
            myServo.writeMicroseconds(525);  // Adjust this value if needed
        } else {
            // Map angle to pulse width (MG996R-style servo)
            int pulseWidth = map(angle, 0, 180, 500, 2500); 
            myServo.writeMicroseconds(pulseWidth);
        }

        Serial.print("Joystick: ");
        Serial.print(joystickValue);
        Serial.print(" -> Servo moved to: ");
        Serial.print(angle);
        Serial.println(" degrees");

        Serial.println("Waiting for next joystick value:");

        digitalWrite(ledPin, LOW);  // 🧠 Turn OFF LED after processing the input
    }
}
