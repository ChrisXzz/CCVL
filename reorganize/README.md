Step 1. Preprocessing your dataset to match the following folder structure

Step 2. Run xxx.py to reorganize your dataset to the following folder structure

Step 3. Run xxx.py to adjust the constrast value into (-1000, 1000) of your ct images (ct.nii.gz)

Step 4. Run normalize_V2.py to restore potential cosine error in ct images and adjust its corresponding 3D direction to RPS

Step 5. Run check_image_type_V2.py to ensure datatype of ct image to be int16 and datatype of mask file to be int8
