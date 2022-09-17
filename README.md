# 딥러닝을 통한 DLP 3D프린터 출력 자동화

해당 내용은 서울과학기술대학교 특수정밀가공 및 생산연구실에서 진행하는 ‘ 세라믹 및 금속 재료의 3D 형상출력을 목적으로 제작된 광경화 타입 3D프린터 제작 및 딥러닝 기술을 기반으로 한 전공정 자동화 ’의 전반적인 기술 및 코드 내용입니다. 


https://user-images.githubusercontent.com/85150616/190361339-f62668f7-aa68-4073-84bd-3492f415d7a6.mp4

[제작된 3D프린터로 세라믹이 출력되는 모습]

## 1. Hardware

3D프린터의 하드웨어는 이전 연구실 연구원들이 제작한 세라믹용 광경화 3D프린터를 조금 더 개선시켜서 진행하였습니다. 자세한 규격 및 형상 정보는 ‘DLP_modeling’ 카테고리에 백업해 놓았습니다.

### 1.1. DLP_modeling

‘DLP_modeling’에서 [0.assembly-MLP_Original.prt](https://github.com/JinkyoJB/DLP_auto/blob/main/DLP_modeling/0.assembly-MLP_Original.prt) 항목은 개선시키기전 기존의 하드웨어의 데이터가 담겨있습니다. 파일형식은 ‘.prt’형식이며 NX Modeling 프로그램으로 제작되었습니다. 기존 DLP프린터 모습은 다음과 같습니다.

![3D프린터-Original](https://user-images.githubusercontent.com/85150616/190361121-0117c724-f518-464e-87e6-159c2f0b06a6.PNG)

기존 3D프린터 모델링 데이터

## 2. Connection & Communication

![gui](https://user-images.githubusercontent.com/85150616/190361170-b48bb2d1-7426-4bdf-b49c-028ab956ea0a.png)

### 2.1. DLP_arduino

## 3. Software

### 3.1. DLP_GUI

## 4. Deep learning

### 4.1. DLP_dataset

### 4.2. DLP_data_augmentation

### 4.3. DLP_deepLearning

### 4.4. DLP_yolo5(testing)
