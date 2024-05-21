import os
import shutil
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count

def pancreas_reorganized(src_directory, target_directory):
    if not os.path.exists(src_directory):
        print(f"Source directory {src_directory} does not exist.")
        return

    if not os.path.exists(target_directory):
        os.makedirs(target_directory, exist_ok=True)

    # Iterate through each case data folder
    for case_folder in os.listdir(src_directory):
        case_path = os.path.join(src_directory, case_folder)
        if os.path.isdir(case_path):
            # Create a new case data folder in the target directory
            new_case_folder = os.path.join(target_directory, f'{os.path.basename(src_directory)}_{case_folder}')
            os.makedirs(new_case_folder, exist_ok=True)
            
            # Create segments folder under new case data folder
            segmentations_folder = os.path.join(new_case_folder, 'segmentations')
            os.makedirs(segmentations_folder, exist_ok=True)
            
            # Iterate through all files in case data
            for file in os.listdir(case_path):
                file_path = os.path.join(case_path, file)
                if file == 'ct.nii.gz':
                    # Copy ct.nii.gz to the new case data folder
                    try:
                        shutil.copy(file_path, new_case_folder)
                    except Exception as e:
                        print(f"Error copying {file_path} to {new_case_folder}: {e}")
                elif file.endswith('.nii.gz') and file != 'ct.nii.gz':
                    # Move other nii.gz files to the segments folder
                    try:
                        shutil.copy(file_path, segmentations_folder)
                    except Exception as e:
                        print(f"Error moving {file_path} to {segmentations_folder}: {e}")
    
    print("Finished")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', default='/ccvl/net/ccvl15/zzhou82/PublicAbdominalData/21_CTSpine1K/data/colon', 
                        help='The path of your data')
    parser.add_argument('--save_dir', default='/ccvl/net/ccvl15/xinze/ctspine1k_reorganized/colon', help='The saving path after 1 by 1 matched')
    args = parser.parse_args()
    
    print('>> {} CPU cores are secured.'.format(cpu_count()))
    with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
        executor.submit(pancreas_reorganized(args.data_path, args.save_dir))

    
if __name__ == "__main__":
    main()