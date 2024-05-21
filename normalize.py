# -*- coding: utf-8 -*-
import itk
import nibabel as nib
import numpy as np
import os
import glob
import argparse
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count

def fix_cosines_and_reorient_image(input_path, output_path):
    try:
        # Attempt to read with a floating-point type which is commonly supported
        image = itk.imread(input_path, itk.F)
    except Exception as e:
        # If reading fails, provide a message and attempt to fix potential issues
        print(f'An error occurred: {e}')
        print(f'Attempting to fix cosines problem for {input_path}...')
        img = nib.load(input_path)
        qform = img.get_qform()
        img.set_qform(qform)
        sform = img.get_sform()
        img.set_sform(sform)
        nib.save(img, input_path)
        # Try reading the image again with a floating-point type
        image = itk.imread(input_path, itk.F)
        print(f'Cosines problem has been fixed for {input_path}.')

    # Reorient the image to standard space
    filter = itk.OrientImageFilter.New(image)
    filter.UseImageDirectionOn()
    matrix = np.array([[1, 0, 0], [0, -1, 0], [0, 0, -1]], np.float64) # RPS
    filter.SetDesiredCoordinateDirection(itk.GetMatrixFromArray(matrix))
    filter.Update()
    reoriented = filter.GetOutput()

    # Ensure the output directory structure mirrors the input's
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    itk.imwrite(reoriented, output_path)

def process_nifti_folder(input_folder, output_folder):
    # Find all .nii.gz files within the input folder and its subdirectories
    for input_path in glob.glob(os.path.join(input_folder, '**', '*.nii.gz'), recursive=True):
        # Construct the output path by maintaining the directory structure
        relative_path = os.path.relpath(input_path, input_folder)
        output_path = os.path.join(output_folder, relative_path)
        # Process the file and save it to the new location
        fix_cosines_and_reorient_image(input_path, output_path)
        # Print the name of the processed case
        case_name = os.path.basename(output_path)
        print(f'Processed case: {case_name} saved to {output_path}')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', default='/ccvl/net/ccvl15/xinze/AbdomenAtlas/', help='The path of totalsegmentator data')
    parser.add_argument('--save_dir', default='/ccvl/net/ccvl15/xinze/abdomenatlas_cleaned/', help='The saving path after reorganizing')
    args = parser.parse_args()
    
    print('>> {} CPU cores are secured.'.format(cpu_count()))
    with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
        executor.submit(process_nifti_folder(args.data_path, args.save_dir))

if __name__ == '__main__':
    main()
