####  This code can be used for post-processing inference results and then calculating the specificity.

###### Directly run
```bash
python specificity_processing.py --input_dir [The path you store your inference results] --output_dir [The path you want to save your post-processing results] --gt_csv [The csv file that contains groundtruth information] --min_radius [The smallest tumor size you want to detect] --dataset [The dataset name you want to process]
```
