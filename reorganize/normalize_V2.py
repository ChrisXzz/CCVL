# -*- coding: utf-8 -*-
import itk
import nibabel as nib
import numpy as np
import os
import glob
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count
from tqdm import tqdm

def fix_cosines_and_reorient_image(input_path, output_path):
    try:
        image = itk.imread(input_path, itk.SS)
    except Exception as e:
        print(f'An error occurred: {e}')
        print(f'Attempting to fix cosines problem for {input_path}...')
        img = nib.load(input_path)
        qform = img.get_qform()
        img.set_qform(qform)
        sform = img.get_sform()
        img.set_sform(sform)
        nib.save(img, input_path)
        image = itk.imread(input_path, itk.F)
        print(f'Cosines problem has been fixed for {input_path}.')

    filter = itk.OrientImageFilter.New(image)
    filter.UseImageDirectionOn()
    matrix = np.array([[1, 0, 0], [0, -1, 0], [0, 0, -1]], np.float64) # RPS
    filter.SetDesiredCoordinateDirection(itk.GetMatrixFromArray(matrix))
    filter.Update()
    reoriented = filter.GetOutput()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    itk.imwrite(reoriented, output_path)

def process_single_file(input_path, input_folder, output_folder):
    relative_path = os.path.relpath(input_path, input_folder)
    output_path = os.path.join(output_folder, relative_path)
    fix_cosines_and_reorient_image(input_path, output_path)
    case_name = os.path.basename(output_path)
    print(f'Processed case: {case_name} saved to {output_path}')

def process_nifti_folder(input_folder, output_folder):
    input_paths = glob.glob(os.path.join(input_folder, '**', '*.nii.gz'), recursive=True)
    return input_paths

def main(args):
    input_paths = process_nifti_folder(args.data_path, args.save_dir)

    print('>> {} CPU cores are secured.'.format(int(cpu_count()*1)))

    with ProcessPoolExecutor(max_workers=int(cpu_count()*1)) as executor:
        futures = {executor.submit(process_single_file, input_path, args.data_path, args.save_dir): input_path for input_path in input_paths}
        
        # Add tqdm progress bar
        for future in tqdm(as_completed(futures), total=len(futures), desc='Processing files'):
            input_path = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"Error processing {input_path}: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', default='F:\\wr_temp\\', help='The path of totalsegmentator data')
    parser.add_argument('--save_dir', default='F:\\wr_temp\\', help='The saving path after reorganizing')
    args = parser.parse_args()

    if not os.path.exists(args.save_dir):
        os.makedirs(args.save_dir)

    main(args)
