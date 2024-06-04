import os
import pydicom
import dicom2nifti
import shutil
import dicom2nifti.settings as settings

settings.disable_validate_slice_increment()
base_dicom_dir = '/Volumes/PortableSSD/TODO/OralContrast'
base_output_dir = '/Volumes/PortableSSD/TODO/OralContrast_reorganized/out'
temp_dir = '/Volumes/PortableSSD/TODO/OralContrast_reorganized/temp'

if not os.path.exists(base_output_dir):
    os.makedirs(base_output_dir)
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

def clear_temp_dir(temp_dir):
    for file in os.listdir(temp_dir):
        file_path = os.path.join(temp_dir, file)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
            
# 遍历总路径下的所有子文件夹的子文件夹
for subfolder in os.listdir(base_dicom_dir):
    first_level_dir = os.path.join(base_dicom_dir, subfolder)
    if not os.path.isdir(first_level_dir):
        continue

    for second_subfolder in os.listdir(first_level_dir):
        dicom_dir = os.path.join(first_level_dir, second_subfolder)
        if not os.path.isdir(dicom_dir):
            continue

        try:
            dicom_files = [f for f in os.listdir(dicom_dir) if os.path.isfile(os.path.join(dicom_dir, f))]

            # 使用字典存储每个 SeriesInstanceUID 对应的文件列表
            series_files = {}

            for dicom_file in dicom_files:
                ds = pydicom.dcmread(os.path.join(dicom_dir, dicom_file), force=True)

                if "SeriesInstanceUID" in ds:
                    uid = ds.SeriesInstanceUID
                    if uid not in series_files:
                        series_files[uid] = []
                    series_files[uid].append(os.path.join(dicom_dir, dicom_file))

            for uid, files in series_files.items():
                # 创建临时文件夹
                if not os.path.exists(temp_dir):
                    os.makedirs(temp_dir)

                # 复制所有文件到临时文件夹
                for file in files:
                    shutil.copy(file, temp_dir)

                # 将临时文件夹中的文件转换为 NIfTI
                dicom2nifti.convert_directory(temp_dir, temp_dir, compression=True, reorient=True)

                # 为输出的 NIfTI 文件创建文件名，包括总路径文件夹名、子文件夹名和子文件夹的子文件夹名
                for file_name in os.listdir(temp_dir):
                    if file_name.endswith('.nii.gz'):
                        new_name = f"{os.path.basename(base_dicom_dir)}_{os.path.basename(first_level_dir)}_{os.path.basename(dicom_dir)}_Depth_{len(files)}_{file_name}"
                        shutil.move(os.path.join(temp_dir, file_name), os.path.join(base_output_dir, new_name))

                print(f"Converted SeriesInstanceUID: {uid} with {len(files)} files. Output to {base_output_dir}")

                # 清空临时文件夹
                clear_temp_dir(temp_dir)

        except Exception as e:
            print(f"Error processing folder '{dicom_dir}': {e}")
