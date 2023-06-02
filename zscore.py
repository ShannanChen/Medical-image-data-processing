import numpy as np
import os
import SimpleITK as sitk
import tqdm


def get_listdir(path):
    tmp_list = []
    for file in os.listdir(path):
        if os.path.splitext(file)[1] == '.gz':
            file_path = os.path.join(path, file)
            tmp_list.append(file_path)
    return tmp_list


def zscore(img_path):
    sitk_img = sitk.ReadImage(img_path)
    img_arr = sitk.GetArrayFromImage(sitk_img)
    new_arr = (img_arr - np.mean(img_arr)) / np.std(img_arr)
    new_img = sitk.GetImageFromArray(new_arr)
    new_img.SetDirection(sitk_img.GetDirection())
    new_img.SetOrigin(sitk_img.GetOrigin())
    new_img.SetSpacing(sitk_img.GetSpacing())
    sitk.WriteImage(new_img, img_path)


if __name__ == '__main__':
    img_path = r'../mydata/train_nii'
    # img_path = r'../mydata/test_nii'
    name_list = os.listdir(img_path)
    name_list.sort()
    for name in tqdm.tqdm(name_list):
        img_list = get_listdir(os.path.join(img_path, name))
        for i in img_list:
            zscore(i)
