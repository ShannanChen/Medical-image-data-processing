import os
import sys
import SimpleITK as sitk
from pathlib import Path

# 设置UTF-8编码，避免中文路径问题
if sys.platform.startswith('win'):
    import locale
    locale.setlocale(locale.LC_ALL, 'C')


def resample_image_to_spacing(image, new_spacing=(3.0, 3.0, 3.0)):
    """
    将图像重采样到指定的spacing
    
    参数:
        image: SimpleITK图像对象
        new_spacing: 目标spacing，默认为(3.0, 3.0, 3.0)
    
    返回:
        重采样后的SimpleITK图像对象
    """
    # 获取原始spacing和size
    original_spacing = image.GetSpacing()
    original_size = image.GetSize()
    
    # 计算新的size，保持物理空间大小不变
    new_size = [
        int(round(original_size[0] * (original_spacing[0] / new_spacing[0]))),
        int(round(original_size[1] * (original_spacing[1] / new_spacing[1]))),
        int(round(original_size[2] * (original_spacing[2] / new_spacing[2])))
    ]
    
    # 创建重采样滤波器
    resample = sitk.ResampleImageFilter()
    resample.SetOutputSpacing(new_spacing)
    resample.SetSize(new_size)
    resample.SetOutputDirection(image.GetDirection())
    resample.SetOutputOrigin(image.GetOrigin())
    resample.SetTransform(sitk.Transform())
    resample.SetDefaultPixelValue(0)
    
    # 根据图像类型选择插值方法
    # 对于标签图像使用最近邻插值，对于普通图像使用线性插值
    resample.SetInterpolator(sitk.sitkLinear)
    
    # 执行重采样
    resampled_image = resample.Execute(image)
    
    return resampled_image


def process_nii_files(root_path, target_spacing=(3.0, 3.0, 3.0)):
    """
    遍历指定路径下的所有文件夹，找到所有nii.gz文件并重采样
    
    参数:
        root_path: 根目录路径
        target_spacing: 目标spacing，默认为(3.0, 3.0, 3.0)
    """
    root_path = Path(root_path)
    
    print(f"检查路径: {root_path}")
    print(f"路径是否存在: {root_path.exists()}")
    print(f"路径绝对路径: {root_path.absolute()}")
    
    if not root_path.exists():
        print(f"❌ 错误：路径 {root_path} 不存在！")
        return
    
    # 查找所有的.nii.gz文件
    nii_files = list(root_path.rglob('*.nii.gz'))
    
    if not nii_files:
        print(f"在路径 {root_path} 下没有找到任何.nii.gz文件")
        return
    
    print(f"找到 {len(nii_files)} 个.nii.gz文件")
    print(f"目标spacing: {target_spacing}")
    print("-" * 60)
    
    # 处理每个文件
    for idx, file_path in enumerate(nii_files, 1):
        try:
            print(f"[{idx}/{len(nii_files)}] 处理文件: {file_path.name}")
            
            # 读取图像
            # 使用pathlib的绝对路径字符串，更好地处理中文路径
            image = sitk.ReadImage(str(file_path.absolute()))
            original_spacing = image.GetSpacing()
            original_size = image.GetSize()
            
            print(f"  原始spacing: {original_spacing}")
            print(f"  原始size: {original_size}")
            
            # 检查是否已经是目标spacing
            if all(abs(original_spacing[i] - target_spacing[i]) < 0.01 for i in range(3)):
                print(f"  ✓ 已经是目标spacing，跳过")
                continue
            
            # 重采样
            resampled_image = resample_image_to_spacing(image, target_spacing)
            new_size = resampled_image.GetSize()
            
            print(f"  新spacing: {resampled_image.GetSpacing()}")
            print(f"  新size: {new_size}")
            
            # 保存并替换原文件
            sitk.WriteImage(resampled_image, str(file_path.absolute()))
            print(f"  ✓ 已保存并替换原文件")
            
        except Exception as e:
            print(f"  ✗ 处理失败: {type(e).__name__}: {str(e)}")
            print(f"  文件路径: {file_path}")
            import traceback
            print(f"  详细错误: {traceback.format_exc()}")
            continue
        
        print("-" * 60)
    
    print(f"\n完成！共处理 {len(nii_files)} 个文件")


if __name__ == "__main__":
    # 设置根目录路径（请修改为您的实际路径）
    root_directory = r"F:\Dataset\tamplate\333"  # 修改为您的路径
    
    # 设置目标spacing
    target_spacing = (3.0, 3.0, 3.0)
    
    # 执行处理
    process_nii_files(root_directory, target_spacing)

