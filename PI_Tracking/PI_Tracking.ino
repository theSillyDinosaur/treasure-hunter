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
  // waiting for game start!
  MotorWriting(0, 0);
  while(BT.available() == 0 || BT.read() != 's') delay(10);

  // initialization in every task
  char act = 'a'; // a means empty
  /* vvvvvvvvvv determining the ratio of response, need to modify vvvvvvvvvv */
  int SI_max = 150, norm_speed = 255;
  int S_ratio = 2, L_ratio = 2, LP_coeff[5] = {norm_speed*2, norm_speed*2/3, 0, -norm_speed*2/3, -norm_speed*2};
  /* ^^^^^^^^^^ determining the ratio of response, need to modify ^^^^^^^^^^ */
  double LP = 0., LP_pre = 0., SI = SI_max / 2, LI = 0.; // initialize - right p, straight i, right i; set straight i to accelerate while being confident

  // start tracking
  while(act != 'z'){
    // initialization in any loop
    Serial.write(act);
    int T_count = 0; // determine the situation, # of TCRT triggered
    int Ls = 0; // set if there's side TCRT's triggered
    LP = 0.; // RP reset
    SI *= S_ratio/(S_ratio+1); // SI decaying
    LI *= L_ratio/(L_ratio+1); // RI decaying

    // Step1: communicating
    if(BT.available() && act == 'a'){
      act = BT.read(); // next action read
      Serial.write(act);
    }
    UID_detect(); // RFID read and send
    
    // Step2: TCRT detecting, variable getting & I setting
    for(int i = 0; i < 5; i++){
      if(digitalRead(TCRT_digitalPin[i])){
        LP += LP_coeff[i]; // LP Step1: adding coefficient
        T_count++; // count # of TCRT triggered
        if(i == 2) SI += SI_max/(S_ratio+1); // straight adding
        if(i == 1) Ls = 1;
        if(i == 5) Ls = -1;
      }
    }
    if(T_count == 0) LP = LP_pre;
    else LP /= T_count;
    LI += LP/(L_ratio+1);

    //step3-1: normal tracking, setting of the MotorWriting()
    if (T_count < 5){
      if(LI > 0) MotorWriting(norm_speed-LI, norm_speed);
      else MotorWriting(norm_speed, norm_speed+LI);
    }
    
    // Step3-2: if we need to start next action...
    if (T_count > 4){

      // determine the next cmd
      if(act == 'f'){
        MotorWriting(255, 255);
        delay(300);
        //act = 'a';
        //continue; // It doesn't need to reset the variable while it's going straight (except act)
      }
      
      else if(act == 'r'){
        MotorWriting(255, 255);
        delay(270);
        MotorWriting(255, 0);
        delay(400);
        while(digitalRead(TCRT_digitalPin[4]) == 0 && digitalRead(TCRT_digitalPin[1]) == 0 && digitalRead(TCRT_digitalPin[2]) == 0 && digitalRead(TCRT_digitalPin[3]) == 0) delay(10);
      }
      
      else if(act == 'l'){
        MotorWriting(255, 255);
        delay(270);
        MotorWriting(0, 255);
        delay(400);
        while(digitalRead(TCRT_digitalPin[0]) == 0 && digitalRead(TCRT_digitalPin[1]) == 0 && digitalRead(TCRT_digitalPin[2]) == 0 && digitalRead(TCRT_digitalPin[3]) == 0) delay(10);
      }
      
      else if(act == 'b'){
        MotorWriting(255, 255);
        delay(200);
        MotorWriting(150, -150);
        delay(500);
        while(digitalRead(TCRT_digitalPin[4]) == 0) delay(10);
        MotorWriting(100, -100);
        while(digitalRead(TCRT_digitalPin[1]) == 0 && digitalRead(TCRT_digitalPin[2]) == 0 && digitalRead(TCRT_digitalPin[3]) == 0) delay(10);
      }
      else if(act == 'e'){
        MotorWriting(255, -255); // YEAH! -by Jamie Oliver
        delay(3000);
        MotorWriting(0, 0);
        act = 'z';
        break; // break the while() loop, stop tracking
      }
      
      // move out of the node
      MotorWriting(255, 255);
      delay(100);
      
      // reset variable
      act = 'a';
      LP = 0.;
      LP_pre = 0.;
      SI = SI_max;
      LI = 0.;
      continue; // no need for tracking
    }//end of conduct cmd
    
    // Step4: set if the next condition is all blank
    if(Ls == -1) LP_pre = LP_coeff[4];
    else if(Ls == 1) LP_pre = LP_coeff[0];
    else LP_pre = LP;
  }
}
