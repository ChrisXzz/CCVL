# -*- coding: utf-8 -*-
import numpy as np
import nibabel as nb
import os
import pandas as pd
from collections import OrderedDict
from SurfaceDice import compute_surface_distances, compute_surface_dice_at_tolerance, compute_dice_coefficient

seg_path = '/Volumes/PortableSSD/segresnet.jhh/' # segmentation results path
gt_path = '/Volumes/PortableSSD/TODO/Testing/' # groundtruth path
save_path = '/Volumes/PortableSSD/Results' # DSC and NSD results save path
save_name = 'DSC_NSD_suprem.xlsx' # DSC and NSD results file name 
cases = os.listdir(seg_path)
cases = [case for case in cases if os.path.isdir(os.path.join(seg_path, case))]
cases.sort()

labels = ['cyst', 'pancreas', 'pdac', 'pnet']
label_tolerance = {'cyst': 2, 'pancreas': 2, 'pdac': 2, 'pnet': 2}

metrics = OrderedDict()
metrics['Name'] = []
for label in labels:
    metrics[f'{label}_DSC'] = []
    metrics[f'{label}_NSD'] = []

for case in cases:
    seg_case_path = os.path.join(seg_path, case, 'segmentations')
    gt_case_path = os.path.join(gt_path, case, 'segmentations')
    
    if not os.path.exists(gt_case_path):
        print(f"Ground truth for case {case} not found. Skipping this case.")
        continue
    
    metrics['Name'].append(case)
    for label in labels:
        seg_file = os.path.join(seg_case_path, f'pancreatic_{label}.nii.gz')
        gt_file = os.path.join(gt_case_path, f'{label}.nii.gz')
        
        if not os.path.exists(seg_file) or not os.path.exists(gt_file):
            print(f"Segmentation or ground truth file for label {label} in case {case} not found. Skipping this label.")
            DSC, NSD = 0, 0
        else:
            seg_data = np.uint8(nb.load(seg_file).get_fdata())
            gt_data = np.uint8(nb.load(gt_file).get_fdata())
            case_spacing = nb.load(gt_file).header.get_zooms()

            if np.sum(gt_data) == 0:
                DSC, NSD = float('nan'), float('nan')
            else:
                DSC = compute_dice_coefficient(gt_data, seg_data)
                surface_distances = compute_surface_distances(gt_data, seg_data, case_spacing)
                NSD = compute_surface_dice_at_tolerance(surface_distances, label_tolerance[label])
        
        if label in ['cyst', 'pdac', 'pnet']:
                if combined_seg_data is None:
                    combined_seg_data = seg_data
                    combined_gt_data = gt_data
                else:
                    combined_seg_data = np.logical_or(combined_seg_data, seg_data)
                    combined_gt_data = np.logical_or(combined_gt_data, gt_data)
        
        metrics[f'{label}_DSC'].append(round(DSC, 4))
        metrics[f'{label}_NSD'].append(round(NSD, 4))
        print(case, label, round(DSC, 4), 'tol:', label_tolerance[label], round(NSD, 4))
    
    if combined_seg_data is not None and combined_gt_data is not None:
        combined_DSC = compute_dice_coefficient(combined_gt_data, combined_seg_data)
        combined_surface_distances = compute_surface_distances(combined_gt_data, combined_seg_data, case_spacing)
        combined_NSD = compute_surface_dice_at_tolerance(combined_surface_distances, label_tolerance['cyst'])
        metrics['Combined_Tumor_DSC'].append(round(combined_DSC, 4))
        metrics['Combined_Tumor_NSD'].append(round(combined_NSD, 4))
        print(case, 'Combined Tumor', round(combined_DSC, 4), 'tol:', label_tolerance['cyst'], round(combined_NSD, 4))
    else:
        metrics['Combined_Tumor_DSC'].append(float('nan'))
        metrics['Combined_Tumor_NSD'].append(float('nan'))

dataframe = pd.DataFrame(metrics)
dataframe.to_excel(os.path.join(save_path, save_name), index=False)
