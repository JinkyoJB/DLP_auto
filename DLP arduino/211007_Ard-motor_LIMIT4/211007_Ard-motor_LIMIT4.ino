//제어용 아두이노 포트번호는 16
#define Blade_DIR 53
#define Blade_STEP 51
#define Blade1_ms1 49
#define Blade1_ms2 47
#define Blade1_ms3 45
#define Blade2_ms1 43
#define Blade2_ms2 41
#define Blade2_ms3 39
#define Blade_e 37 //Enable
#define zaxis_DIR 52
#define zaxis_STEP 50
#define zaxis1_ms1 48
#define zaxis1_ms2 46
#define zaxis1_ms3 44
#define zaxis2_ms1 42
#define zaxis2_ms2 40
#define zaxis2_ms3 38
#define zaxis_e 30 //Enable

#define button 34 //0812업글
#define sensor 32 //0812업글
 
void setup()
{
  pinMode(Blade_e, OUTPUT);
  pinMode(zaxis_e, OUTPUT);
  digitalWrite(Blade_e,LOW);
  digitalWrite(zaxis_e,LOW);
  pinMode(Blade_DIR, OUTPUT);
  pinMode(Blade_STEP, OUTPUT);
  pinMode(Blade1_ms3, OUTPUT);
  pinMode(Blade1_ms2, OUTPUT);
  pinMode(Blade1_ms1, OUTPUT);
  pinMode(Blade2_ms3, OUTPUT);
  pinMode(Blade2_ms2, OUTPUT);
  pinMode(Blade2_ms1, OUTPUT);
 
  pinMode(zaxis_DIR, OUTPUT);
  pinMode(zaxis_STEP,OUTPUT);
  pinMode(zaxis1_ms3, OUTPUT);
  pinMode(zaxis1_ms2, OUTPUT);
  pinMode(zaxis1_ms1, OUTPUT);
  pinMode(zaxis2_ms3, OUTPUT);
  pinMode(zaxis2_ms2, OUTPUT);
  pinMode(zaxis2_ms1, OUTPUT);

  pinMode(button, INPUT_PULLUP);
  pinMode(sensor, INPUT_PULLUP);
 
 Serial.begin(9600);
}
 
void loop()
{  
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
   if((value1 == 1) & (value2 == 1) & (value3 == 1)) ///blade going
   {
      order();
   }

 ///원하는 스텝만큼 모터이동하는 함수들
    if(value1 == 7) //7은 blade함수 8은 zaxis함수 9는 piston함수
    {
      Serial.print("blade:"); Serial.print(value3); Serial.println("step");
      blade(value2, value3);
    }
    if(value1 == 8)
    {
      Serial.print("zaxis:"); Serial.print(value3); Serial.println("step");
      zaxis(value2, value3); 
    }
  }
}
 
void blade(int direct, int step) // direct는 방향: 1은 앞으로, 0은 뒤로, step은 모터 step수,
{
    digitalWrite(Blade1_ms3,HIGH);
    digitalWrite(Blade1_ms2,HIGH);
    digitalWrite(Blade1_ms1,HIGH);
    digitalWrite(Blade2_ms3,HIGH);
    digitalWrite(Blade2_ms2,HIGH);
    digitalWrite(Blade2_ms1,HIGH);
  if(direct == 1)
  {
    digitalWrite(Blade_DIR,HIGH);
    for(int i = 0; i < step; i++)
      {
        digitalWrite(Blade_STEP,HIGH);
        delayMicroseconds(1000);
        digitalWrite(Blade_STEP,LOW);
        delayMicroseconds(1000);
      }
  }
  if(direct == 0)
  {
    digitalWrite(Blade_DIR,LOW);
    for(int i = 0; i < step; i++)
      {
        digitalWrite(Blade_STEP,HIGH);
        delayMicroseconds(1000);
        digitalWrite(Blade_STEP,LOW);
        delayMicroseconds(1000);
      }
  }
}
 
void zaxis(int direct, int step) // direct는 방향: 1은 앞으로, 0은 뒤로, step은 모터 step수,
{
    digitalWrite(zaxis1_ms3,HIGH);
    digitalWrite(zaxis1_ms2,HIGH);
    digitalWrite(zaxis1_ms1,HIGH);
    digitalWrite(zaxis2_ms3,HIGH);
    digitalWrite(zaxis2_ms2, HIGH);
    digitalWrite(zaxis2_ms1, HIGH);
  if(direct == 1)
  {
    digitalWrite(zaxis_DIR,HIGH);
    for(int i = 0; i < step; i++)
      {
        digitalWrite(zaxis_STEP,HIGH);
        delayMicroseconds(1000);
        digitalWrite(zaxis_STEP,LOW);
        delayMicroseconds(1000);
      }
  }
  if(direct == 0)
  {
    digitalWrite(zaxis_DIR,LOW);
    for(int i = 0; i < step; i++)
      {
        digitalWrite(zaxis_STEP,HIGH);
        delayMicroseconds(1000);
        digitalWrite(zaxis_STEP,LOW);
        delayMicroseconds(1000);
      }
  }
}
 
void bhoming()
{
  Serial.println("homing-blade");
  digitalWrite(Blade1_ms3,LOW);
  digitalWrite(Blade1_ms2,LOW);
  digitalWrite(Blade1_ms1,LOW);
  digitalWrite(Blade2_ms3,LOW);
  digitalWrite(Blade2_ms2,LOW);
  digitalWrite(Blade2_ms1,LOW);
 
  digitalWrite(Blade_DIR, HIGH);
  
  for(int i = 0; i < 9999999; i++ ) 
  {
    if( digitalRead(button) == HIGH) 
    {
      Serial.println("blade touched");
      blade(0,0);
      break;
    } 
    else 
    {
      digitalWrite(Blade_STEP,HIGH);
      delayMicroseconds(1500);
      digitalWrite(Blade_STEP,LOW);
      delayMicroseconds(1500);
    }
  }
}

///블레이드시작위치로 부터 일정 스텝만큼 뒤로 이동하는 함수
void bgoing()
{
    digitalWrite(Blade1_ms3,HIGH);
    digitalWrite(Blade1_ms2,HIGH);
    digitalWrite(Blade1_ms1,HIGH);
    digitalWrite(Blade2_ms3,HIGH);
    digitalWrite(Blade2_ms2,HIGH);
    digitalWrite(Blade2_ms1,HIGH);

    digitalWrite(Blade_DIR, LOW);
    
  for(int i = 0; i < 20000; i++)
  {
    digitalWrite(Blade_STEP,HIGH);
    delayMicroseconds(500);0,0,
    digitalWrite(Blade_STEP,LOW);
    delayMicroseconds(500);
  }
    for(int i = 0; i < 18000; i++)
  {
    digitalWrite(Blade_STEP,HIGH);
    delayMicroseconds(500);
    digitalWrite(Blade_STEP,LOW);
    delayMicroseconds(500);
  }
}

///z축이 리미트센서에 닿도록 아래로 이동하는 함수
void zhoming()
{
  Serial.println("homing-Z-axis");
  digitalWrite(zaxis1_ms3, HIGH);    
  digitalWrite(zaxis1_ms2, HIGH);
  digitalWrite(zaxis1_ms1, HIGH);
  digitalWrite(zaxis2_ms3, HIGH);
  digitalWrite(zaxis2_ms2, HIGH);
  digitalWrite(zaxis2_ms1, HIGH);   
 
  digitalWrite(zaxis_DIR, LOW);
  
  for(int i = 0; i < 9999999; i++ ) 
  {
    if( digitalRead(sensor) == HIGH ) 
    {
      Serial.println("z-axis sensor touched");
      zaxis(0,0);
      break;
    } 
    else 
    {
      digitalWrite(zaxis_STEP,HIGH);
      delayMicroseconds(1000);
      digitalWrite(zaxis_STEP,LOW);
      delayMicroseconds(1000);
    }
  }
}

///z판이 블레이드 날에 닿도록 일정위치 이동하는 함수 , 25.5mm 이동
void zgoing()
{
  Serial.println("going-Z-axis");
  digitalWrite(zaxis1_ms3, HIGH);    
  digitalWrite(zaxis1_ms2, HIGH);
  digitalWrite(zaxis1_ms1, HIGH);
  digitalWrite(zaxis2_ms3, HIGH);
  digitalWrite(zaxis2_ms2, HIGH);
  digitalWrite(zaxis2_ms1, HIGH);    
 
  digitalWrite(zaxis_DIR, HIGH);
   
  for(int i = 0; i < 21700; i++)
  {
    digitalWrite(zaxis_STEP,HIGH);
    delayMicroseconds(1000);
    digitalWrite(zaxis_STEP,LOW);
    delayMicroseconds(1000);
  }
}

void order()
{
  zaxis(0, 3000);
  delay(15000);
  bhoming();
  zaxis(1, 2940);
  bgoing(); 
}
