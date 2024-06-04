import os
import shutil
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count
from tqdm import tqdm
import argparse

def process_file(file, dataset_path, target_path):
    if os.path.isfile(os.path.join(dataset_path, file)):
        file_name = os.path.splitext(file)[0]
        if file_name.endswith('.nii'):
            file_name = file_name[:-4]  # 移除 .nii 扩展名
        
        new_folder_path = os.path.join(target_path, file_name)
        os.makedirs(new_folder_path, exist_ok=True)
        
        segmentations_folder_path = os.path.join(new_folder_path, 'segmentations')
        os.makedirs(segmentations_folder_path, exist_ok=True)
        
        new_file_path = os.path.join(new_folder_path, 'ct.nii.gz')
        shutil.copy2(os.path.join(dataset_path, file), new_file_path)
        
    return file

def main():
    parser = argparse.ArgumentParser(description="Reorganize medical image dataset.")
    parser.add_argument('--dataset_path', default='F:\\Heidelberg_reorganized\\temp', help='The path of the dataset to be processed.')
    parser.add_argument('--target_path', default='F:\\Heidelberg_reorganized\\upload', help='The target path where files will be copied.')
    args = parser.parse_args()
    
    files = os.listdir(args.dataset_path)
    
    print('>> {} CPU cores are secured.'.format(cpu_count()))
    with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
        futures = {executor.submit(process_file, file, args.dataset_path, args.target_path): file for file in files}
        
        for future in tqdm(as_completed(futures), total=len(futures), desc='Processing files'):
            file = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"Error processing {file}: {e}")

if __name__ == "__main__":
    main()

