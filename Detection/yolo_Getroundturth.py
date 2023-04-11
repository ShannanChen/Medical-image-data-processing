import os
import numpy as np
from PIL import Image
import SimpleITK as sitk
import cv2

# 输出成图片查看得到boundingbox效果
imagedir = r'C:\Users\Administrator\Desktop\1'

filenames = os.listdir(imagedir)  # 读取nii文件
for file_name in filenames:
    img_path = os.path.join(imagedir, file_name)
    if file_name.split('.')[-1] == 'bmp':
        # image = sitk.ReadImage(img_path)
        # image = sitk.GetArrayFromImage(image)
        image = cv2.imread(img_path)
        file_name_txt = file_name.split('.')[0] + '.txt'
        file_name_new = file_name.split('.')[0] + '.jpg'
        img_tmp = image.copy()
        if os.path.isfile(os.path.join(imagedir, file_name_txt)):
            with open(os.path.join(imagedir, file_name_txt), 'r') as fr:
                i = 0  # 保存的是需要画的框的个数
                labelList = fr.readlines()
                for label in labelList:
                    label = label.strip().split()
                    # convert x,y,w,h to x1,y1,x2,y2
                    H, W, _ = image.shape
                    x1 = int((float(label[1]) - float(label[3]) / 2) * W)  # x_center - width/2
                    y1 = int((float(label[2]) - float(label[4]) / 2) * H)  # y_center - height/2
                    x2 = int((float(label[1]) + float(label[3]) / 2) * W)  # x_center + width/2
                    y2 = int((float(label[2]) + float(label[4]) / 2) * H)  # y_center + height/2

                    start_point, end_point = (x1, y1), (x2, y2)

                    color = (0, 0, 255)  # Red color in BGR；红色：rgb(255,0,0)
                    thickness = 1  # Line thickness

                    mask_bboxs = cv2.rectangle(img_tmp, start_point, end_point, color, thickness)

                cv2.imwrite(os.path.join(imagedir, file_name_new), mask_bboxs)


