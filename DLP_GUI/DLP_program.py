import threading
import time

import natsort
import pywinauto
import pygetwindow as gw
import pyautogui as pag

from common_func import *


#  프로그램 열기
def dlp_program_open():
    try:
        win = gw.getWindowsWithTitle('Full-HD UV LE Controller v2.3')[0]
        win.moveTo(-6, 0)
    except:
        pywinauto.application.Application().start("C:/jinkyo_coding/DLP_GUI/LED_Controller.exe").top_window().set_focus()
        win = gw.getWindowsWithTitle('Full-HD UV LE Controller v2.3')[0]
        win.moveTo(-6, 0)
        pag.click(211, 80)  # nvr창 활성화
        time.sleep(0.5)
        pag.click(190, 126)  # nvr선택
        time.sleep(0.5)
        pag.click(45, 114)  # project on 선택
        time.sleep(2)
        pag.hotkey('enter')


# 이미지 띄우는 함수
def image(folder, pic_num, sec):
    cv2_sec = int((float(sec+2))*1000)
    pre_file_list = os.listdir(folder)
    file_list = natsort.natsorted(pre_file_list)  # 이미지 파일 순서대로 정렬

    file_type1 = ".jpg"
    file_type2 = ".png"
    img_files = [file for file in file_list if file.endswith(f'{file_type1}') or file.endswith(f'{file_type2}')]

    while True:
        if pic_num >= len(img_files):
            print("이미지 끝")
            sub_image()

        img = cv2.imread(f'{folder}/{img_files[pic_num]}')

        # 예외처리
        if img is None:
            print("이미지를 불러오는데 실패했습니다.")
            sub_image()
        # 창만들기
        cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        cv2.moveWindow('image', 1920, 0)  # 창 위치 변경
        cv2.setWindowProperty('image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        cv2.imshow('image', img)
        th1 = threading.Thread(target=pag_i2c, args=(sec,))
        th1.start()

        if cv2.waitKey(cv2_sec) == -1:
            break
    cv2.destroyAllWindows()

def pag_i2c(sec):
    win = gw.getWindowsWithTitle('Full-HD UV LE Controller v2.3')[0]
    win.activate()
    time.sleep(1)
    pag.click(104, 220)
    time.sleep(sec)
    pag.click(170, 220)
    return



def sub_image():
    black_numpy = np.zeros([960, 540, 1])
    # 창만들기
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.moveWindow('image', 1920, 0)  # 창 위치 변경
    cv2.setWindowProperty('image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    cv2.imshow('image', black_numpy)

# 마우스 위치 확인 코드
# while True:
#     print(pag.position())








