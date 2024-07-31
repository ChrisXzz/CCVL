#### Calculate DSC and NSD of SuPreM and SegResNet inference results
###### Please modify seg_path, gt_path, save_path and save_name to meet your needs. To be specific,

seg_path: path that store your SuPreM or SegResNet inference results, the folder structure should be 
```
- Your_Inference_Result/
  - case1/
    - combined_labels.nii.gz
    - probabilities/
      - mask1.nii.gz
      ...
      - 
    - segmentations/
      - mask1.nii.gz
      ...
      - 
  - case2/
    - combined_labels.nii.gz
    - probabilities/
      - mask1.nii.gz
      ...
      - 
    - segmentations/
      - mask1.nii.gz
      ...
      - 
  - case3/
    - combined_labels.nii.gz
    - probabilities/
      - mask1.nii.gz
      ...
      - 
    - segmentations/
      - mask1.nii.gz
      ...
      - 
```

gt_path: path that store your groundtruth, groundtruth should be organized like the following folder structure:
```
- Your_Groundtruth/
  - case1/
    - combined_labels.nii.gz
    - ct.nii.gz
    - segmentations/
      - mask1.nii.gz
      ...
      - 
  - case2/
    - combined_labels.nii.gz
    - ct.nii.gz
    - segmentations/
      - mask1.nii.gz
      ...
      - 
  - case3/
    - combined_labels.nii.gz
    - ct.nii.gz
    - segmentations/
      - mask1.nii.gz
      ...
      - 
```
save_path: path that save your DSC and NSD results

save_name: the prefered name of csv file that contains DSC and NSD results
