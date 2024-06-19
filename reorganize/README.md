Step 1. Preprocessing your dataset to match the following folder structure to the following folder structure
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

Step 2. Run contrast_norm.py to adjust the constrast value into (-1000, 1000) of your ct images (ct.nii.gz)
```
python 
```
Step 3. Run normalize_V2.py to restore potential cosine error in ct images and adjust its corresponding 3D direction to RPS

Step 4. Run check_image_type_V2.py to ensure datatype of ct image to be int16 and datatype of mask file to be int8
