#### STEP 0. Setup


###### STEP 0.1 Create a virtual environment (optional)

```bash
conda create -n suprem python=3.8
source activate suprem
```

###### STEP 0.2 Clone the GitHub repository

```bash
git clone https://github.com/MrGiovanni/SuPreM
cd SuPreM/
pip install torch==1.11.0+cu113 torchvision==0.12.0+cu113 torchaudio==0.11.0 --extra-index-url https://download.pytorch.org/whl/cu113
pip install monai[all]==0.9.0
pip install -r requirements.txt
```

###### STEP 0.3 Download the pre-trained checkpoints

```bash
cd target_applications/pancreas_tumor_detection/pretrained_weights/
wget https://huggingface.co/MrGiovanni/SuPreM/resolve/main/supervised_suprem_swinunetr_2100.pth
wget https://huggingface.co/MrGiovanni/SuPreM/resolve/main/supervised_suprem_segresnet_2100.pth
wget https://huggingface.co/MrGiovanni/SuPreM/resolve/main/supervised_suprem_unet_2100.pth
cd ../
```


#### STEP 1. Create datalists for cross validation
###### Download cv_datalist.py to the following path: SuPreM/target_applications/pancreas_tumor_detection/dataset/dataset_list/
###### Download cross_validation.sh, and shell_scripts_cv folder to the following path: SuPreM/target_applications/pancreas_tumor_detection/
###### Modify the datalist_dir to the actual path
###### Create datalists for cross validation
```bash
python ./dataset/dataset_list/cv_datalist.py --input_file1 ./dataset/dataset_list/jhh_train.txt --input_file2 ./dataset/dataset_list/jhh_test.txt --output_dir ./dataset/dataset_list/
```

#### STEP 2. Run cross validation
```bash
bash cross_validation.sh
```
