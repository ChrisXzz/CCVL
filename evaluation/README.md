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
  ...
```

gt_path: path that store your groundtruth, groundtruth should be organized like the following folder structure:
###### For JHU student, you can find groundtruth in /ccvl/net/ccvl15/zzhou82/data/JHH_ROI_0.5mm
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
  ...
```
save_path: path that save your DSC and NSD results to

save_name: the prefered name of excel file that contains DSC and NSD results

Before you start calculating, make sure that you have removed the following cases from your inference results.
```
'FELIX-Cys-1432', 'FELIX5145', 'FELIX-CYS-1289', 'FELIX7528', 'FELIX-Cys-1680', 'FELIX-Cys-1222', 'FELIX7594', 'FELIX5222', 'FELIX5224', 'FELIX-PDAC-1174', 'FELIX7179', 'FELIX5544', 'FELIX7521', 'FELIX-Cys-1632', 'FELIX-Cys-1623', 'FELIX-Cys-1233', 'FELIX5046'
```
