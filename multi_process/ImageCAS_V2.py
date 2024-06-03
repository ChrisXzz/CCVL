# -*- coding: utf-8 -*-
import os
import shutil
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count
from tqdm import tqdm

def process_file(base_path, filename, target_path):
    """处理单个文件，重命名并移动到目标路径"""
    if filename.endswith('.nii.gz'):
        case_name, case_type = filename.split('.')[:2]

        # 创建案例对应的文件夹
        case_folder_name = f"{os.path.basename(base_path)}_{case_name}"
        case_folder_path = os.path.join(target_path, case_folder_name)
        os.makedirs(case_folder_path, exist_ok=True)
        
        if case_type == 'label':
            # 创建 segmentations 文件夹
            segmentations_folder_path = os.path.join(case_folder_path, 'segmentations')
            os.makedirs(segmentations_folder_path, exist_ok=True)
            # 重命名标注文件并移动到 segmentations 文件夹
            new_label_filename = f"{case_name}_labels.nii.gz"
            shutil.copy2(os.path.join(base_path, filename), os.path.join(segmentations_folder_path, new_label_filename))
        elif case_type == 'img':
            # 重命名 ct 影像并移动到案例文件夹
            new_ct_filename = 'ct.nii.gz'
            shutil.copy2(os.path.join(base_path, filename), os.path.join(case_folder_path, new_ct_filename))

def reorganize_files(base_path, target_path):
    """遍历指定路径下的所有文件，并行处理符合命名规则的文件"""
    files = [filename for filename in os.listdir(base_path) if filename.endswith('.nii.gz')]
    
    with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
        futures = {executor.submit(process_file, base_path, filename, target_path): filename for filename in files}

        for future in tqdm(as_completed(futures), total=len(futures), desc='Processing files'):
            filename = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"Error processing {filename}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Reorganize medical image datasets.")
    parser.add_argument('--base_path', default = 'F:\\ImageCAS', help='The base path containing the nii.gz files.')
    parser.add_argument('--target_path', default = 'F:\\imagecas_reorganized', help='The target path where reorganized files will be saved.')
    args = parser.parse_args()

    reorganize_files(args.base_path, args.target_path)

if __name__ == "__main__":
    main()
