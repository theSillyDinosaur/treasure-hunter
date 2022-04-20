#include "car_init.h"

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  //RFID setup
  SPI.begin();
  mfrc522 = new MFRC522(RFID_SS_PIN, RFID_RST_PIN); 
  mfrc522->PCD_Init();
  Serial.println(F("Read UID on a MIFARE PICC:")); 

  //TCRT setup
  for(int i=0; i<5; i++)
    pinMode(TCRT_digitalPin[i], INPUT);

  //TB setup
  pinMode(TB_PWMA, OUTPUT);
  pinMode(TB_PWMB, OUTPUT);
  pinMode(TB_AIN1, OUTPUT);
  pinMode(TB_AIN2, OUTPUT);
  pinMode(TB_BIN1, OUTPUT);
  pinMode(TB_BIN1, OUTPUT);

  //BT setup
  BT.begin(9600);

  
}

void loop() {
  // put your main code here, to run repeatedly:
  MotorWriting(0, 0);
  while(BT.available() == 0 || BT.read() != 's') delay(10);
  char act = 'a';
  while(act != 'e'){
    int T = 0, T_count = 0;
    if(BT.available() && act == 'a'){
      act = BT.read();
    }
    //RFID
    UID_detect();
  
    //tracking
    for(int i = 0; i < 5; i++){
      T = T << 1;
      T += digitalRead(TCRT_digitalPin[i]);
      if(digitalRead(TCRT_digitalPin[i])) T_count++;
    }
    if(T == 1 || T == 3)MotorWriting(100, 30);
    if(T == 16 || T == 24)MotorWriting(30, 100);
    if(T == 2) MotorWriting(150, 100);
    if(T == 6) MotorWriting(150, 125);
    if(T == 4) MotorWriting(150, 150);
    if(T == 12) MotorWriting(125, 150);
    if(T == 8) MotorWriting(100, 150);
    if(T == 7){
      MotorWriting(125, 0);
      while(digitalRead(TCRT_digitalPin[2]) == 0) delay(10);
    }
    if(T == 28){
      MotorWriting(0, 125);
      while(digitalRead(TCRT_digitalPin[2]) == 0) delay(10);
    }
    
    if(T_count > 3){
      MotorWriting(150, 150);
      for(int i = 0; i < 35; i++) UID_detect();
      while(true){
        if(act == 'f'){
          delay(750);
          break;
        }
        else if(act == 'r'){
          MotorWriting(75, -75);
          delay(1020);
          //while(digitalRead(TCRT_digitalPin[1]) == 0 && digitalRead(TCRT_digitalPin[2]) == 0 && digitalRead(TCRT_digitalPin[3]) == 0) delay(10);
          MotorWriting(150, 150);
          delay(300);
          break;
        }
        else if(act == 'l'){
          MotorWriting(-75, 75);
          delay(1020);
          //while(digitalRead(TCRT_digitalPin[1]) == 0 && digitalRead(TCRT_digitalPin[2]) == 0 && digitalRead(TCRT_digitalPin[3]) == 0) delay(10);
          MotorWriting(150, 150);
          delay(300);
          break;
        }
        else if(act == 'b'){
          MotorWriting(75, -75);
          delay(2040);
          //while(digitalRead(TCRT_digitalPin[1]) == 0 && digitalRead(TCRT_digitalPin[2]) == 0 && digitalRead(TCRT_digitalPin[3]) == 0) delay(10);
          MotorWriting(150, 150);
          delay(300);
          break;
        }
        else{
          MotorWriting(0, 0);
          if(BT.available()) act = BT.read();
        }
      }
      act = 'a';
    }
  }
}
