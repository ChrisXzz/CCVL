# -*- coding: utf-8 -*-
import os
import nibabel as nib
import numpy as np
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm
import argparse

def convert_image_dtype(file_path, target_dtype, max_value=None):
    img = nib.load(file_path)
    data = np.array(img.dataobj)
    

    if max_value is not None:
        data[data > max_value] = max_value
        data[data < -max_value] = -max_value
    # data = data.astype(target_dtype)
    img = nib.Nifti1Image(data, img.affine, img.header)
    img.set_data_dtype(target_dtype)
    img.get_data_dtype(finalize=True)
    nib.save(img, file_path)
    # print(f"Converted {file_path} to {target_dtype}")

def process_case_folder(case_folder):
    ct_file = os.path.join(case_folder, 'ct.nii.gz')
    segmentations_folder = os.path.join(case_folder, 'segmentations')
    
    if os.path.exists(ct_file):
        convert_image_dtype(ct_file, np.int16, max_value=1000)
    
    if os.path.exists(segmentations_folder):
        for file_name in os.listdir(segmentations_folder):
            if file_name.endswith('.nii.gz'):
                seg_file = os.path.join(segmentations_folder, file_name)
                convert_image_dtype(seg_file, np.int8)

def process_all_cases(base_folder):
    case_folders = [os.path.join(base_folder, case_name) for case_name in os.listdir(base_folder) if os.path.isdir(os.path.join(base_folder, case_name))]
    
    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(process_case_folder, case_folder): case_folder for case_folder in case_folders}
        
        for future in tqdm(as_completed(futures), total=len(futures), desc='Processing cases'):
            case_folder = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"Error processing {case_folder}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Process medical image datasets.")
    parser.add_argument('--base_folder', default = 'G:\\TODO\\yf_reorganized\\', help='The base folder containing all case folders.')
    args = parser.parse_args()
    
    process_all_cases(args.base_folder)

if __name__ == '__main__':
    main()
