#include "Adafruit_VL53L1X.h"

// XSHUT pins
#define XSHUT_FRONT 2
#define XSHUT_BACK 14
#define XSHUT_RIGHT 4
#define XSHUT_LEFT 5
#define XSHUT_BOTTOM 12

// I2C Addresses
#define I2C_ADDR_FRONT 0x30
#define I2C_ADDR_BACK 0x31
#define I2C_ADDR_RIGHT 0x32
#define I2C_ADDR_LEFT 0x33
#define I2C_ADDR_BOTTOM 0x34

// Timing Budget
#define TIMING 50

// Buffer settings
#define BUFFER_SIZE 10

// Maximum size for error handling
#define MAX 150

Adafruit_VL53L1X sensorFront;
Adafruit_VL53L1X sensorBack;
Adafruit_VL53L1X sensorRight;
Adafruit_VL53L1X sensorLeft;
Adafruit_VL53L1X sensorBottom;

// Buffers for distance readings
int16_t distanceBufferFront[BUFFER_SIZE];
int16_t distanceBufferBack[BUFFER_SIZE];
int16_t distanceBufferRight[BUFFER_SIZE];
int16_t distanceBufferLeft[BUFFER_SIZE];
int16_t distanceBufferBottom[BUFFER_SIZE];

// Buffer indices and sums
int bufferIndexFront = 0, bufferIndexBack = 0;
int16_t distanceSumFront = 0, distanceSumBack = 0;
int bufferIndexRight = 0, bufferIndexLeft = 0, bufferIndexBottom = 0;
int16_t distanceSumRight = 0, distanceSumLeft = 0, distanceSumBottom = 0;

void setup() {
  Serial.begin(115200);
  Serial.println("Starting");
  Wire.begin();
  Serial.println("I2C Done");

  // Initialize sensors
  initializeSensor(sensorFront, XSHUT_FRONT, I2C_ADDR_FRONT, TIMING);
  initializeSensor(sensorBack, XSHUT_BACK, I2C_ADDR_BACK, TIMING);
  initializeSensor(sensorRight, XSHUT_RIGHT, I2C_ADDR_RIGHT, TIMING);
  initializeSensor(sensorLeft, XSHUT_LEFT, I2C_ADDR_LEFT, TIMING);
  initializeSensor(sensorBottom, XSHUT_BOTTOM, I2C_ADDR_BOTTOM, TIMING);

  Serial.println("Sensors Done");

  // Initialize buffers
  for (int i = 0; i < BUFFER_SIZE; i++) {
    distanceBufferFront[i] = 0;
    distanceBufferBack[i] = 0;
    distanceBufferRight[i] = 0;
    distanceBufferLeft[i] = 0;
    distanceBufferBottom[i] = 0;
  }

  Serial.println("Buffer Done");
}

void loop() {
  float set_offset = 1.25;

  // Update buffer and print distance for each sensor
  int frontDistance = round(updateBufferAndPrintDistance(sensorFront, distanceBufferFront, bufferIndexFront, distanceSumFront) - set_offset);
  int backDistance = round(updateBufferAndPrintDistance(sensorBack, distanceBufferBack, bufferIndexBack, distanceSumBack) - set_offset);
  int rightDistance = round(updateBufferAndPrintDistance(sensorRight, distanceBufferRight, bufferIndexRight, distanceSumRight) - set_offset);
  int leftDistance = round(updateBufferAndPrintDistance(sensorLeft, distanceBufferLeft, bufferIndexLeft, distanceSumLeft) - set_offset);
  int bottomDistance = round(updateBufferAndPrintDistance(sensorBottom, distanceBufferBottom, bufferIndexBottom, distanceSumBottom) - set_offset);

  // Print distances with offset
  Serial.print("Front: ");
  Serial.print(frontDistance);
  Serial.println(" cm");

  Serial.print("Back: ");
  Serial.print(backDistance);
  Serial.println(" cm");

  Serial.print("Right: ");
  Serial.print(rightDistance);
  Serial.println(" cm");

  Serial.print("Left: ");
  Serial.print(leftDistance);
  Serial.println(" cm");

  Serial.print("Bottom: ");
  Serial.print(bottomDistance);
  Serial.println(" cm");

  delay(500);  // Delay between readings
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
  sensor.setTimingBudget(timing);  // Set timing budget
  Serial.print(F("Timing budget (ms): "));
  Serial.println(sensor.getTimingBudget());

  Serial.print(F("Sensor initialized at address 0x"));
  Serial.println(address, HEX);
}

float updateBufferAndPrintDistance(Adafruit_VL53L1X &sensor, int16_t *buffer, int &bufferIndex, int16_t &distanceSum) {
  if (sensor.dataReady()) {
    int16_t newDistance = sensor.distance();

    if (newDistance != -1) {
      // Update buffer
      distanceSum -= buffer[bufferIndex];
      buffer[bufferIndex] = newDistance;
      distanceSum += buffer[bufferIndex];
      bufferIndex = (bufferIndex + 1) % BUFFER_SIZE;

      // Calculate and return average distance in cm
      return distanceSum / (float)BUFFER_SIZE / 10.0;
    } else {
      return MAX;
    }
  }
}
