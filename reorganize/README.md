#### STEP 0. Set up.



#### STEP 1. Preprocessing your dataset to match the following folder structure.
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

#### STEP 2. Run contrast_norm.py to adjust the constrast value into (-1000, 1000) of your ct images (ct.nii.gz). Modify the "directory" to [Your_Dataset_Dir].
```
python contrast_norm.py --directory [Your_Dataset_Dir]
```
#### STEP 3. Run normalize_V2.py to restore potential cosine error in ct images and adjust its corresponding 3D direction to RPS. Modify the "data_path" to [Your_Dataset_Dir] and modify the "save_dir" to [Your_Processed_Dataset_Dir].
```
python normalize.py --data_path [Your_Dataset_Dir] --save_dir [Your_Processed_Dataset_Dir]
```

#### STEP 4. Run check_image_type_V3.py to ensure datatype of ct image to be int16 and datatype of mask file to be int8. Modify the "base_folder" to [Your_Processed_Dataset_Dir].
```
pyhthon check_image_type.py --base_folder [Your_Processed_Dataset_Dir]
```

#### STEP 5. Run id_map.py to rename cases in dataset to ID_MAP style. Modify the "source_path" to [Your_Processed_Dataset_Dir]. Modify the "destination_path" to [Your_ID_MAP_Dir]. Modify "start_number" to the number you want to start coding.
```
python id_maps.py --source_path [Your_Processed_Dataset_Dir] --destination_path [Your_ID_MAP_Dir] --start_number [Number you want to start coding]
```

#### Dataset waiting for reorganizing
```bash
ULS23
```
