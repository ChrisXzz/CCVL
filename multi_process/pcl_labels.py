import os
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count
from tqdm import tqdm

def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        return file_path, 'deleted'
    else:
        return file_path, 'not found'

def rename_file(old_path, new_path):
    if os.path.exists(old_path):
        os.rename(old_path, new_path)
        return old_path, new_path, 'renamed'
    else:
        return old_path, new_path, 'not found'

def process_directory(base_directory, files_to_delete, files_to_rename):
    tasks = []
    for root, _, _ in os.walk(base_directory):
        # Add delete tasks
        for file_name in files_to_delete:
            file_path = os.path.join(root, file_name)
            tasks.append(('delete', file_path))
        
        # Add rename tasks
        for old_name, new_name in files_to_rename.items():
            old_path = os.path.join(root, old_name)
            new_path = os.path.join(root, new_name)
            tasks.append(('rename', old_path, new_path))
    
    return tasks

def main():
    parser = argparse.ArgumentParser(description="Delete and rename files in a specified directory.")
    parser.add_argument('--directory', default='/Volumes/PortableSSD/TODO/id_map/', help='The base directory to process.')
    args = parser.parse_args()

    base_directory = args.directory

    files_to_delete = [
        "cyst_mask_predicted.nii.gz",
        "duct_mask_predicted.nii.gz",
        "pancreas_mask_split_0.nii.gz",
        "pancreas_mask_split_1.nii.gz",
        "pancreas_mask_split_2.nii.gz"
    ]

    files_to_rename = {
        "cyst_mask_groundtruth.nii.gz": "pancreatic_cyst.nii.gz",
        "duct_mask_groundtruth.nii.gz": "pancreatic_duct.nii.gz",
        "pancreas_mask.nii.gz": "pancreas.nii.gz"
    }

    tasks = process_directory(base_directory, files_to_delete, files_to_rename)

    print('>> {} CPU cores are secured.'.format(cpu_count()))
    with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
        delete_futures = {
            executor.submit(delete_file, task[1]): task[1] for task in tasks if task[0] == 'delete'
        }
        rename_futures = {
            executor.submit(rename_file, task[1], task[2]): (task[1], task[2]) for task in tasks if task[0] == 'rename'
        }

        for future in tqdm(as_completed(delete_futures), total=len(delete_futures), desc='Deleting files'):
            task = delete_futures[future]
            try:
                file_path, status = future.result()
                # print(f"{file_path} {status}")
            except Exception as e:
                print(f"Error processing {task}: {e}")

        for future in tqdm(as_completed(rename_futures), total=len(rename_futures), desc='Renaming files'):
            task = rename_futures[future]
            try:
                old_path, new_path, status = future.result()
                # print(f"{old_path} to {new_path} {status}")
            except Exception as e:
                print(f"Error processing {task}: {e}")

if __name__ == "__main__":
    main()
 