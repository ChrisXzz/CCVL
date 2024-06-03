# -*- coding: utf-8 -*-
import os
import nibabel as nib
import shutil
import numpy as np
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count
from tqdm import tqdm

feature_dict = {'vertebrae_C1': 1, 'vertebrae_C2': 2, 'vertebrae_C3': 3, 'vertebrae_C4': 4, 'vertebrae_C5': 5,
                'vertebrae_C6': 6, 'vertebrae_C7': 7, 'vertebrae_T1': 8, 'vertebrae_T2': 9, 'vertebrae_T3': 10, 'vertebrae_T4': 11, 
                'vertebrae_T5': 12, 'vertebrae_T6': 13, 'vertebrae_T7': 14, 'vertebrae_T8': 15, 'vertebrae_T9': 16, 'vertebrae_T10': 17, 
                'vertebrae_T11': 18, 'vertebrae_T12': 19, 'vertebrae_L1': 20, 'vertebrae_L2': 21, 'vertebrae_L3': 22, 'vertebrae_L4': 23, 
                'vertebrae_L5': 24, 'vertebrae_L6': 25}

def match(raw_base_dir, mask_base_dir, new_base_dir):
    if not os.path.isdir(new_base_dir):
        os.makedirs(new_base_dir, exist_ok=True)
        
    tasks = []
    for case in os.listdir(raw_base_dir):
        case_raw_path = os.path.join(raw_base_dir, case)
        if os.path.isfile(case_raw_path) and case_raw_path.endswith('.nii.gz'):
            tasks.append((raw_base_dir, mask_base_dir, new_base_dir, case))
        else:
            print(f"Warning: Raw file for case {case} not found.")
    return tasks

def process_match_task(raw_base_dir, mask_base_dir, new_base_dir, case):
    case_raw_path = os.path.join(raw_base_dir, case)
    case_new_path = os.path.join(new_base_dir, os.path.splitext(os.path.splitext(case)[0])[0])

    # Create a new case directory for the case
    new_case_dir = os.path.join(new_base_dir, f'{os.path.basename(os.path.normpath(raw_base_dir))}_{os.path.splitext(os.path.splitext(case)[0])[0]}')
    os.makedirs(new_case_dir, exist_ok=True)
    
    # Copy and rename raw data to ct.nii.gz
    ct_dst = os.path.join(new_case_dir, 'ct.nii.gz')
    shutil.copy2(case_raw_path, ct_dst)
    
    # Create new path in new directory and copy mask data
    seg_dir = os.path.join(new_case_dir, 'segmentations')
    os.makedirs(seg_dir, exist_ok=True)
    # Base case name is the filename without the extension
    base_case_name = os.path.splitext(os.path.splitext(case)[0])[0]
    # Here we append '_seg' to the base case name to get the mask filename
    case_mask_path = os.path.join(mask_base_dir, f"{base_case_name}_seg.nii.gz")
    
    mask_dst = os.path.join(seg_dir, f"{os.path.basename(os.path.normpath(raw_base_dir))}_{base_case_name}_seg.nii.gz")
    if os.path.isfile(case_mask_path):
        shutil.copy2(case_mask_path, mask_dst)
    else:
        print(f"Warning: Mask file for case {base_case_name} not found.")

def extract_features(data_folder, feature_dict):
    tasks = []
    for case in os.listdir(data_folder):
        case_path = os.path.join(data_folder, case)
        if os.path.isdir(case_path):
            tasks.append((case_path, feature_dict))
    return tasks

def process_feature_task(case_path, feature_dict):
    segmentation_folder = os.path.join(case_path, "segmentations")
    base_case_name = os.path.basename(case_path)
    segmentation_file = os.path.join(segmentation_folder, f"{base_case_name}_seg.nii.gz")

    if os.path.isfile(segmentation_file):
        seg_img = nib.load(segmentation_file)
        seg_data = seg_img.get_fdata()

        for feature_name, feature_value in feature_dict.items():
            feature_mask = (seg_data == feature_value)
            if np.any(feature_mask):
                feature_data = np.zeros_like(seg_data)
                feature_data[feature_mask] = feature_value
                feature_img = nib.Nifti1Image(feature_data, seg_img.affine, seg_img.header)
                feature_filename = f"{feature_name}.nii.gz"
                nib.save(feature_img, os.path.join(segmentation_folder, feature_filename))
                print(f"Feature '{feature_name}' saved for case {base_case_name}")
    else:
        print(f"Warning: Mask file for case {base_case_name} not found.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', default='F:\\21_CTSpine1K\\colon\\', 
                        help='The path of your data')
    parser.add_argument('--data_path_mask', default='F:\\21_CTSpine1K\\label\\conlon\\', 
                        help='The path of your data with mask/label')
    parser.add_argument('--save_dir', default='F:\\ctspine1k_reorganized\\', help='The saving path after 1 by 1 matched')
    args = parser.parse_args()
    
    print('>> {} CPU cores are secured.'.format(cpu_count()))
    '''
    # Matching tasks
    match_tasks = match(args.data_path, args.data_path_mask, args.save_dir)
    with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
        futures = {executor.submit(process_match_task, *task): task for task in match_tasks}
        for future in tqdm(as_completed(futures), total=len(futures), desc='Matching cases'):
            task = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"Error processing {task[3]}: {e}")
    '''
    # Feature extraction tasks
    extract_tasks = extract_features(args.save_dir, feature_dict)
    with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
        futures = {executor.submit(process_feature_task, *task): task for task in extract_tasks}
        for future in tqdm(as_completed(futures), total=len(futures), desc='Extracting features'):
            task = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"Error processing {task[0]}: {e}")
    

if __name__ == "__main__":
    main()
