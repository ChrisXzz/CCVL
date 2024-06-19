import os
import nibabel as nib
import numpy as np
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count
from tqdm import tqdm

def normalize_image(image, min_val=-1000, max_val=1000):
    """
    Normalize the image to the range [min_val, max_val]
    """
    image[image > max_val] = max_val
    image[image < min_val] = min_val
    normalized_image = image
    
    return normalized_image

def process_file(file_path):
    """
    Normalize a single ct.nii.gz file
    """
    # Load the NIfTI file
    img = nib.load(file_path)
    img_data = np.array(img.dataobj)

    normalized_data = normalize_image(img_data)

    normalized_img = nib.Nifti1Image(normalized_data, img.affine, img.header)

    normalized_img.set_data_dtype(np.int16)
    normalized_img.get_data_dtype(finalize=True)
    
    nib.save(normalized_img, file_path)
    return file_path



def normalize_ct_images(directory):
    """
    Generate tasks for normalizing all ct.nii.gz files in the specified directory
    """
    tasks = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file == 'ct.nii.gz':
                file_path = os.path.join(root, file)
                tasks.append(file_path)
    return tasks

def main():
    parser = argparse.ArgumentParser(description="Normalize CT images in NIfTI format to int16.")
    parser.add_argument('--directory', default = 'F:\\acrin_reorganized\\final', help='The directory containing the ct.nii.gz files.')
    args = parser.parse_args()

    tasks = normalize_ct_images(args.directory)
    
    print('>> {} CPU cores are secured.'.format(cpu_count()))
    with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
        futures = {executor.submit(process_file, task): task for task in tasks}

        for future in tqdm(as_completed(futures), total=len(futures), desc='Normalizing and converting CT images'):
            task = futures[future]
            try:
                future.result()
                # print(f"Normalized and saved {task}")
            except Exception as e:
                print(f"Error processing {task}: {e}")

if __name__ == '__main__':
    main()


