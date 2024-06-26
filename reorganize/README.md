Step 1. Preprocessing your dataset to match the following folder structure.
```
- Your_Dataset_reorganized_Dir/
  - case1/
    - segmentations/
    - ct.nii.gz
  - case2/
    - segmentations/
    - ct.nii.gz
  - case3/
    - segmentations/
    - ct.nii.gz
  - ...
```

Step 2. Run contrast_norm.py to adjust the constrast value into (-1000, 1000) of your ct images (ct.nii.gz). Modify the "directory" to [Your_Dataset_Dir].
```
python contrast_norm.py
```
Step 3. Run normalize_V2.py to restore potential cosine error in ct images and adjust its corresponding 3D direction to RPS. Modify the "data_path" to [Your_Dataset_Dir] and modify the "save_dir" to [Your_Processed_Dataset_Dir].
```
python normalize_V2.py
```

Step 4. Run check_image_type_V3.py to ensure datatype of ct image to be int16 and datatype of mask file to be int8. Modify the "base_folder" to [Your_Processed_Dataset_Dir].
```
pyhthon check_image_type_V3.py
```

Step 5. Run id_map.py to rename cases in dataset to ID_MAP style. Modify the "source_path" to [Your_Processed_Dataset_Dir]. Modify the "destination_path" to [Your_ID_MAP_Dir]. Modify "start_number" to the number you want.
```
python id_maps.py
```
