# -*- coding: utf-8 -*-
import os
import shutil
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count
from tqdm import tqdm

def process_case(case_folder, src_directory, target_directory):
    case_path = os.path.join(src_directory, case_folder)
    if os.path.isdir(case_path):
        new_case_folder = os.path.join(target_directory, f'Pancreas_{case_folder}')
        os.makedirs(new_case_folder, exist_ok=True)
        
        segmentations_folder = os.path.join(new_case_folder, 'segmentations')
        os.makedirs(segmentations_folder, exist_ok=True)
        
        for file in os.listdir(case_path):
            file_path = os.path.join(case_path, file)
            if file == 'ct.nii.gz':
                shutil.copy(file_path, new_case_folder)
            elif file.endswith('.nii.gz') and file != 'ct.nii.gz':
                shutil.copy(file_path, segmentations_folder)
    
    return case_folder

def pancreas_reorganized(src_directory, target_directory):
    if not os.path.exists(src_directory):
        print(f"Source directory {src_directory} does not exist.")
        return

    if not os.path.exists(target_directory):
        os.makedirs(target_directory, exist_ok=True)

    case_folders = [case_folder for case_folder in os.listdir(src_directory) if os.path.isdir(os.path.join(src_directory, case_folder))]
    return case_folders

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', required=True, help='The path of your data')
    parser.add_argument('--save_dir', required=True, help='The saving path after reorganization')
    args = parser.parse_args()

    case_folders = pancreas_reorganized(args.data_path, args.save_dir)
    
    print('>> {} CPU cores are secured.'.format(cpu_count()))
    with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
        futures = {executor.submit(process_case, case_folder, args.data_path, args.save_dir): case_folder for case_folder in case_folders}

        for future in tqdm(as_completed(futures), total=len(futures), desc='Processing cases'):
            case_folder = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"Error processing {case_folder}: {e}")

if __name__ == "__main__":
    main()
