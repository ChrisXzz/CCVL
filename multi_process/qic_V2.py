import os
import shutil
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count
from tqdm import tqdm

target_features = ['spleen', 'gall_bladder', 'kidney_left', 'kidney_right', 'liver', 'pancreas', 'postcava', 
                   'stomach', 'adrenal_gland_left', 'adrenal_gland_right', 'bladder', 'celiac_truck', 'colon', 'duodenum',
                   'esophagus', 'femur_left', 'femur_right', 'hepatic_vessel', 'intestine', 'lung_left', 'lung_right', 
                   'portal_vein_and_splenic_vein', 'prostate', 'rectum', 'aorta', 'esophagus_tumor']

def process_single_case(base_dir, case, target_features, new_base_dir):
    case_path = os.path.join(base_dir, case)
    if os.path.isdir(case_path):
        base_dir_name = os.path.basename(base_dir)
        new_case_dir_name = f"{base_dir_name}_{case}"
        new_case_dir = os.path.join(new_base_dir, new_case_dir_name)
        os.makedirs(new_case_dir, exist_ok=True)
        
        ct_src = os.path.join(case_path, "ct.nii.gz")
        ct_dst = os.path.join(new_case_dir, "ct.nii.gz")
        if os.path.exists(ct_src):
            shutil.copy(ct_src, ct_dst)
        
        seg_dir = os.path.join(new_case_dir, "segmentations")
        os.makedirs(seg_dir, exist_ok=True)
        
        for feature in target_features:
            feature_src = os.path.join(case_path, "segmentations", f"{feature}.nii.gz")
            feature_dst = os.path.join(seg_dir, f"{feature}.nii.gz")
            if os.path.exists(feature_src):
                shutil.copy(feature_src, feature_dst)
        return case

def organize_dataset(base_dir, target_features, new_base_dir):
    os.makedirs(new_base_dir, exist_ok=True)
    cases = [case for case in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, case))]
    return cases

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', default='F:\\qic', help='The path of your data')
    parser.add_argument('--save_dir', default='F:\\qic_reorganized', help='The saving path')
    args = parser.parse_args()

    cases = organize_dataset(args.data_path, target_features, args.save_dir)

    print('>> {} CPU cores are secured.'.format(cpu_count()))
    with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
        futures = {executor.submit(process_single_case, args.data_path, case, target_features, args.save_dir): case for case in cases}

        for future in tqdm(as_completed(futures), total=len(futures), desc='Processing cases'):
            case = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"Error processing {case}: {e}")

if __name__ == "__main__":
    main()
