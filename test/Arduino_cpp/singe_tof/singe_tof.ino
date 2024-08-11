#include "Adafruit_VL53L1X.h"

// XSHUT pin
#define XSHUT_FRONT 2

// I2C Address
#define I2C_ADDR_FRONT 0x30

// Timming Budget
#define TIMING 50

// Buffer settings
#define BUFFER_SIZE 10

//MAXIMUM SIZE
#define MAX 150

Adafruit_VL53L1X sensorFront;

// Buffer for distance readings
int16_t distanceBuffer[BUFFER_SIZE];
int bufferIndex = 0;
int16_t distanceSum = 0;
int front;

void setup() {
  Serial.begin(115200);
  Serial.println("Starting");
  Wire.begin();
  Serial.println("I2C Done");

  // Initialize sensor
  initializeSensor(sensorFront, XSHUT_FRONT, I2C_ADDR_FRONT, TIMING);
  Serial.println("Sensor Done");

  // Initialize buffer
  for (int i = 0; i < BUFFER_SIZE; i++) {
    distanceBuffer[i] = 0;
  }
  Serial.println("buffer Done");
}

void loop() {

  float set_offset = 1.25;
  // Update buffer and print distance from the sensor
  front = round(updateBufferAndPrintDistance(sensorFront) - set_offset);
  Serial.print(updateBufferAndPrintDistance(sensorFront));
  Serial.print(" | ");
  Serial.print(updateBufferAndPrintDistance(sensorFront) - set_offset);
  Serial.print(" | ");
  Serial.print(F(" Distance: "));
  Serial.print(front);
  Serial.println(" cm");
  delay(10);  // Delay between readings
}

void initializeSensor(Adafruit_VL53L1X &sensor, int xshutPin, uint8_t address, int timing) {
  // Reset sensor via XSHUT pin
  pinMode(xshutPin, OUTPUT);
  digitalWrite(xshutPin, LOW);
  delay(100);
  digitalWrite(xshutPin, HIGH);
  delay(100);

  if (!sensor.begin(address, &Wire)) {
    Serial.print(F("Error initializing sensor at XSHUT pin "));
    Serial.println(xshutPin);
    while (1) delay(10);  // Stop if sensor fails to initialize
  }

  if (!sensor.startRanging()) {
    Serial.print(F("Couldn't start ranging on sensor at address 0x"));
    Serial.println(address, HEX);
    while (1) delay(10);  // Stop if ranging can't be started
  }

  // Set timing budget
  sensor.setTimingBudget(timing);  // Set timing budget to 50 ms
  Serial.print(F("Timing budget (ms): "));
  Serial.println(sensor.getTimingBudget());

  Serial.print(F("Sensor initialized at address 0x"));
  Serial.println(address, HEX);
}

float updateBufferAndPrintDistance(Adafruit_VL53L1X &sensor) {
  if (sensor.dataReady()) {
    int16_t newDistance = sensor.distance();

    if (newDistance != -1) {
      // Update buffer
      distanceSum -= distanceBuffer[bufferIndex];
      distanceBuffer[bufferIndex] = newDistance;
      distanceSum += distanceBuffer[bufferIndex];
      bufferIndex = (bufferIndex + 1) % BUFFER_SIZE;

      // Calculate and print average distance in cm
      float averageDistanceCm = distanceSum / (float)BUFFER_SIZE / 10.0;

      return averageDistanceCm;

      sensor.clearInterrupt();  // Prepare for next reading
    } else {
      return MAX;
    }
  }
}
