#!/usr/bin/env python
# coding: utf-8

# -첫 layer-
# 
# 1. serial16 연결
# 1-1. z축 리미트센서 터치(0,0,1)
# 1-2. z축 블레이드 날이 닿는 위치로 이동(0,1,1)
# 1-3. 닿은 위치에서 일정거리 내리기(8,0,4800) --> 6mm
# 1-4. 블레이드 앞위치로 위치(0,1,1)
# 1-5. 블레이드 (7,0,8000) -->블레이드10mm 뒤로 이동
# 1-6. 시료주입
# 1-7. 블레이드 앞위치로 위치(0,1,1)
# 1-8. 닿은 위치로 일정거리 올리기(8,1,4800) --> 6mm
# 1-9. 블레이딩(0,1,2)
# 2-1. 사진찍기(매크로)
# 2-2. 상태확인 메세지
# 3. com3연결
# 3-1 ok--광경화  // not ok -- 3번으로 돌아가기
# 
# -다음 레이어-
# 
# 1. serial16 연결
# 1-1. 닿은 위치에서 '일정거리 + 경화두께(48step, 0.06mm)' 내리기(8,0,4848) --> 6.06mm
# 1-2. 블레이드 앞위치로 위치(0,1,1)
# 1-3. 블레이드 (7,0,8000) -->블레이드10mm 뒤로 이동
# 1-4. 시료주입
# 1-5. 블레이드 앞위치로 위치(0,1,1)
# 1-6. 닿은 위치로 일정거리 올리기(8,1,4800) --> 6mm
# 1-7. 블레이딩(0,1,2)
# 2-1. 사진찍기(매크로)
# 2-2. 상태확인 메세지
# 3. com3연결
# 3-1. ok--광경화  // not ok -- 3번으로 돌아가기

# In[1]:


#필요한 라이브러리를 import합니다.

#매크로와 알림창을 위한 pyautogui
import pyautogui as pag

#아두이노와 시리얼 통신을 위한 serial
import serial

#시간간격을 두고 함수를 시행하기 위한 time
import time

#강제종료 등 프로그램 명령어 sys
import sys

#시리얼 통신 용 threading
import threading

#프로그램 자동실행을 위한  pywinauto 
import pywinauto 

#커스텀 함수 import as cf
#from DLP_function import * 


# In[2]:


#함수1. 아두이노와 시리얼 통신을 위한 함수, 통신대기 2초
def serial16():
    try:
        global ser16
        ser16 = serial.Serial('COM16', 9600)
        time.sleep(2)
        return "com16과 시리얼통신 성공"
    except serial.SerialException as e:
        print(e)


# In[3]:


#함수1-1. -첫 layer- z축 리미트센서 터치(0,0,1)
def zhoming(ser, exitcode='*'):
    try:
        print(ser.write(b'0,0,1'))
        list = []
        while True:
            data = ser.read().decode('utf-8')
            print(ser.readline().decode('utf-8'))
            list.append(data)
            if exitcode in list:
                return print("done")
            list.clear
            print(list)
    except:
        print("zhoming error")


# In[4]:


#함수1-2. z축 블레이드 날이 닿는 위치로 이동(0,1,1)
def zgoing(ser, exitcode='*'):
    try:
        print(ser.write(b'0,0,2'))
        list = []
        while True:
            data = ser.read().decode('utf-8')
            print(ser.readline().decode('utf-8'))
            list.append(data)
            if exitcode in list:
                return print("done")
            list.clear
            print(list)
    except:
        print("zgoing error")
        


# In[5]:


#함수1-3. 닿은 위치에서 일정거리 내리기(8,0,8000) --> 6mm
def littledown(ser, exitcode='*'):
    try:
        print(ser.write(b'8,0,7000'))
        list = []
        while True:
            data = ser.read().decode('utf-8')
            print(ser.readline().decode('utf-8'))
            list.append(data)
            if exitcode in list:
                return print("done")
            list.clear
            print(list)
    except:
        print("littledown error")


# In[7]:


#함수1-3.5. 닿은 위치에서 일정거리 내리기(8,0,8065) --> 10mm +0.1mm (서포트용)
def thcickdown1(ser, exitcode='*'):
    try:
        print(ser.write(b'8,0,7080'))
        list = []
        while True:
            data = ser.read().decode('utf-8')
            print(ser.readline().decode('utf-8'))
            list.append(data)
            if exitcode in list:
                list.clear
                print(list)
                return print("done")
    except:
        print("thcickdown error")


# In[8]:


#함수1-3.55. 닿은 위치에서 일정거리 내리기(8,0,8048) -->10mm +0.06mm (시편 출력용)
def thcickdown2(ser, exitcode='*'):
    try:
        print(ser.write(b'8,0,7048'))
        list = []
        while True:
            data = ser.read().decode('utf-8')
            print(ser.readline().decode('utf-8'))
            list.append(data)
            if exitcode in list:
                return print("done")
            list.clear
            print(list)
    except:
        print("thcickdown error")


# In[9]:


#함수1-4. 블레이드 앞위치로 위치(0,1,1)
def bhoming(ser, exitcode='*'):
    try:
        print(ser.write(b'0,1,1'))
        list = []
        while True:
            data = ser.read().decode('utf-8')
            print(ser.readline().decode('utf-8'))
            list.append(data)
            if exitcode in list:
                return 
            list.clear
            print(list)
    except:
        print("bhoming error")


# In[10]:


#함수1-5. 블레이드 (7,0,8000) -->블레이드10mm 뒤로 이동
def littleback(ser, exitcode='*'):
    try:
        print(ser.write(b'7,0,7000'))
        list = []
        while True:
            data = ser.read().decode('utf-8')
            print(ser.readline().decode('utf-8'))
            list.append(data)
            if exitcode in list:
                return print("done")
            list.clear
            print(list)
    except:
        print("little back error")


# In[11]:


#함수1-6. 시료주입
def resinshot(ser, exitcode='*'):
    try:
        print(ser.write(b'2,2,2'))
        list = []
        while True:
            data = ser.read().decode('utf-8')
            print(ser.readline().decode('utf-8'))
            list.append(data)
            if exitcode in list:
                return print("done")
            list.clear
            print(list)
    except:
        print("resin shot error")


# In[13]:


#함수1-8. 닿은 위치로 일정거리 올리기(8,1,4800) --> 6mm
def littleup(ser, exitcode='*'):
    try:
        print(ser.write(b'8,1,7000'))
        list = []
        while True:
            data = ser.read().decode('utf-8')
            print(ser.readline().decode('utf-8'))
            list.append(data)
            if exitcode in list:
                return print("done")
            list.clear
            print(list)
    except:
        print("blading error")


# In[14]:


#함수1-9. 블레이딩(0,1,2)
def bgoing(ser, exitcode='*'):
    try:
        print(ser.write(b'0,1,2'))
        list = []
        while True:
            data = ser.read().decode('utf-8')
            print(ser.readline().decode('utf-8'))
            list.append(data)
            if exitcode in list:
                return print("done")
            list.clear
            print(list)

    except:
        print("blading error")


# In[15]:


#함수2-1. 어플키고 사진찍기(매크로)
def picture():
    try:
        pag.moveTo(1825, 820)
        time.sleep(1)
        pag.dragTo(x=1, y=1, duration=0.3)
        time.sleep(1)
        pag.doubleClick(x=1635, y=800)
        print("capture")
    except:
        print("error")


# In[16]:


#함수3-1 ok--광경화  // not ok -- 3번으로 돌아가기
def photo():
    try:
        sel = pag.confirm(text="광조사 가능한 상태?", title="확인", buttons=['ok','nob'])
        if sel == 'ok':
            serial3()
            ser3.write('7\r\n'.encode())
            time.sleep(1)
            ser3.close()
            time.sleep(1)
            serial16()
        elif sel == 'nob':
            print("안타깝군요")


            
    except:
        print("photo error")


# In[17]:


#함수3. com3연결
def serial3():
    global ser3
    try:
        ser3 = serial.Serial('COM3', 9600)
        time.sleep(2)
        return "com3과 시리얼통신 성공"
    except:
        print("please check if ser16 still connected")


# In[18]:


def close3():
    ser3.close()


# In[19]:


def close16():
    ser16.close()


# In[20]:


def openapp():
    app = pywinauto.Application(backend='uia').start("C:\Program Files (x86)\Mirroid\Mirroid.exe")


# In[21]:


def cleaning():
    value = pag.prompt(text='청소하시게요? 얼마나 내릴까요?', title='cleaning', default='please input')
    value = float(value)/1
    down = f'8,0,{value}'
    down = down.encode('utf-8')
    up = f'8,1,{value}'
    up = up.encode('utf-8')
    print(ser16.write(down))
    com = pag.alert(text='청소완료?', title='청소완료?', button='OK')
    if com == 'OK':
        print(ser16.write(up))


# In[22]:


def suppoter(n):
    i=1
    while i<=n:
        thcickdown1(ser16) #서포터 층(0.1mm만큼 더 내리기)
        time.sleep(15)
        bhoming(ser16) #블레이드 호밍
        littleup(ser16) #베드가 날에 닿기
        bgoing(ser16) #블레이딩
        picture() #블레이딩 상태 촬영
        photo() #광 조사 또는 재블레이딩
        print(i, "번째 층 출력완료했습니다.")
        time.sleep(15)
        i+=1


# In[ ]:


def specimen(n):
    i=1
    while i<= n:
        thcickdown2(ser16) #시편층(0.05mm 만큼 더 내리기)
        time.sleep(15)
        resinshot(ser16) #시료 주사
        bhoming(ser16) #블레이드 호밍
        littleup(ser16) #베드가 날에 닿기
        bgoing(ser16) #블레이딩
        picture() #블레이딩 상태 촬영
        photo() #광 조사 또는 재블레이딩
        print(i, "번째 층 출력완료했습니다.")
        i+=1

