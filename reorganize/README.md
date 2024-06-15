Step 1. Preprocessing your dataset to match the following folder structure in two different folders
- Your_CT_images_Dir_folder/
  - case1_ct.nii.gz
  - case2_ct.nii.gz
  - case3_ct.nii.gz
  - ...
- Your_Mask_Dir_folder/
  - case1_mask.nii.gz
  - case2_mask_nii.gz
  - case3_mask_nii.gz
  - ...

Step 2. Run xxx.py to reorganize your dataset to the following folder structure
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

Step 3. Run contrast_norm.py to adjust the constrast value into (-1000, 1000) of your ct images (ct.nii.gz)

Step 4. Run normalize_V2.py to restore potential cosine error in ct images and adjust its corresponding 3D direction to RPS

Step 5. Run check_image_type_V2.py to ensure datatype of ct image to be int16 and datatype of mask file to be int8
