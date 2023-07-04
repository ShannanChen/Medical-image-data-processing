import numpy as np
import os #遍历文件夹
import nibabel as nib
import imageio #转换成图像
import SimpleITK as sitk

import cv2


def get_largest_slice(image):
    """
    获取 3D 图像的最大层面
    """
    largest_slice = None
    largest_slice_area = 0
    for z in range(image.shape[0]):
        slice_area = cv2.countNonZero(image[z, :, :])
        if slice_area > largest_slice_area:
            largest_slice_area = slice_area
            largest_slice = image[z, :, :]
            image_area = image[z, :, :].shape[0] * image[z, :, :].shape[1]
            area_ratio = (slice_area / image_area) * 100
            print(area_ratio)
    return largest_slice


def nii_to_image(niifile):

    img = sitk.ReadImage(niifile)
    img_array = sitk.GetArrayFromImage(img)

    largest_slice = get_largest_slice(img_array)
    largest_slice = cv2.cvtColor(largest_slice, cv2.COLOR_GRAY2BGR)

    image_name = 'aaa'
    save_name = os.path.join(imgfile, f"{image_name}.bmp")
    cv2.imwrite(save_name, largest_slice)

if __name__ == '__main__':
    str = r'C:\Users\Administrator\Desktop\2 _OAx_Prop_T2_PWMV_0.nii.gz'
    # str = r'C:\Users\Administrator\Desktop\2 _OAx_Prop_T2_src.nii.gz'
    filepath = str
    imgfile = r'C:\Users\Administrator\Desktop\1'
    nii_to_image(filepath)