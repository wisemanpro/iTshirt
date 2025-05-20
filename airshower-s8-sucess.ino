
#include <MECHA_PMS5003ST.h>  //24.4.18. PM 2:22

#define SWITCH1 14  // on/off main button switch
#define SWITCH2 15  // Ai select switch
#define SENSOR 3    // motion sensor
#define FAN 6
#define FANPOWER A0
#define UVLED A1

volatile bool motionFlag = false;
unsigned long lastMotionTime = 0;
unsigned long debounceInterval = 5000;

bool inShower = false;
bool airCleaning = false;
unsigned long showerStartTime = 0;
unsigned long showerDuration = 10000;
unsigned long lastShowerEndTime = 0;
unsigned long reDetectDelay = 10000;

bool MAINSWITCH;
bool AISWITCH;

int showerPower = 200;
int showertime = 3;
int showerspeed = 1;

MECHA_PMS5003ST pms(&Serial2);

void setup() {

  pinMode(SWITCH1, INPUT_PULLUP);
  pinMode(SWITCH2, INPUT_PULLUP);
  pinMode(SENSOR, INPUT_PULLUP);
  pinMode(FAN, OUTPUT);
  pinMode(FANPOWER, OUTPUT);
  pinMode(UVLED, OUTPUT);

  Serial.begin(9600);
  Serial2.begin(9600);
  pms.begin();
  pms.setMode(PASSIVE);

  attachInterrupt(digitalPinToInterrupt(SENSOR), motionDetected, FALLING);

  digitalWrite(FANPOWER, LOW);
  digitalWrite(UVLED, LOW);
  delay(500);
}

void loop() {
  pms.request();
  pms.read();

  MAINSWITCH = digitalRead(SWITCH1);
  AISWITCH = digitalRead(SWITCH2);

   if (MAINSWITCH == HIGH && AISWITCH == HIGH) {
    powerOff();
  } else if (MAINSWITCH == LOW && AISWITCH == LOW) {
    airControlManual();
  } else if (MAINSWITCH == LOW && AISWITCH == HIGH) {
    airControlAI();
  } else if (MAINSWITCH == HIGH && AISWITCH == LOW) {
    airControlManual();
  }

  // 감지 → 에어샤워 시작
  if (motionFlag && !inShower && !airCleaning) {
    motionFlag = false;
    inShower = true;
    airCleaning = false;

    showerStartTime = millis();
    digitalWrite(FANPOWER, HIGH);
    digitalWrite(UVLED, HIGH);
// 에어샤워 시작
  }

  // 에어샤워 중
  if (inShower) {
    analogWrite(FAN, showerPower);
    if (millis() - showerStartTime >= showerDuration) {
      inShower = false;
      airCleaning = true;

      digitalWrite(UVLED, LOW);
      analogWrite(FAN, 30); // 공기정화 팬속도
// 에어샤워 종료 → 공기정화모드 진입
      lastShowerEndTime = millis(); // 10초동안 감지 무시
    }
  }

  // 공기정화 중 → 팬 유지
 if (airCleaning) {
  analogWrite(FAN, 30);

  if (motionFlag && millis() - lastShowerEndTime > reDetectDelay) {
    motionFlag = false;
    inShower = true;
    airCleaning = false;

    showerStartTime = millis();
    digitalWrite(FANPOWER, HIGH);
    digitalWrite(UVLED, HIGH);
  }
}

  delay(1000);
}

void motionDetected() {
  unsigned long now = millis();
  if (now - lastMotionTime > debounceInterval) {
    motionFlag = true;
    lastMotionTime = now;
// 디버깅용  Serial.println("[INTERRUPT] 사람이 감지됨 (motionFlag = true)");
  }
}

void powerOff() {
  digitalWrite(FANPOWER, LOW);
  digitalWrite(UVLED, LOW);
  analogWrite(FAN, 0);
  delay(500);
}

void airControlManual() {
  float pm25 = pms.getPmAto(2.5);
  showerDuration = 12500;
  showerPower = 200;

  Serial.print("-");
  Serial.print((int)pms.getTemp());
  Serial.print("-");
  Serial.print((int)pms.getHumi());
  Serial.print("-");
  Serial.print(pms.getForm(), 2);
  Serial.print("-");
  Serial.print((int)pms.getPmAto(10));
  Serial.print("-");
  Serial.print((int)pms.getPmAto(2.5));
  Serial.print("-");
  Serial.print((int)pms.getPmAto(1.0));
  Serial.print("-");
  Serial.print(showertime);
  Serial.print("-");
  Serial.print(showerspeed);
  Serial.print("-");
  Serial.println();
}

void airControlAI() {
  float pm25 = pms.getPmAto(2.5);
  if (pm25 <= 15) {
    goodair(); showerDuration = 7000; showerPower = 70;
  } else if (pm25 <= 50) {
    normalair(); showerDuration = 8500; showerPower = 100;
  } else if (pm25 <= 100) {
    badair(); showerDuration = 10000; showerPower = 150;
  } else {
    seriousair(); showerDuration = 12500; showerPower = 200;
  }

  Serial.print("-");
  Serial.print((int)pms.getTemp());
  Serial.print("-");
  Serial.print((int)pms.getHumi());
  Serial.print("-");
  Serial.print(pms.getForm(), 2);
  Serial.print("-");
  Serial.print((int)pms.getPmAto(10));
  Serial.print("-");
  Serial.print((int)pms.getPmAto(2.5));
  Serial.print("-");
  Serial.print((int)pms.getPmAto(1.0));
  Serial.print("-");
  Serial.print(showertime);
  Serial.print("-");
  Serial.print(showerspeed);
  Serial.print("-");
  Serial.println();
}

void UVLED_off_airclean_mode() {
  digitalWrite(UVLED, LOW);
  analogWrite(FAN, 50);
}

void goodair() {
  digitalWrite(FANPOWER, HIGH);
  digitalWrite(UVLED, LOW);
  analogWrite(FAN, 30);
}

void normalair() {
  digitalWrite(FANPOWER, HIGH);
  digitalWrite(UVLED, LOW);
  analogWrite(FAN, 50);
}

void badair() {
  digitalWrite(FANPOWER, HIGH);
  digitalWrite(UVLED, LOW);
  analogWrite(FAN, 75);
}

void seriousair() {
  digitalWrite(FANPOWER, HIGH);
  digitalWrite(UVLED, LOW);
  analogWrite(FAN, 100);
}
