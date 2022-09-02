import torchvision.transforms as transforms
import os
from datetime import datetime

def tensor_imshow(tensor):
    # matplotlib는 CPU 기반이므로 CPU로 옮기기
    image = tensor.cpu().clone()

    image = image.squeeze(0)
    # PIL 객체로 변경
    image = transforms.ToPILImage()(image)
    # 이미지를 화면에 출력(matplotlib는 [0, 1] 사이의 값이라고 해도 정상적으로 처리)
    image.show()


classes = ['normal', 'sub_normal', 'critical', 'pore', 'minor_defect']


def makedir(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)
        print('made sub-dir')


def tensor_img_save(tensor, i , e):
    image = tensor.cpu().clone()
    image = image.squeeze(0)
    image = transforms.ToPILImage()(image)
    makedir('C:/jinkyo_coding/DLP_deepLearning/test_value_image/0825ResNet152_IMG')
    image.save(f'C:/jinkyo_coding/DLP_deepLearning/test_value_image/0825ResNet152_IMG/prediction {classes[i]},true {classes[e]}-{datetime.today().strftime("%M%S.%f")}.png')
