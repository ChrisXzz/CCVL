# -*- coding: utf-8 -*-
import numpy as np
import nibabel as nb
import os
import pandas as pd
from collections import OrderedDict
from SurfaceDice import compute_surface_distances, compute_surface_dice_at_tolerance, compute_dice_coefficient

seg_path = 'E:\\suprem_remake\\SuPreM\\target_applications\\pancreas_tumor_detection\\inference\\segresnet.jhh\\'
gt_path = 'E:\\GT\\'
save_path = 'E:\\'
save_name = 'DSC_NSD_teamname.xlsx'
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
    seg_case_path = os.path.join(seg_path, case, 'probabilities')
    gt_case_path = os.path.join(gt_path, case, 'segmentations')
    
    if not os.path.exists(gt_case_path):
        print(f"Ground truth for case {case} not found. Skipping this case.")
        continue
    
    metrics['Name'].append(case)
    for label in labels:
        seg_file = os.path.join(seg_case_path, f'{label}.nii.gz')
        gt_file = os.path.join(gt_case_path, f'{label}.nii.gz')
        
        if not os.path.exists(seg_file) or not os.path.exists(gt_file):
            print(f"Segmentation or ground truth file for label {label} in case {case} not found. Skipping this label.")
            DSC, NSD = 0, 0
        else:
            seg_data = np.uint8(nb.load(seg_file).get_fdata())
            gt_data = np.uint8(nb.load(gt_file).get_fdata())
            case_spacing = nb.load(gt_file).header.get_zooms()

            if np.sum(gt_data) == 0 and np.sum(seg_data) == 0:
                DSC, NSD = 1, 1
            elif np.sum(gt_data) == 0 or np.sum(seg_data) == 0:
                DSC, NSD = 0, 0
            else:
                DSC = compute_dice_coefficient(gt_data, seg_data)
                if DSC < 0.2:
                    NSD = 0
                else:
                    surface_distances = compute_surface_distances(gt_data, seg_data, case_spacing)
                    NSD = compute_surface_dice_at_tolerance(surface_distances, label_tolerance[label])
        
        metrics[f'{label}_DSC'].append(round(DSC, 4))
        metrics[f'{label}_NSD'].append(round(NSD, 4))
        print(case, label, round(DSC, 4), 'tol:', label_tolerance[label], round(NSD, 4))

dataframe = pd.DataFrame(metrics)
dataframe.to_excel(os.path.join(save_path, save_name), index=False)
