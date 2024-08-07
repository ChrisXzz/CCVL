# -*- coding: utf-8 -*-
import os
import shutil
import pandas as pd
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count
from tqdm import tqdm

def rename_folder(task):
    source_folder, destination_folder = task
    shutil.copytree(source_folder, destination_folder)
    return os.path.basename(source_folder), os.path.basename(destination_folder)

def rename_folders(source_path, destination_path, prefix="BDMAP_", start_number=9902):
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)

    folders = [f for f in os.listdir(source_path) if os.path.isdir(os.path.join(source_path, f))]
    folders.sort()  # Sorting to maintain order

    tasks = []
    for i, folder in enumerate(folders):
        new_name = f"{prefix}{start_number + i:08d}"
        source_folder = os.path.join(source_path, folder)
        destination_folder = os.path.join(destination_path, new_name)
        tasks.append((source_folder, destination_folder))

    return tasks

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source_path', required=True, help='The source directory containing the folders to rename.')
    parser.add_argument('--destination_path', required=True, help='The destination directory to save the renamed folders.')
    parser.add_argument('--prefix', default='BDMAP_', help='The prefix for the new folder names.')
    parser.add_argument('--start_number', type=int, required=True, help='The starting number for the new folder names.')
    args = parser.parse_args()

    tasks = rename_folders(args.source_path, args.destination_path, args.prefix, args.start_number)

    print('>> {} CPU cores are secured.'.format(cpu_count()))
    rename_mapping = []

    with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
        futures = {executor.submit(rename_folder, task): task for task in tasks}

        for future in tqdm(as_completed(futures), total=len(futures), desc='Renaming and copying folders'):
            task = futures[future]
            try:
                original_name, new_name = future.result()
                rename_mapping.append((original_name, new_name))
                # print(f"Copied {original_name} to {new_name}")
            except Exception as e:
                print(f"Error processing {task}: {e}")

    # Save the mapping to an Excel file
    df = pd.DataFrame(rename_mapping, columns=['Original Name', 'New Name'])
    excel_path = os.path.join(args.destination_path, "rename_id_mapping.xlsx")
    df.to_excel(excel_path, index=False)

    print(f"Renamed {len(rename_mapping)} folders and saved to {args.destination_path}")
    print(f"Mapping saved to {excel_path}")

if __name__ == "__main__":
    main()
