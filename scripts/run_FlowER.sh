#!/bin/bash

module load anaconda3/2024.02-1-11.4
. "$(conda info --base)/etc/profile.d/conda.sh"
conda activate data-disc

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PROJECT_ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
FLOWER_REPO="$PROJECT_ROOT/external/FlowER-repo"

[ -d "$FLOWER_REPO" ] || { echo "FlowER repository not found: $FLOWER_REPO" >&2; exit 1; }

cd "$FLOWER_REPO" || exit 1

export DATA_NAME="flower_new_dataset"
export EXP_NAME="best_large_hyperparam"
export EMB_DIM=256
export RBF_HIGH=12
export RBF_GAP=0.1
export SIGMA=0.15

export MODEL_NAME="model.2940000_97.pt" # your checkpoint file

export TRAIN_BATCH_SIZE=8192
export VAL_BATCH_SIZE=8192
export TEST_BATCH_SIZE=2048

export NUM_WORKERS=8
export CUDA_VISIBLE_DEVICES="${CUDA_VISIBLE_DEVICES:-0}"
export NUM_GPUS_PER_NODE="${NUM_GPUS_PER_NODE:-1}"
export NUM_NODES=1
export NODE_RANK=0
export MASTER_ADDR=localhost
export MASTER_PORT=1235

export TRAIN_FILE="$PROJECT_ROOT/models/FlowER/data/$DATA_NAME/train.txt"
export VAL_FILE="$PROJECT_ROOT/models/FlowER/data/$DATA_NAME/val.txt"
export TEST_FILE="$PROJECT_ROOT/models/FlowER/data/$DATA_NAME/test.txt"
#export TEST_FILE="$PROJECT_ROOT/models/FlowER/data/$DATA_NAME/beam.txt"

export MODEL_PATH="$PROJECT_ROOT/models/FlowER/checkpoints/$DATA_NAME/$EXP_NAME/"
RUN_ID="${SLURM_JOB_ID:-$(date +%Y%m%d_%H%M%S)_$$}"
export RESULT_PATH="$PROJECT_ROOT/results/$DATA_NAME/$EXP_NAME/run-$RUN_ID/"
mkdir -p "$RESULT_PATH"

[ -f "$TEST_FILE" ] || { echo "Test file not found: $TEST_FILE" >&2; exit 1; }
[ -f "$MODEL_PATH/$MODEL_NAME" ] || {
    echo "Checkpoint not found: $MODEL_PATH/$MODEL_NAME" >&2
    exit 1
}

export SCALE=1 # larger sample size during testing
bash scripts/eval_multiGPU.sh
# bash scripts/search.sh