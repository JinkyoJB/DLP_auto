//제어용 아두이노 포트번호는 16 
//21.11.02 모터 드라이버 교체--> 이전버전 코드와 모터 방향 반대
#define Blade_DIR 53
#define Blade_STEP 51
#define Blade1_ms1 49
#define Blade1_ms2 47
#define Blade1_SP 45
#define Blade2_ms1 43
#define Blade2_ms2 41
#define Blade2_SP 39
#define Blade_e 37 //Enable

#define zaxis_DIR 52
#define zaxis_STEP 50
#define zaxis1_ms1 48
#define zaxis1_ms2 46
#define zaxis1_SP 44
#define zaxis2_ms1 42
#define zaxis2_ms2 40
#define zaxis2_SP 38
#define zaxis_e 30 //Enable

#define button 34 //0812업글
#define sensor 32 //0812업글

#define resin_SIG 2

void setup()
{
  pinMode(Blade_e, OUTPUT);
  pinMode(zaxis_e, OUTPUT);
  digitalWrite(Blade_e,LOW);
  digitalWrite(zaxis_e,LOW);
  pinMode(Blade_DIR, OUTPUT);
  pinMode(Blade_STEP, OUTPUT);
  pinMode(Blade1_SP, OUTPUT);
  pinMode(Blade1_ms2, OUTPUT);
  pinMode(Blade1_ms1, OUTPUT);
  pinMode(Blade2_SP, OUTPUT);
  pinMode(Blade2_ms2, OUTPUT);
  pinMode(Blade2_ms1, OUTPUT);
 
  pinMode(zaxis_DIR, OUTPUT);
  pinMode(zaxis_STEP,OUTPUT);
  pinMode(zaxis1_SP, OUTPUT);
  pinMode(zaxis1_ms2, OUTPUT);
  pinMode(zaxis1_ms1, OUTPUT);
  pinMode(zaxis2_SP, OUTPUT);
  pinMode(zaxis2_ms2, OUTPUT);
  pinMode(zaxis2_ms1, OUTPUT);
  pinMode(resin_SIG, OUTPUT);
  
  pinMode(button, INPUT_PULLUP);
  pinMode(sensor, INPUT_PULLUP);
 
 Serial.begin(9600);
}
 
void loop()
{ 
  digitalWrite(resin_SIG,LOW);
  if(Serial.available() > 0)
  {
    String inString = Serial.readStringUntil('\n');
    int index1 = inString.indexOf(','); //문자열에 '찾을문자'가 있는 위치(index)값 반환
    int index2 = inString.indexOf(',', index1+1); //('찾을문자', 시작위치) 문자열의 시작위치에서 시작하고 '찾을문자'가 있는 위치값 반환
    int index3 = inString.length();
    int value1 = inString.substring(0, index1).toInt();
    int value2 = inString.substring(index1+1,index2).toInt();
    int value3 = inString.substring(index2+1,index3).toInt();
    
 ////Value2가 0이면 z축 관련
    if((value1 == 0) & (value2 == 0) & (value3 == 1)) /// z축이 리미트센서에 터치
    {
      zhoming();
    }
    if((value1 == 0) & (value2 == 0) & (value3 == 2)) /// z축이 블레이드 날에 닿는 위치로
    {
      zgoing();
    }

 ///value2 가 1이면 blade 관련
   if((value1 == 0) & (value2 == 1) & (value3 == 1)) ///blade Homing, 블레이드 시작 위치에서 멈추기
    {
      bhoming();
    }
   if((value1 == 0) & (value2 == 1) & (value3 == 2)) ///blade going
   {
      bgoing();
   }

   //resin함수
      if((value1 == 2) & (value2 == 2) & (value3 == 2))
   {
      resinshot();
   }

 ///원하는 스텝만큼 모터이동하는 함수들
    if(value1 == 7) //7은 blade함수
    {
      Serial.print(" blade:"); Serial.print(value3); Serial.print("step");
      blade(value2, value3);
    }
    if(value1 == 8) //8은 zaxis함수 
    {
      Serial.print(" zaxis:"); Serial.print(value3); Serial.print("step");
      zaxis(value2, value3); 
    }
  }
}
 
void blade(int direct, int step) // direct는 방향: 1은 앞으로, 0은 뒤로, step은 모터 step수,
{
    digitalWrite(Blade1_SP,LOW);
    digitalWrite(Blade1_ms2,HIGH);
    digitalWrite(Blade1_ms1,LOW);
    digitalWrite(Blade2_SP,LOW);
    digitalWrite(Blade2_ms2,HIGH);
    digitalWrite(Blade2_ms1,LOW);
  if(direct == 1)
  { 
    Serial.println(" forward");
    digitalWrite(Blade_DIR,LOW);
    for(int i = 0; i < step; i++)
      {
        digitalWrite(Blade_STEP,HIGH);
        delayMicroseconds(500);
        digitalWrite(Blade_STEP,LOW);
        delayMicroseconds(500);
      }
     Serial.println("*"); 
  }
  if(direct == 0)
  {
    Serial.println(" backward");
    digitalWrite(Blade_DIR,HIGH);
    for(int i = 0; i < step; i++)
      {
        digitalWrite(Blade_STEP,HIGH);
        delayMicroseconds(500);
        digitalWrite(Blade_STEP,LOW);
        delayMicroseconds(500);
      }
    Serial.println("*");
  }
}
 
void zaxis(int direct, int step) // direct는 방향: 1은 앞으로, 0은 뒤로, step은 모터 step수,
{
    digitalWrite(zaxis1_SP,LOW);
    digitalWrite(zaxis1_ms2,HIGH);
    digitalWrite(zaxis1_ms1,LOW);
    digitalWrite(zaxis2_SP,LOW);
    digitalWrite(zaxis2_ms2, HIGH);
    digitalWrite(zaxis2_ms1, LOW);
  if(direct == 1)
  {
    Serial.println(" up");
    digitalWrite(zaxis_DIR,LOW);
    for(int i = 0; i < step; i++)
      {
        digitalWrite(zaxis_STEP,HIGH);
        delayMicroseconds(1000);
        digitalWrite(zaxis_STEP,LOW);
        delayMicroseconds(1000);
      }
    Serial.println("*");
  }
  if(direct == 0)
  {
    Serial.println(" down");
    digitalWrite(zaxis_DIR,HIGH);
    for(int i = 0; i < step; i++)
      {
        digitalWrite(zaxis_STEP,HIGH);
        delayMicroseconds(1000);
        digitalWrite(zaxis_STEP,LOW);
        delayMicroseconds(1000);
      }
    Serial.println("*");
  }
}
 
void bhoming()
{
  Serial.println(" homing-blade");
  digitalWrite(Blade1_SP,LOW);
  digitalWrite(Blade1_ms2,LOW);
  digitalWrite(Blade1_ms1,LOW);
  digitalWrite(Blade2_SP,LOW);
  digitalWrite(Blade2_ms2,LOW);
  digitalWrite(Blade2_ms1,LOW);
 
  digitalWrite(Blade_DIR, LOW);
  
  for(int i = 0; i < 9999999; i++ ) 
  {
    if( digitalRead(button) == HIGH) 
    {
      Serial.println(" blade touched");
      break;
    } 
    else 
    {
      digitalWrite(Blade_STEP,HIGH);
      delayMicroseconds(700);
      digitalWrite(Blade_STEP,LOW);
      delayMicroseconds(700);
    }
  }
 Serial.println("*");
}

///블레이드시작위치로 부터 일정 스텝만큼 뒤로 이동하는 함수
void bgoing()
{
    digitalWrite(Blade1_SP, LOW);
    digitalWrite(Blade1_ms2,HIGH);
    digitalWrite(Blade1_ms1,LOW);
    digitalWrite(Blade2_SP,LOW);
    digitalWrite(Blade2_ms2,HIGH);
    digitalWrite(Blade2_ms1,LOW);

    digitalWrite(Blade_DIR, HIGH);
    
  for(int i = 0; i < 32000; i++)
  {
    digitalWrite(Blade_STEP,HIGH);
    delayMicroseconds(500);
    digitalWrite(Blade_STEP,LOW);
    delayMicroseconds(500);
  }
  for(int i = 0; i < 2800; i++)
  {
    digitalWrite(Blade_STEP,HIGH);
    delayMicroseconds(500);
    digitalWrite(Blade_STEP,LOW);
    delayMicroseconds(500);
  }
 Serial.println("*");
}

///z축이 리미트센서에 닿도록 아래로 이동하는 함수
void zhoming()
{
  Serial.println(" homing-Z-axis");
  digitalWrite(zaxis1_SP, LOW);    
  digitalWrite(zaxis1_ms2, HIGH);
  digitalWrite(zaxis1_ms1, LOW);
  digitalWrite(zaxis2_SP, LOW);
  digitalWrite(zaxis2_ms2, HIGH);
  digitalWrite(zaxis2_ms1, LOW);   
 
  digitalWrite(zaxis_DIR, HIGH);
  
  for(int i = 0; i < 9999999; i++ ) 
  {
    if( digitalRead(sensor) == HIGH ) 
    {
      Serial.println(" z-axis sensor touched");
      break;
    } 
    else 
    {
      digitalWrite(zaxis_STEP,HIGH);
      delayMicroseconds(700);
      digitalWrite(zaxis_STEP,LOW);
      delayMicroseconds(700);
    }
  }
  Serial.println("*");
}

///z판이 블레이드 날에 닿도록 일정위치 이동하는 함수 , 25.5mm 이동
void zgoing()
{
  Serial.println(" going-Z-axis");
  digitalWrite(zaxis1_SP, LOW);    
  digitalWrite(zaxis1_ms2, HIGH);
  digitalWrite(zaxis1_ms1, LOW);
  digitalWrite(zaxis2_SP, LOW);
  digitalWrite(zaxis2_ms2, HIGH);
  digitalWrite(zaxis2_ms1, LOW);    
 
  digitalWrite(zaxis_DIR, LOW);
   
  for(int i = 0; i < 22050; i++)   //23000
  {
    digitalWrite(zaxis_STEP,HIGH);
    delayMicroseconds(700);
    digitalWrite(zaxis_STEP,LOW);
    delayMicroseconds(700);
  }
 Serial.println("*");
}

void resinshot()
{
    Serial.println(" resin shot");
    digitalWrite(resin_SIG, HIGH);
    delay(1000);
    pinMode(resin_SIG, OUTPUT);
    Serial.println("*");
}
