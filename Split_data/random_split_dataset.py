import os
import shutil
import random


def make_dir(path):
    os.mkdir(path)


def split_data(image_path, mask_path, train_img_path, val_img_path, train_mask_path, val_mask_path):
    filenames = os.listdir(image_path)  # 读取nii文件夹
    number = len(filenames)-2

    c = range(number)
    indexs = random.sample(c, 50)
    for i in indexs:
        name = filenames[i]
        shutil.move(os.path.join(image_path, name), os.path.join(val_img_path, name))
        mask_name = filenames[i].replace('dwi', 'msk')
        shutil.move(os.path.join(mask_path, mask_name), os.path.join(val_mask_path, mask_name))


if __name__ == '__main__':
    image_path = r'G:\DWI\MICCAI\MICCAI_2022\Stroke\images'
    mask_path = r'G:\DWI\MICCAI\MICCAI_2022\Stroke\labels'

    train_img_path = os.path.join(image_path, 'train_img')
    val_img_path = os.path.join(image_path, 'val_img')

    train_mask_path = os.path.join(mask_path, 'train_mask')
    val_mask_path = os.path.join(mask_path, 'val_mask')

    # 判断是否包含文件夹
    if os.path.isdir(train_img_path) == False:
        make_dir(train_img_path)
    else:
        shutil.rmtree(train_img_path)
        make_dir(train_img_path)

    if os.path.isdir(val_img_path) == False:
        make_dir(val_img_path)
    else:
        shutil.rmtree(val_img_path)
        make_dir(val_img_path)

    if os.path.isdir(train_mask_path) == False:
        make_dir(train_mask_path)
    else:
        shutil.rmtree(train_mask_path)
        make_dir(train_mask_path)

    if os.path.isdir(val_mask_path) == False:
        make_dir(val_mask_path)
    else:
        shutil.rmtree(val_mask_path)
        make_dir(val_mask_path)

    # 随机挑选
    split_data(image_path, mask_path, train_img_path, val_img_path, train_mask_path, val_mask_path)

