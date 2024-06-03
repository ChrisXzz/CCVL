import os
import nibabel as nib
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count
from tqdm import tqdm
import argparse

def compress_nii_file(input_path, output_path):
    """压缩 NIfTI 文件并保存为 .nii.gz 格式"""
    img = nib.load(input_path)
    nib.save(img, output_path)

def organize_and_compress_nii_files(base_path, output_base_path):
    """组织并压缩 NIfTI 文件"""
    tasks = []
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.nii'):
                case_method = os.path.basename(root)
                file_name = os.path.splitext(file)[0]
                output_file_name = f"{os.path.basename(base_path)}_{case_method}_{file_name}.nii.gz"
                output_path = os.path.join(output_base_path, output_file_name)

                input_file_path = os.path.join(root, file)
                tasks.append((input_file_path, output_path))
    return tasks

def process_task(task):
    input_path, output_path = task
    compress_nii_file(input_path, output_path)
    return output_path

def main():
    parser = argparse.ArgumentParser(description="Organize and compress NIfTI files.")
    parser.add_argument('--base_path', default='F:\\Heidelberg', help='The base path containing the NIfTI files to be processed.')
    parser.add_argument('--output_base_path', default='F:\\Heidelberg_reorganized\\temp', help='The output base path where compressed files will be saved.')
    args = parser.parse_args()

    tasks = organize_and_compress_nii_files(args.base_path, args.output_base_path)

    print('>> {} CPU cores are secured.'.format(cpu_count()))
    with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
        futures = {executor.submit(process_task, task): task for task in tasks}
        
        for future in tqdm(as_completed(futures), total=len(futures), desc='Processing files'):
            task = futures[future]
            try:
                result = future.result()
                print(f"Compressed and saved: {result}")
            except Exception as e:
                print(f"Error processing {task}: {e}")

if __name__ == "__main__":
    main()
