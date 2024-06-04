# -*- coding: utf-8 -*-
import os
import shutil
import nibabel as nib
import numpy as np
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count
from tqdm import tqdm

def merge_segmentations(input_files, output_file):
    base_img = nib.load(input_files[0])
    base_data = base_img.get_fdata()

    for file in input_files[1:]:
        img = nib.load(file)
        img_data = img.get_fdata()
        base_data += img_data

    new_img = nib.Nifti1Image(base_data, base_img.affine)
    nib.save(new_img, output_file)

def process_case(case_folder, output_folder, features_rename_map, features_to_merge):
    os.makedirs(output_folder, exist_ok=True)
    shutil.copy2(os.path.join(case_folder, 'ct.nii.gz'), os.path.join(output_folder, 'ct.nii.gz'))
    seg_input_folder = os.path.join(case_folder, 'segmentations')
    seg_output_folder = os.path.join(output_folder, 'segmentations')
    shutil.copytree(seg_input_folder, seg_output_folder)

    for old_name, new_name in features_rename_map.items():
        old_path = os.path.join(seg_output_folder, old_name)
        if os.path.exists(old_path):
            new_path = os.path.join(seg_output_folder, new_name)
            os.rename(old_path, new_path)

    for output_name, input_names in features_to_merge.items():
        input_files = [os.path.join(seg_output_folder, name) for name in input_names if os.path.exists(os.path.join(seg_output_folder, name))]
        if input_files:
            merge_segmentations(input_files, os.path.join(seg_output_folder, output_name))

def clean(cases_path, output_root, features_rename_map, features_to_merge):
    cases_folder_name = os.path.basename(cases_path)  

    tasks = []
    for case_name in os.listdir(cases_path):
        case_folder = os.path.join(cases_path, case_name)
        if os.path.isdir(case_folder):
            output_folder = os.path.join(output_root, f"{cases_folder_name}_{case_name}")  
            tasks.append((case_folder, output_folder, features_rename_map, features_to_merge))
    return tasks

def process_task(task):
    process_case(*task)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', default='F:\\Totalsegmentator_dataset', help='The path of totalsegmentator data')
    parser.add_argument('--save_dir', default='F:\\totalsegmentator_reorganized\\', help='The saving path after reorganizing')
    args = parser.parse_args()

    features_rename_map = {
        'gallbladder.nii.gz': 'gall_bladder.nii.gz', 
        'small_bowel.nii.gz': 'intestine.nii.gz'
    }

    features_to_merge = {
        'lung_left.nii.gz': ['lung_lower_lobe_left.nii.gz', 'lung_upper_lobe_left.nii.gz'],
        'lung_right.nii.gz': ['lung_middle_lobe_right.nii.gz', 'lung_lower_lobe_right.nii.gz', 'lung_upper_lobe_right.nii.gz']
    }

    tasks = clean(args.data_path, args.save_dir, features_rename_map, features_to_merge)

    print('>> {} CPU cores are secured.'.format(cpu_count()))
    with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
        futures = {executor.submit(process_task, task): task for task in tasks}

        for future in tqdm(as_completed(futures), total=len(futures), desc='Processing cases'):
            task = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"Error processing {task[0]}: {e}")

if __name__ == '__main__':
    main()

