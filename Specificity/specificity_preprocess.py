# -*- coding: utf-8 -*-
import os
import cc3d
import nibabel as nib
import numpy as np
import pandas as pd
from scipy.ndimage import binary_dilation
import math
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count
from tqdm import tqdm
import argparse

def remove_small_components(seg_data, label, voxel_volume, min_radius):
    labeled, N = cc3d.connected_components(seg_data == label, connectivity=6, return_N=True)
    for i in range(1, N + 1):
        component = (labeled == i)
        if component.any():
            voxel = np.sum(component)
            volume = voxel * voxel_volume
            radius = (3 * volume / (4 * math.pi))**(1/3)
            if radius <= min_radius:
                seg_data[component] = 0
    return seg_data

def keep_largest_component(seg_data, label):
    labeled, N = cc3d.connected_components(seg_data == label, connectivity=6, return_N=True)
    max_component = None
    max_size = 0
    for i in range(1, N + 1):
        component = (labeled == i)
        size = np.sum(component)
        if size > max_size:
            max_component = component
            max_size = size
    if max_component is not None:
        seg_data[seg_data == label] = 0
        seg_data[max_component] = label
    return seg_data

def process_segmentation(input_file, output_file, min_radius):
    img = nib.load(input_file)
    data = img.get_fdata()
    voxel_volume = np.prod(img.header.get_zooms())
    data[data==4] = 1 #remove cyst, treat it as pancreas 
    data = keep_largest_component(data, 1)

    #for label in [3, 4, 5]:
    for label in [3, 5]: #remove cyst mask
        data = remove_small_components(data, label, voxel_volume, min_radius)
        label_mask = (data == label)
        dilated_mask = binary_dilation(label_mask, iterations=1)
        if np.any(dilated_mask & (data == 1)):
            data[label_mask] = label
        else:
            data[label_mask] = 0

    data = data.astype(np.int8)
    processed_img = nib.Nifti1Image(data, img.affine)
    nib.save(processed_img, output_file)

def process_case(filename, input_dir, output_dir, min_radius):
    input_file = os.path.join(input_dir, filename)
    output_file = os.path.join(output_dir, filename)
    print(f"Processing {filename}...")
    process_segmentation(input_file, output_file, min_radius)

def process_all_cases(input_dir, output_dir, min_radius):
    os.makedirs(output_dir, exist_ok=True)
    files = [f for f in os.listdir(input_dir) if f.endswith('.nii.gz')]

    print('>> {} CPU cores are secured.'.format(cpu_count()))
    with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
        futures = {
            executor.submit(process_case, filename, input_dir, output_dir, min_radius): filename
            for filename in files
        }

        for future in tqdm(as_completed(futures), total=len(futures), desc='Processing cases'):
            filename = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"Error processing {filename}: {e}")

def calculate_true_negative(csv_file, output_dir, dataset):
    df = pd.read_csv(csv_file)
    msd_healthy_cases = df[(df['source_dataset'] == dataset) & (df['pancreas'] == 'healthy')]
    msd_healthy_case_names = msd_healthy_cases['AbdomenAtlas_id'].tolist()
    
    true_negative_count = 0

    for case in msd_healthy_case_names:
        # load nii.gz file
        seg_file = os.path.join(output_dir, f"{case}.nii.gz")
        if os.path.exists(seg_file):
            img = nib.load(seg_file)
            data = img.get_fdata()
            
            # check if any detectable tumors
            if np.all((data != 3) & (data != 4) & (data != 5)):
                true_negative_count += 1
    
    return len(msd_healthy_case_names), true_negative_count



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process segmentation results with connected component analysis.")
    parser.add_argument('--input_dir', required=True, help='The directory containing input segmentation files.')
    parser.add_argument('--output_dir', required=True, help='The directory to save the processed segmentation files.')
    parser.add_argument('--gt_csv', required=True, help='The directory containing patient groudtruth information.')
    parser.add_argument('--min_radius', required=True, help='The smallest tumor size you want to detect.')
    parser.add_argument('--dataset', required=True, help='The name of dataset you want to process.')
    
    args = parser.parse_args()

    process_all_cases(args.input_dir, args.output_dir, args.min_radius)
    total_cases, true_negative_count = calculate_true_negative(args.gt_csv, args.output_dir, args.dataset)
    Specificity = true_negative_count/total_cases
    print(f"Total healthy cases: {total_cases}")
    print(f"True negative cases: {true_negative_count}")
    print(f"Specificity:{Specificity}")