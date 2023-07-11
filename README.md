# 딥러닝을 통한 DLP 3D프린터 출력 자동화

해당 내용은 서울과학기술대학교 특수정밀가공 및 생산연구실에서 진행하는 ‘ 세라믹 및 금속 재료의 3D 형상출력을 목적으로 제작된 광경화 타입 3D프린터 제작 및 딥러닝 기술을 기반으로 한 전공정 자동화 ’의 전반적인 기술 및 코드 내용입니다. 


https://user-images.githubusercontent.com/85150616/190361339-f62668f7-aa68-4073-84bd-3492f415d7a6.mp4

[제작된 3D프린터로 세라믹이 출력되는 모습]

## 1. Hardware

3D프린터의 하드웨어는 이전 연구실 연구원들이 제작한 세라믹용 광경화 3D프린터를 조금 더 개선시켜서 진행하였습니다. 자세한 규격 및 형상 정보는 ‘DLP_modeling’ 카테고리에 백업해 놓았습니다.

### 1.1. DLP_modeling

‘DLP_modeling’에서 [0.assembly-MLP_Original.prt](https://github.com/JinkyoJB/DLP_auto/blob/main/DLP_modeling/0.assembly-MLP_Original.prt) 항목은 개선시키기전 기존의 하드웨어의 데이터가 담겨있습니다. 파일형식은 ‘.prt’형식이며 NX Modeling 프로그램으로 제작되었습니다. 기존 DLP프린터 모습은 다음과 같습니다.

![3D프린터-Original](https://user-images.githubusercontent.com/85150616/190361121-0117c724-f518-464e-87e6-159c2f0b06a6.PNG)

[기존 3D프린터 모델링 데이터]

![최종모델링](https://github.com/JinkyoJB/DLP_auto/assets/85150616/225661aa-9097-4f11-bbe2-9b790dc30527)
[최종 3D프린터 모델링 데이터]

[behind modeling]
  
고점도 세라믹 레진을 토출하기 위해 여러 모델링을 실험해 봤습니다.
<br>
1차적으로는 제어하기 쉬운 스텝모터를 이용해 여러 형상으로 토출을 시도해 봤으나 필요압력이 높아 구조물이 외압을 버티기 힘들어 3차 시도 끝에 공압기로 압력을 가해 토출하는 방식을 차용했습니다.

![시료주사기](https://github.com/JinkyoJB/DLP_auto/assets/85150616/81f908d7-b5df-4674-a14d-b1e2606ae90b)

사용된 시료 주사기는 250ml 공업용 주사기에 3D프린터 및 o-ring으로 커스텀하여 사용하였습니다.

### 1.2. DLP_arduino
![모터사양](https://github.com/JinkyoJB/DLP_auto/assets/85150616/7b37ed0c-1cc7-4d04-a820-3659f3038f4d)

아두이노는 시리얼 통신을 통해 말단의 모터,센서를 제어하며 컴퓨터의 GUI명령 또한 시리얼 통신으로 입력받습니다. 모터의 동작은 비동기방식이여야 하므로 일정 동작이 끝난 뒤, 아두이노는 '*'과 같은 특정 시그널을 통해 동작의 끝남을 컴퓨터에게 알리는 방식을 차용하였습니다.

### 1.3 블레이드 히팅

세라믹의 점도 및 흐름성은 온도에 반비례하는 특성을 지니므로 고점도 세라믹을 도포 시 40-70도의 블레이드가 필요합니다. 
![image](https://github.com/JinkyoJB/DLP_auto/assets/85150616/c7f71921-4a4c-4389-809c-38c307e3b3d1)
따라서 모델링 및 가공하여 블레이드 양측에 열봉이 1개씩 삽입되고 중앙에 온도센서를 부착함으로써 히팅 블레이드를 적용했습니다.

### 1.4 flow-chart 및 diagram
![figure7](https://github.com/JinkyoJB/DLP_auto/assets/85150616/76975f1e-7250-40cc-8057-768efe1efead)
![figure4](https://github.com/JinkyoJB/DLP_auto/assets/85150616/e84d451b-f473-4da6-96c7-77da7228ad32)
![image](https://github.com/JinkyoJB/DLP_auto/assets/85150616/8392bfe0-ec14-49a5-b94c-292bb50f915d)


---
## 2. Software

![화면 캡처 2023-07-11 131624](https://github.com/JinkyoJB/DLP_auto/assets/85150616/13b66011-cf88-46b0-a97d-206ebcadeb8b)
3D프린터와 연결된 컴퓨터 화면에서는 위 이미지와 같은 화면을 볼 수 있습니다.
<br>
![image](https://github.com/JinkyoJB/DLP_auto/assets/85150616/3d5dbf48-469b-4432-98e3-5e1a2f96d043)

좌측 프로그램은 광원인 DLP 제어 프로그램이며, 중간은 3D프린터를 제어하기 위해 파이썬으로 자체 제작한 프로그램입니다. 해당 GUI를 통해 DLP에 input될 이미지, 광파워, 노광 시간, 3D프린터의 모터,센서를 조절할 수 있습니다. 또한 AI모드 출력 명령 버튼을 누르면 densenet을 적용하여 세라믹 표면에 결점이 발견 될 시 자동 재 블레이딩 및 블레이드 온도를 높이는 등의 폐루프 시스템을 적용할 수 있습니다.
맨 우측은 표면 결점을 검출하기 위해서 3D프린터 윗면에 달아둔 안드로이드기기를 통해 보여지는 이미지를 상시로 확인 할 수 있습니다. 안드로이드 연결은 파이썬을 이용해 ADB서버를 통해 통신합니다.

## 3. Deep learning

### 3.1. DLP_dataset
데이터셋은 2021.10.07~2022.02.23까지 실험 중 촬용된 세라믹 도표면 사진을 바탕으로 구성되었습니다.
![image](https://github.com/JinkyoJB/DLP_auto/assets/85150616/ebb91870-656c-4c79-95e9-7ff584c73bb4)
정상상태(Normal)와 출력 중 빈번한 결함들로 분류했으며, 기계 자체적으로 조치를 취할 수 있는 상태인 미미한 결함(Minor defect)과 기공 상태(Pore), 적층이 아예 불가능한 심각한 상태(Critical) 및 기계오류 문제(Error) 로 총 5가지의 유형으로 분류했습니다.

### 3.2. DLP_data_augmentation
![table2](https://github.com/JinkyoJB/DLP_auto/assets/85150616/19a08ecb-c751-4d13-847c-f3238acf2dee)
데이터셋의 정확도를 높이기 위해 원본 이미지에 적절한 변형을 가해서 학습데이터셋의 규모를 인위적으로 증대하는 augmentation 기법을 적용했습니다. 각 분류의 데이터셋 양을 비슷하게 조절하고 각 가중치를 비슷하게 학습하여 정규화 및 과적합을 줄였으며, 종류는 기본적인 좌우반전, 상하반전, 랜덤위치합성 3가지를 적용했습니다. Augmentation을 적용한 최종 개수의 전체비율이 25%내외가 되도록 하여 가중치를 비슷하게 학습하도록 적용하였습니다.
![figure13](https://github.com/JinkyoJB/DLP_auto/assets/85150616/e4810988-5412-438d-9f81-365102a96a71)
이 외에도 세라믹 도표면은 광경화 반응이 일어 날 수 있도록 회백색인 경우가 많은데 이는 RGB의 값이 (255,255,255)로 편중되어 있음을 말합니다. 따라서 RGB픽셀값 표준화를 적용하여 주변 픽셀 대비 연산 픽셀의 RGB값의 변화가 더 쉽게 인식될 수 있도록 하여 학습 효율을 높였습니다. RGB평균값은 [0.485,0.456,0.406], 표준편차는 [0.229,0.224,0.225]를 적용하였으며, 적용된 최종 입력데이터의 이미지는 위 사진과 같습니다. 적용 후 보통 3%정도의 성능 향상을 확인했습니다.

### 3.3. DLP_deepLearning

![image](https://github.com/JinkyoJB/DLP_auto/assets/85150616/1822307b-d719-4170-afff-95a16d268d74)
준비된 데이터셋을 저명한 이미지 알고리즘에 파인 튜닝하여 적용해 본 결과, 어느정도 saturation된 결과값이 나온 것을 확인 할 수 있었습니다. 특히 denseNet에서 좋은 성능지표를 보여 해당 모델의 하이퍼파라미터를 optimization하여 3D프린터에 적용하였습니다.

---

### 결과
![image](https://github.com/JinkyoJB/DLP_auto/assets/85150616/14204e1a-42d2-4f73-982e-01b5b90a408f)
이렇게 폐루프 시스템으로 동작하는 세라믹 3D프린터의 출력 결과물입니다. 딥러닝을 통해 결함을 검출함으로써 sintered body에서도 정밀하고 적은 크랙을 관찰할 수 있었습니다.

### 3.4. DLP_yolo5(testing)
현재는 도포 과정이 아닌 전과정에서 일어날 수 있는 결함을 yolo5로 관측하기 위해 test 중입니다.
