import os
import shutil
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count
from tqdm import tqdm
import argparse

def process_case(case_file, img_path, label_path, label_6cls_path, destination_path):
    """处理单个案例文件，复制并重命名到目标路径"""
    # 获取文件名（去除扩展名和.nii）
    case_name = os.path.splitext(case_file)[0]
    if case_name.endswith(".nii"):
        case_name = case_name[:-4]  # 移除 .nii 扩展名

    # 定义案例文件夹路径
    case_folder_name = "OUT_" + case_name
    case_folder_path = os.path.join(destination_path, case_folder_name)
    segmentations_path = os.path.join(case_folder_path, "segmentations")
    
    # 创建案例文件夹和segmentations子文件夹
    os.makedirs(segmentations_path, exist_ok=True)
    
    # 获取每个案例的文件路径
    img_file_path = os.path.join(img_path, case_file)
    label_file_path = os.path.join(label_path, case_file)
    label_6cls_file_path = os.path.join(label_6cls_path, case_file)
    
    # 定义重命名后的文件路径
    new_img_file_path = os.path.join(case_folder_path, "ct.nii.gz")
    new_label_file_path = os.path.join(segmentations_path, case_file)
    new_label_6cls_file_path = os.path.join(segmentations_path, "6cls_" + case_file)
    
    # 复制并重命名文件
    shutil.copy2(img_file_path, new_img_file_path)
    shutil.copy2(label_file_path, new_label_file_path)
    shutil.copy2(label_6cls_file_path, new_label_6cls_file_path)

    return case_file

def main():
    parser = argparse.ArgumentParser(description="Reorganize and copy medical image datasets.")
    parser.add_argument('--base_path', default = 'F:\\OUT', help='The base path containing the img, label, and label_6cls folders.')
    parser.add_argument('--destination_path', default = 'F:\\out_reorganized', help='The destination path where reorganized files will be saved.')
    args = parser.parse_args()

    img_path = os.path.join(args.base_path, "img")
    label_path = os.path.join(args.base_path, "label")
    label_6cls_path = os.path.join(args.base_path, "label_6cls")
    destination_path = args.destination_path

    case_files = os.listdir(img_path)

    print('>> {} CPU cores are secured.'.format(cpu_count()))
    with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
        futures = {executor.submit(process_case, case_file, img_path, label_path, label_6cls_path, destination_path): case_file for case_file in case_files}

        for future in tqdm(as_completed(futures), total=len(futures), desc='Processing files'):
            case_file = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"Error processing {case_file}: {e}")

if __name__ == "__main__":
    main()

