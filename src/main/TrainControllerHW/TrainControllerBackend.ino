#include "Adafruit_Keypad.h"
#include <LiquidCrystal_I2C.h>
#define KEYPAD_PID419

#define R1    2
#define R2    3
#define R3    5
#define R4    7
#define C1    8
#define C2    10
#define C3    12
#define C4    13
#include "keypad_config.h"

bool enable = false;
String startCode = "33333333";

int authority = 0;
int commandedSpeed = 0;
int currentSpeed = 0;
int setpointSpeed = 0;
int driverSpeed;
String speedString = "";
String dataIn = "";
String dataOut = "";
bool headlights = 0;
bool E_Brake = 0;
bool S_Brake = 0;
bool mode = 1; //1 for automatic driving mode
bool R_Door = 0;
bool L_Door = 0;
bool inLights = 1;


//Power Variables
double kp = 10000;
double ki = 900;
double uk = 0;
double powerToSend = 0;
double powerLimit = 120;
double lastError = 0;
double thisError = 0;

LiquidCrystal_I2C lcd = LiquidCrystal_I2C(27, 16, 2);
//initialize an instance of class NewKeypad
Adafruit_Keypad customKeypad = Adafruit_Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS);

void setup() {
  Serial.begin(115200);
  customKeypad.begin();
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Welcome");
  //BUTTONS
  pinMode(22, INPUT);  //HEADLIGHTS
  pinMode(24, INPUT);  //E-BRAKE
  pinMode(26, INPUT);  //SERVICE BRAKE
  pinMode(28, INPUT);  //MODE BUTTON
  pinMode(30, INPUT);  //LEFT DOOR
  pinMode(32, INPUT);  //RIGHT DOOR
  pinMode(34, INPUT);  //INTERIOR LIGHTS
  pinMode(36, INPUT);  //
  pinMode(38, INPUT);  //
  pinMode(40, INPUT);  //
  pinMode(42, INPUT);  //

  //LEDS FOR UI
  pinMode(23, OUTPUT); //HEADLIGHTS
  pinMode(25, OUTPUT); //E-BRAKE ENGAGED
  pinMode(27, OUTPUT); //SERVICE BRAKE ENGAGED
  pinMode(29, OUTPUT); //MODE LIGHT (ON FOR AUTOMATIC)
  pinMode(31, OUTPUT); //LEFT DOOR STATE
  pinMode(33, OUTPUT); //RIGHT DOOR STATE
  pinMode(35, OUTPUT); //INTERIOR LIGHTS
}

String formatPower(double);

void loop() {
  while(!enable)
  {
    while(!Serial.available());
    String en = Serial.readString();
      if (en == "33333333")
      {
        enable = true;
      }
  }
  if (enable)
  {
    // put your main code here, to run repeatedly:
    speedString = "";
    dataOut = "0000000";
    while (!Serial.available());
    dataIn = Serial.readString();
    if (digitalRead(28))
    {
      mode = !mode;
    }
    if (!mode)
    {
      if (digitalRead(22))
      {
        headlights = !headlights;
      }
      if (digitalRead(24))
      {
        E_Brake = !E_Brake;
      }
      if (digitalRead(26))
      {
        S_Brake = !S_Brake;
      }
      if (digitalRead(30))
      {
        L_Door = !L_Door;
      }
      if (digitalRead(32))
      {
        R_Door = !R_Door;
      }
      if (digitalRead(34))
      {
        inLights = !inLights;
      }
      customKeypad.tick();

      if(customKeypad.available())
      {
        keypadEvent e = customKeypad.read();
        if (e.bit.KEY == 'A')
        {
          lcd.clear();                 // clear display
          lcd.setCursor(0, 0);         // move cursor to   (0, 0)
          lcd.print("Enter Speed:");
          lcd.setCursor(0, 1);
          bool speedMode = 1;
          while (speedMode)
          {
            customKeypad.tick();
            if(customKeypad.available())
            {
              speedString += (char)customKeypad.read().bit.KEY;
              lcd.print(speedString);
            }
            if (speedString.length() == 2)
            {
              speedMode = 0;
            }
          }
          driverSpeed = speedString.toInt();
        }
      }
    }
    else
    {
      if (dataIn[0] == '0')
      {
        headlights = dataIn[1];
        E_Brake    = dataIn[2];
        S_Brake    = dataIn[3];
        L_Door     = dataIn[4];
        R_Door     = dataIn[5];
        inLights   = dataIn[6];
      }
    }

    if (dataIn[0] == "1")
    {
      authority = dataIn[7];
      currentSpeed = 10*dataIn[1] + dataIn[2];
      commandedSpeed = 10*dataIn[3] + dataIn[4];
    }

    digitalWrite(23, headlights);
    digitalWrite(25, E_Brake);
    digitalWrite(27, S_Brake);
    digitalWrite(29, mode);
    digitalWrite(31, L_Door);
    digitalWrite(33, R_Door);
    digitalWrite(35, inLights);

    lcd.clear();                 // clear display
    lcd.setCursor(0, 0);         // move cursor to   (0, 0)
    lcd.print("Speed: " + String(currentSpeed) + " mph");
    lcd.setCursor(0, 1);
    lcd.print("Set Speed: " + String(commandedSpeed) + "mph");

    //Power Calculation
    if (mode)
    {
      setpointSpeed = commandedSpeed;
    }
    else
    {
      setpointSpeed = driverSpeed;
    }
    double newError = (setpointSpeed - currentSpeed) / 2.237;
    if (newError == 0 && lastError == 0)
    {
      powerToSend = 0;
    }
    else
    {
      double newUk = uk + (newError + lastError)/2;
      double power1 = kp * newError + ki * newUk;
      double power2 = kp * newError + ki * newUk;
      double power3 = kp * newError + ki * newUk;
      powerToSend = (power1 + power2 + power3) / 3;
      uk = newUk;
      lastError = newError;
    }

    if (!mode)
    {
      dataOut[0] = headlights;
      dataOut[1] = E_Brake;
      dataOut[2] = S_Brake;
      dataOut[3] = mode;
      dataOut[4] = L_Door;
      dataOut[5] = R_Door;
      dataOut[6] = inLights;
    }
    dataOut += formatPower(powerToSend);
    Serial.print(dataOut);

    //delay(10);
  }
}

String formatPower(double p)
{
  String outString = "";
  if (p < 10)
  {
    outString = "00" + (int)(p * 100);
  }
  else if (p < 100)
  {
    outString = "0" + (int)(p * 100);
  }
  else
  {
    outString = p * 100;
  }
  return outString;
}