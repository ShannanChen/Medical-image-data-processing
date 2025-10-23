import os
from pathlib import Path
import nibabel as nib
import sys


def convert_nii_to_niigz(folder_path):
    """
    Converts all .nii files in a specified folder to .nii.gz files
    and deletes the original .nii file upon successful conversion.

    Args:
        folder_path (str or Path): The path to the folder containing .nii files.
    """

    # 1. 将输入路径转换为 Path 对象，以便更方便地操作
    p = Path(folder_path)

    # 2. 检查路径是否存在且是否是一个文件夹
    if not p.is_dir():
        print(f"错误: 提供的路径 '{folder_path}' 不是一个有效的文件夹。")
        return

    print(f"开始扫描文件夹: {p.resolve()}")

    # 3. 搜索所有 .nii 文件 (使用 .glob)
    #    注意：glob 区分大小写，如果需要不区分大小写，可能需要更复杂的逻辑
    #    这里我们只查找小写的 .nii
    nii_files = list(p.glob('*.nii'))

    if not nii_files:
        print("在文件夹中未找到 .nii 文件。")
        return

    print(f"找到了 {len(nii_files)} 个 .nii 文件。开始转换...")
    print("-" * 30)

    # 4. 遍历并处理每个文件
    success_count = 0
    fail_count = 0

    for nii_file_path in nii_files:
        # 5. 定义输出的 .nii.gz 文件路径
        #    nii_file_path.with_suffix('.nii.gz') 会将 'file.nii' 变为 'file.nii.gz'
        gz_file_path = nii_file_path.with_suffix('.nii.gz')

        print(f"处理中: {nii_file_path.name}")

        try:
            # 6. 检查 .nii.gz 文件是否已存在
            if gz_file_path.exists():
                print(f"  跳过: {gz_file_path.name} 已存在。")
                # 如果 .gz 文件已存在，我们也可以选择删除 .nii 文件
                # print(f"  删除原始文件: {nii_file_path.name}")
                # nii_file_path.unlink() # 取消注释此行以删除
                continue

            # 7. 加载 .nii 文件
            print("  加载中...")
            img = nib.load(nii_file_path)

            # 8. 保存为 .nii.gz 文件 (nibabel 会自动处理压缩)
            print(f"  保存为: {gz_file_path.name}")
            nib.save(img, gz_file_path)

            # 9. 确认 .gz 文件已创建
            if gz_file_path.exists():
                print("  保存成功。")
                # 10. 删除原始的 .nii 文件
                print(f"  删除原始文件: {nii_file_path.name}")
                nii_file_path.unlink()  # unlink() 是 pathlib 中删除文件的方法
                success_count += 1
            else:
                print(f"  错误: 保存后未找到 {gz_file_path.name}。")
                fail_count += 1

        except Exception as e:
            print(f"  处理 {nii_file_path.name} 时发生错误: {e}")
            fail_count += 1

        print("-" * 20)  # 添加分隔符

    print("-" * 30)
    print("转换完成。")
    print(f"成功转换并删除 {success_count} 个文件。")
    print(f"失败 {fail_count} 个文件。")


# --- 如何使用 ---
if __name__ == "__main__":

    FOLDER_TO_PROCESS = r"F:\Dataset\南京大学\姜医生PWI分割\pwi1004\Tmaxroi"

    # 运行转换函数
    convert_nii_to_niigz(FOLDER_TO_PROCESS)