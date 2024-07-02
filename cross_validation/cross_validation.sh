ARCH="segresnet"

PRETRAINED_MODEL="pretrained_weights/supervised_suprem_segresnet_2100.pth"

BATCH_SIZE=8

NUM_SAMPLES=4

NUM_GPUS=8

LOG_FILE="logs/segresnet.jhh.txt"

for i in {0..4}
do
  echo "Training fold $i..."
  bash shell_scripts_cv/step1.train.multigpu.sh $ARCH $PRETRAINED_MODEL $BATCH_SIZE $NUM_SAMPLES dataset_lists/jhh_train_fold_${i}.txt $i >> $LOG_FILE

  echo "Inference fold $i..."
  bash shell_scripts_cv/step2.inference.multigpu.sh $ARCH out/$ARCH.jhh.fold_$i/model.pth $ARCH.jhh $NUM_GPUS dataset_lists/jhh_test_fold_${i}.txt $i >> $LOG_FILE

  echo "Evaluation fold $i..."
  bash shell_scripts_cv/step3.eval.sh inference/$ARCH.jhh.fold_$i /data/zzhou82/data/JHH_ROI_0.5mm $ARCH.jhh $i >> $LOG_FILE
done
