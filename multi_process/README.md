Some explanations
1. normalize_V2.py: code for fixing "orthonormal direction cosines" error in AbdomenAtlas1.0 dataset, and adjusting the direction of the AbdomenAtlas1.0 dataset to RPS. 

2. totalsegmentator_V2.py: code for reorganizing 16_TotalSegmentor dataset.  
Note: Rename "gallbladder.nii.gz" to "gall_bladder.nii.gz";  
Rename "small_bowel.nii.gz" to "intestine.nii.gz".  
Combine "lung_lower_lobe_left.nii.gz" and "lung_upper_lobe_left.nii.gz" into "lung_left.nii.gz", and also keep the origianl files before combination;  
Combine "lung_middle_lobe_right.nii.gz", "lung_lower_lobe_right.nii.gz", and "lung_upper_lobe_right.nii.gz" into "lung_right.nii.gz", and also keep the original files before combination.

3. pancreas_V2.py: code for reorganizing 15_Pancreas dataset.

4. AutoPET_V2.py: code for reorganizing 19_AutoPet_Nifti dataset.

5. ctspine1k_V2.py: code for reorganizing 21_CTSpine1K dataset.
