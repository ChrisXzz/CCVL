# -*- coding: utf-8 -*-
import os
import pydicom
import dicom2nifti
import shutil
import dicom2nifti.settings as settings
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count
from tqdm import tqdm

settings.disable_validate_slice_increment()

def clear_temp_dir(temp_dir):
    for file in os.listdir(temp_dir):
        file_path = os.path.join(temp_dir, file)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

def process_dicom_series(args):
    uid, files, temp_dir, base_output_dir, base_dicom_dir, first_level_dir, dicom_dir = args

    # 创建临时文件夹
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    # 复制所有文件到临时文件夹
    for file in files:
        shutil.copy(file, temp_dir)

    # 将临时文件夹中的文件转换为 NIfTI
    dicom2nifti.convert_directory(temp_dir, temp_dir, compression=True, reorient=True) 

    # 为输出的 NIfTI 文件创建文件名，包括总路径文件夹名、子文件夹名和子文件夹的子文件夹名
    for file_name in os.listdir(temp_dir):
        if file_name.endswith('.nii.gz'):
            new_name = f"{os.path.basename(base_dicom_dir)}_{os.path.basename(first_level_dir)}_{os.path.basename(dicom_dir)}_Depth_{len(files)}_{file_name}"
            shutil.move(os.path.join(temp_dir, file_name), os.path.join(base_output_dir, new_name))

    print(f"Converted SeriesInstanceUID: {uid} with {len(files)} files. Output to {base_output_dir}")

    # 清空临时文件夹
    clear_temp_dir(temp_dir)

def main():
    parser = argparse.ArgumentParser(description="Convert DICOM series to NIfTI format.")
    parser.add_argument('--base_dicom_dir', default = '/Volumes/PortableSSD/TODO/OralContrast', help='The base directory containing DICOM files.')
    parser.add_argument('--base_output_dir', default = '/Volumes/PortableSSD/TODO/OralContrast_reorganized/out', help='The base directory to save the converted NIfTI files.')
    parser.add_argument('--temp_dir', default = '/Volumes/PortableSSD/TODO/OralContrast_reorganized/temp', help='The temporary directory for processing.')
    args = parser.parse_args()

    if not os.path.exists(args.base_output_dir):
        os.makedirs(args.base_output_dir)
    if not os.path.exists(args.temp_dir):
        os.makedirs(args.temp_dir)

    tasks = []

    # 遍历总路径下的所有子文件夹的子文件夹
    for subfolder in os.listdir(args.base_dicom_dir):
        first_level_dir = os.path.join(args.base_dicom_dir, subfolder)
        if not os.path.isdir(first_level_dir):
            continue

        for second_subfolder in os.listdir(first_level_dir):
            dicom_dir = os.path.join(first_level_dir, second_subfolder)
            if not os.path.isdir(dicom_dir):
                continue

            try:
                dicom_files = [f for f in os.listdir(dicom_dir) if os.path.isfile(os.path.join(dicom_dir, f))]

                # 使用字典存储每个 SeriesInstanceUID 对应的文件列表
                series_files = {}

                for dicom_file in dicom_files:
                    ds = pydicom.dcmread(os.path.join(dicom_dir, dicom_file), force=True) # Normally, force=False

                    if "SeriesInstanceUID" in ds:
                        uid = ds.SeriesInstanceUID
                        if uid not in series_files:
                            series_files[uid] = []
                        series_files[uid].append(os.path.join(dicom_dir, dicom_file))

                for uid, files in series_files.items():
                    tasks.append((uid, files, args.temp_dir, args.base_output_dir, args.base_dicom_dir, first_level_dir, dicom_dir))

            except Exception as e:
                print(f"Error processing folder '{dicom_dir}': {e}")

    print('>> {} CPU cores are secured.'.format(cpu_count()))
    with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
        futures = {executor.submit(process_dicom_series, task): task for task in tasks}

        for future in tqdm(as_completed(futures), total=len(futures), desc='Processing DICOM series'):
            task = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"Error processing SeriesInstanceUID {task[0]}: {e}")

if __name__ == "__main__":
    main()

