import os
import nibabel as nib
import shutil
import numpy as np
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count
from tqdm import tqdm

feature_dict = {'background': 0, 'unknown_tissue': 1, 'muscles': 2, 'fat': 3, 'abdominal_tissue': 4, 'mediastinal_tissue': 5,
                'esophagus': 6, 'stomach': 7, 'small_bowel': 8, 'duodenum': 9, 'colon': 10, 'gallbladder': 12, 'liver': 13, 
                'pancreas': 14, 'kidney_left': 15, 'kidney_right': 16, 'bladder': 17, 'gonads': 18, 'prostate': 19,
                'uterocervix': 20, 'uterus': 21, 'breast_left': 22, 'breast_right': 23, 'spinal_canal': 24, 'brain': 25,
                'spleen': 26, 'adrenal_gland_left': 27, 'adrenal_gland_right': 28, 'thyroid_left': 29, 'thyroid_right': 30,
                'thymus': 31, 'gluteus_maximus_left': 32, 'gluteus_maximus_right': 33, 'gluteus_medius_left': 34,
                'gluteus_medius_right': 35, 'gluteus_minimus_left': 36, 'gluteus_minimus_right': 37, 'iliopsoas_left': 38,
                'iliopsoas_right': 39, 'autochthon_left': 40, 'autochthon_right': 41, 'skin': 42, 'vertebrae_C1': 43,
                'vertebrae_C2': 44, 'vertebrae_C3': 45, 'vertebrae_C4': 46, 'vertebrae_C5': 47, 'vertebrae_C6': 48,
                'vertebrae_C7': 49, 'vertebrae_T1': 50, 'vertebrae_T2': 51, 'vertebrae_T3': 52, 'vertebrae_T4': 53,
                'vertebrae_T5': 54, 'vertebrae_T6': 55, 'vertebrae_T7': 56, 'vertebrae_T8': 57, 'vertebrae_T9': 58, 
                'vertebrae_T10': 59, 'vertebrae_T11': 60, 'vertebrae_T12': 61, 'vertebrae_L1': 62, 'vertebrae_L2': 63,
                'vertebrae_L3': 64, 'vertebrae_L4': 65, 'vertebrae_L5': 66, 'costa_1_left': 67, 'costa_1_right': 68,
                'costa_2_left': 69, 'costa_2_right': 70, 'costa_3_left': 71, 'costa_3_right': 72, 'costa_4_left': 73,
                'costa_4_right': 74, 'costa_5_left': 75, 'costa_5_right': 76, 'costa_6_left': 77, 'costa_6_right': 78,
                'costa_7_left': 79, 'costa_7_right': 80, 'costa_8_left': 81, 'costa_8_right': 82, 'costa_9_left': 83,
                'costa_9_right': 84, 'costa_10_left': 85, 'costa_10_right': 86, 'costa_11_left': 87, 'costa_11_right': 88,
                'costa_12_left': 89, 'costa_12_right': 90, 'rib_cartilage': 91, 'sternum_corpus': 92, 'clavicula_left': 93,
                'clavicula_right': 94, 'scapula_left': 95, 'scapula_right': 96, 'humerus_left': 97, 'humerus_right': 98,
                'skull': 99, 'hip_left': 100, 'hip_right': 101, 'sacrum': 102, 'femur_left': 103, 'femur_right': 104,
                'heart': 105, 'heart_atrium_left': 106, 'heart_tissue': 107, 'heart_atrium_right': 108, 'heart_myocardium': 109,
                'heart_ventricle_left': 110, 'heart_ventricle_right': 111, 'iliac_artery_left': 112, 'iliac_artery_right': 113,
                'aorta': 114, 'iliac_vena_left': 115, 'iliac_vena_right': 116, 'inferior_vena_cava': 117, 
                'portal_vein_and_splenic_vein': 118, 'celiac_trunk': 119, 'lung_lower_lobe_left': 120, 'lung_upper_lobe_left': 121,
                'lung_lower_lobe_right': 122, 'lung_middle_lobe_right': 123, 'lung_upper_lobe_right': 124, 'bronchus': 125,
                'trachea': 126, 'pulmonary_artery': 127, 'cheek_left': 128, 'cheek_right': 129, 'eyeball_left': 130,
                'eyeball_right': 131, 'nasal_cavity': 132, 'artery_common_carotid_right': 133, 'artery_common_carotid_left': 134,
                'sternum_manubrium': 135, 'artery_internal_carotid_right': 136, 'artery_internal_carotid_left': 137,
                'internal_jugular_vein_right': 138, 'internal_jugular_vein_left': 139, 'artery_brachiocephalic': 140,
                'vein_brachiocephalic_right': 141, 'vein_brachiocephalic_left': 142, 'artery_subclavian_right': 143,
                'artery_subclavian_left': 144}  # Fill in with actual feature name and value

def match(raw_base_dir, mask_base_dir, new_base_dir):
    """匹配原始数据和掩码数据，并复制到新的目录结构中"""
    if not os.path.isdir(new_base_dir):
        os.makedirs(new_base_dir)

    tasks = []
    for case in os.listdir(raw_base_dir):
        case_raw_path = os.path.join(raw_base_dir, case)
        case_mask_path = os.path.join(mask_base_dir, case)

        if os.path.isfile(case_raw_path) and case_raw_path.endswith('.nii.gz'):
            new_case_dir = os.path.join(new_base_dir, f'{case.split(".")[0]}')
            os.makedirs(new_case_dir, exist_ok=True)

            ct_dst = os.path.join(new_case_dir, 'ct.nii.gz')
            shutil.copy2(case_raw_path, ct_dst)

            seg_dir = os.path.join(new_case_dir, 'segmentations')
            os.makedirs(seg_dir, exist_ok=True)
            mask_dst = os.path.join(seg_dir, case)
            if os.path.isfile(case_mask_path):
                shutil.copy2(case_mask_path, mask_dst)
            else:
                print(f"Warning: Mask file for case {case} not found.")
                
            tasks.append(new_case_dir)
    return tasks

def extract_features(case_dir, feature_dict):
    """提取特征并保存为单独的 NIfTI 文件"""
    segmentation_folder = os.path.join(case_dir, "segmentations")
    case = os.path.basename(case_dir)
    segmentation_file = os.path.join(segmentation_folder, f"{case}.nii.gz")

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
                print(f"Feature '{feature_name}' saved for case {case}.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', default='F:\\AutoPET\\', help='The path of your raw data')
    parser.add_argument('--data_path_mask', default='F:\\Atlas_dataset\\', help='The path of your mask data')
    parser.add_argument('--save_dir', default='F:\\autopet_reorganized\\', help='The saving path after 1 by 1 matched')
    args = parser.parse_args()
  
    print('>> {} CPU cores are secured.'.format(int(cpu_count()*1)))
    
    with ProcessPoolExecutor(max_workers=int(cpu_count()*1)) as executor:
        match_tasks = match(args.data_path, args.data_path_mask, args.save_dir)
        
        futures = {executor.submit(extract_features, case_dir, feature_dict): case_dir for case_dir in match_tasks}

        for future in tqdm(as_completed(futures), total=len(futures), desc='Extracting features'):
            case_dir = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"Error processing {case_dir}: {e}")

if __name__ == "__main__":
    main()
