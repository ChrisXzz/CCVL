import os
import nibabel as nib
import numpy as np
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count
from tqdm import tqdm

def binarize_segmentation(input_file):
    """
    Binarize the segmentation file.
    """
    img = nib.load(input_file)
    data = img.get_fdata()
    
    # Binarize the data (convert to 0/1)
    binarized_data = np.where(data > 0, 1, 0)
    
    # Create a new NIfTI image
    binarized_img = nib.Nifti1Image(binarized_data, img.affine, img.header)
    
    # Save the binarized image, overwriting the original file
    nib.save(binarized_img, input_file)
    return input_file

def process_case(case_folder):
    """
    Process a single case folder.
    """
    segmentations_folder = os.path.join(case_folder, 'segmentations')
    if not os.path.exists(segmentations_folder):
        print(f"No segmentations folder found in {case_folder}")
        return []
    
    tasks = []
    for filename in os.listdir(segmentations_folder):
        if filename.endswith('.nii.gz'):
            input_file = os.path.join(segmentations_folder, filename)
            tasks.append(input_file)
    return tasks

def process_all_cases(root_folder):
    """
    Generate tasks for processing all cases in the specified root folder.
    """
    tasks = []
    for case_folder in os.listdir(root_folder):
        case_path = os.path.join(root_folder, case_folder)
        if os.path.isdir(case_path):
            tasks.extend(process_case(case_path))
    return tasks

def main():
    parser = argparse.ArgumentParser(description="Binarize NIfTI segmentation files.")
    parser.add_argument('--root_folder', default='/Volumes/PortableSSD/TODO/out_reorganized/', help='The root folder containing all the cases.')
    args = parser.parse_args()

    tasks = process_all_cases(args.root_folder)
    
    print('>> {} CPU cores are secured.'.format(cpu_count()))
    with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
        futures = {executor.submit(binarize_segmentation, task): task for task in tasks}

        for future in tqdm(as_completed(futures), total=len(futures), desc='Binarizing segmentation files'):
            task = futures[future]
            try:
                future.result()
                # print(f"Binarized and overwritten {task}")
            except Exception as e:
                print(f"Error processing {task}: {e}")

if __name__ == '__main__':
    main()
