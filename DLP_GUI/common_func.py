import os
import cv2
import time
import numpy as np
from ppadb.client import Client as AdbClient

import torch
import torch.nn as nn

import torchvision.transforms as transforms
import torchvision.models as models

import serial
import re
import pyautogui as pag
import threading

class block(nn.Module):
    def __init__(self, in_channels, out_channels, identity_downsample=None, stride=1):
        super(block, self).__init__()
        self.expansion = 4
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=1, padding=0)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3, stride=stride, padding=1)
        self.bn2 = nn.BatchNorm2d(out_channels)
        self.conv3 = nn.Conv2d(out_channels, out_channels * self.expansion, kernel_size=1, stride=1, padding=0)
        self.bn3 = nn.BatchNorm2d(out_channels * self.expansion)
        self.relu = nn.ReLU()
        self.identity_downsample = identity_downsample

    def forward(self, x):
        identity = x

        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.conv2(x)
        x = self.bn2(x)
        x = self.relu(x)
        x = self.conv3(x)
        x = self.bn3(x)

        if self.identity_downsample is not None:
            identity = self.identity_downsample(identity)
        x += identity
        x = self.relu(x)
        return x


class ResNet(nn.Module):
    def __init__(self, block, layers, image_channels, num_classes):
        super(ResNet, self).__init__()
        self.in_channels = 64
        self.conv1 = nn.Conv2d(image_channels, 64, kernel_size=7, stride=2, padding=3)
        self.bn1 = nn.BatchNorm2d(64)
        self.relu = nn.ReLU()
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
        self.layer1 = self._make_layer(block, layers[0], out_channels=64, stride=1)
        self.layer2 = self._make_layer(block, layers[1], out_channels=128, stride=2)
        self.layer3 = self._make_layer(block, layers[2], out_channels=256, stride=2)
        self.layer4 = self._make_layer(block, layers[3], out_channels=512, stride=2)

        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(512 * 4, num_classes)

    def forward(self, x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)

        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)

        x = self.avgpool(x)
        x = x.reshape(x.shape[0], -1)
        x = self.fc(x)
        return x

    def _make_layer(self, block, num_residual_blocks, out_channels, stride):
        identity_downsample = None
        layers = []

        if stride != 1 or self.in_channels != out_channels * 4:
            identity_downsample = nn.Sequential(nn.Conv2d(self.in_channels, out_channels * 4, kernel_size=1,
                                                          stride=stride), nn.BatchNorm2d(out_channels * 4))

        layers.append(block(self.in_channels, out_channels, identity_downsample, stride))
        self.in_channels = out_channels * 4

        for i in range(num_residual_blocks - 1):
            layers.append(block(self.in_channels, out_channels))

        return nn.Sequential(*layers)


def ResNet50(img_channels=3, num_classes=5):
    return ResNet(block, [3, 4, 6, 3], img_channels, num_classes)


def ResNet101(img_channels=3, num_classes=5):
    return ResNet(block, [3, 4, 23, 3], img_channels, num_classes)


def ResNet152(img_channels=3, num_classes=5):
    return ResNet(block, [3, 8, 36, 3], img_channels, num_classes)



def makedir(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)
        print('made sub-dir')


def cv_show(target_img, **kwargs):
    cv_x = kwargs.get("cv_x", 504)
    cv_y = kwargs.get("cv_y", 672)
    try:
        if type(target_img) == np.ndarray:
            cv2.namedWindow('show_img', cv2.WINDOW_NORMAL)
            cv2.imshow('show_img', target_img)
            cv2.resizeWindow('show_img', cv_x, cv_y)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            cv2.namedWindow('show_img', cv2.WINDOW_NORMAL)
            cv2.imshow('show_img', cv2.imread(target_img))
            cv2.resizeWindow('show_img', cv_x, cv_y)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    except:
        return "이미지 입력 오류"

class processing:
    def __init__(self, **kwargs):
        self.guide_address = kwargs.get("guide_address")
        self.y = kwargs.get("y")
        self.yh = kwargs.get("yh")
        self.x = kwargs.get("x")
        self.xw = kwargs.get("xw")
        self.thresh = kwargs.get("thresh")
        self.max_area = kwargs.get("max_area")

        self.now = time.strftime('%y%m%d')
        self.now_time = time.strftime('%H%M%S')

        self.img = cv2.imread(self.guide_address)

    def contour_show(self):
        self.img_cut = self.img[self.y:self.yh, self.x:self.xw]
        self.gray = cv2.cvtColor(self.img_cut, cv2.COLOR_BGR2GRAY)
        self.thresh_value = int(np.mean(self.gray)) / self.thresh

        ret, self.thresh_sh = cv2.threshold(self.gray, self.thresh_value, 255, cv2.THRESH_BINARY)
        self.binary = cv2.bitwise_not(self.thresh_sh)
        self.contours, _ = cv2.findContours(self.binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.guideline_mask = cv2.drawContours(self.img_cut, self.contours, -1, (0, 0, 255), 15)

        self.index = len(self.contours)
        self.contour_list = []
        for i in range(self.index):
            if cv2.contourArea(self.contours[i]) > self.max_area:
                self.contour_list.append(i)

        cv_show(self.guideline_mask, cv_x=550, cv_y=300)

        return len(self.contour_list)

    """
    lastpic_cropping는 안드로이드에서 제일 최신 사진을 가져와서 crop한 후 dlp_temp에 저장,크롭이미지를 리스트로 반환
    """

    def lastpic_cropping(self):
        client = AdbClient(host="127.0.0.1", port=5037)
        devices = client.devices()
        device = devices[0]
        self.img_cut = self.img[self.y:self.yh, self.x:self.xw]
        self.gray = cv2.cvtColor(self.img_cut, cv2.COLOR_BGR2GRAY)
        self.thresh_value = int(np.mean(self.gray)) / self.thresh

        ret, self.thresh_sh = cv2.threshold(self.gray, self.thresh_value, 255, cv2.THRESH_BINARY)
        self.binary = cv2.bitwise_not(self.thresh_sh)
        self.contours, _ = cv2.findContours(self.binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.index = len(self.contours)
        self.contour_list = []
        for i in range(self.index):
            if cv2.contourArea(self.contours[i]) > self.max_area:
                self.contour_list.append(i)

        self.min_x_list = []
        self.min_y_list = []
        self.max_x_list = []
        self.max_y_list = []

        for i in self.contour_list:
            self.contour = np.array(self.contours[i])

            self.min_v = np.min(self.contour, axis=0)
            self.min_x = self.min_v[0][0]
            self.min_y = self.min_v[0][1]
            self.min_x_list.append(self.min_x)
            self.min_y_list.append(self.min_y)

            self.max_v = np.max(self.contour, axis=0)
            self.max_x = self.max_v[0][0]
            self.max_y = self.max_v[0][1]
            self.max_x_list.append(self.max_x)
            self.max_y_list.append(self.max_y)

        self.file_listing = device.shell("ls -p /sdcard/DCIM/Camera/").split('  ')
        self.file_list = []
        for i in self.file_listing:
            i = i.strip('\n')
            if i != '':
                self.file_list.append(i)
        self.file_list = sorted(self.file_list)
        self.file_name = self.file_list[-1]
        self.img_dir = f"/sdcard/DCIM/Camera/{self.file_name}"

        self.base_folder = "./DLP_temp/"
        self.folder_name = f"{self.base_folder}{self.now}{self.now_time}"
        makedir(self.folder_name)
        print(self.folder_name)
        device.pull(self.img_dir, f"{self.folder_name}/{self.file_name}")

        self.picture = cv2.imread(f"{self.folder_name}/{self.file_name}")
        self.picture = self.picture[self.y:self.yh, self.x:self.xw]

        self.picture_list = []

        for i in range(len(self.contour_list)):
            self.crop = self.picture[self.min_y_list[i]:self.max_y_list[i], self.min_x_list[i]:self.max_x_list[i]]
            self.crop = cv2.resize(self.crop, (512, 512), interpolation=cv2.INTER_AREA)
            cv2.imwrite(f'{self.folder_name}/{self.now_time}_{i + 1}.jpg', self.crop)
            self.picture_list.append(self.crop)

        return self.picture_list


def classify(picture_list):
    classes = ["normal", "critical", "error", "pore", "minor_defect"]
    trans = transforms.Compose(
        [transforms.ToTensor(),transforms.Resize(224), transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))])
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    class_value_list = []

    # densenet = models.densenet161()
    # densenet.classifier = nn.Linear(in_features=2208, out_features=5, bias=True)
    # densenet.to(device)
    #
    resnet152 = ResNet152().to(device)

    googlenet = models.googlenet(num_classes=5, init_weights=True).to(device)
    # alexnet = models.alexnet()
    criterion = nn.CrossEntropyLoss()
    # optimizer = optim.SGD(alexnet.parameters(), lr=0.0001, momentum=0.9, weight_decay=0.0005)
    # alexnet.fc = nn.Linear(in_features=4096, out_features=5, bias=True)

    path = 'C:/jinkyo_coding/DLP_deepLearning/0511_ResNet152(100)80.0001.pth'
    resnet152.load_state_dict(torch.load(path))
    # googlenet.load_state_dict(torch.load(path))
    # densenet.load_state_dict(torch.load(path))

    for i in picture_list:
        outputs = resnet152(trans(i).unsqueeze(0).to(device))  # resnet용
        _, predictions = outputs.max(1)  # resnet용
        class_value_list.append(classes[predictions])  # resnet용
        # outputs = googlenet(trans(i).unsqueeze(0).to(device))  # googlenet용
        # _, predictions = outputs.logits.max(1)  # googlenet용
        # class_value_list.append(classes[predictions])  # googlenet용

    return class_value_list


