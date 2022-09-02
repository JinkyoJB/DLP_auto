import cv2
import os
import time
import numpy as np

def cv_show(guideline_img):
    cv2.namedWindow('guideline_img',cv2.WINDOW_NORMAL)
    cv2.imshow('guideline_img',guideline_img)
    cv2.resizeWindow('guideline_img', 403, 302)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def makedir(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)
        print('made sub-dir')


def flipping(file_dir):
    for (path,dirs,files) in os.walk(file_dir):
        for file in files:
            print(file)
            file_ad = file_dir + '/' + file
            file_bgr = cv2.imread(file_ad)
            LR_flip = cv2.flip(file_bgr, 1) # 1은 좌우 반전, 0은 상하 반전입니다.
            UD_flip = cv2.flip(file_bgr, 0)
            
            makedir(file_dir+'/'+'LR_flipped')
            cv2.imwrite(f'{file_dir}/LR_flipped/{file[:-4]}_LR.jpg',LR_flip)
            
            makedir(file_dir+'/'+'UD_flipped')
            cv2.imwrite(f'{file_dir}/UD_flipped/{file[:-4]}_UD.jpg',UD_flip)