# data-discovery

# Models
* [ReactionT5](huggingface.co/sagawa/ReactionT5v2-forward)
	- Expects molecular SMILES in the format `REACTANT:<reactant_smiles>REAGENT:<reagent_smiles>`.
	- Separate multiple molecules with `.` and predicts product SMILES from the reactants and reagents.
	- The FlowER records and impurity dataset formulas, such as `Li2CO3` and `ZrO2`, are not directly valid ReactionT5 inputs because they are chemical formulas rather than molecular SMILES.
* [FlowER](github.com/FongMunHong/FlowER)
	- To retrain/reproduce FlowER, download `data.zip` and `checkpoints.zip` from [this link](https://doi.org/10.6084/m9.figshare.32513667), unzip them, and place under `FlowER/`.
	- The folder structure for the `data` folder is `data/{DATASET_NAME}/{train,val,test}.txt` and `checkpoints` folder is `checkpoints/{DATASET_NAME}/{EXPERIMENT_NAME}/model.{STEP}_{IDX}.pt`.

## Run FlowER

FlowER requires Linux/WSL, Python 3.10, and a CUDA-enabled GPU. Run these commands from the repository root.

### 1. Create the environment

```bash
conda create -n flower python=3.10
conda activate flower
pip install -r requirements.txt
```

The root-level `requirements.txt` contains the packages required by both ReactionT5 and FlowER, so a separate FlowER environment or dependency file is not needed.

The included dataset and checkpoint should be arranged as follows:

```text
models/FlowER/data/flower_new_dataset/{train,val,test,beam}.txt
models/FlowER/checkpoints/flower_new_dataset/best_large_hyperparam/model.2940000_97.pt
```

No Windows junctions or manually edited absolute paths are required. The launcher resolves paths relative to the repository itself.

### 2. Run inference on the test set

```bash
bash external/FlowER-repo/run_FlowER_large_newData.sh
```

Results are written to `results/flower_new_dataset/best_large_hyperparam/`.

To select specific GPUs or change the GPU count, set these variables before running the launcher:

```bash
export CUDA_VISIBLE_DEVICES=0
export NUM_GPUS_PER_NODE=1
bash external/FlowER-repo/run_FlowER_large_newData.sh
```

### 3. Run beam search

Put non-atom-mapped reactions in `models/FlowER/data/flower_new_dataset/beam.txt`, using this format:

```text
reactants>>product1|product2
```

`beam.txt` is an inference-only input for beam search. It is separate from `train.txt`, `val.txt`, and `test.txt`, which are used for model training and evaluation.

In `external/FlowER-repo/run_FlowER_large_newData.sh`, comment out the test-set line and enable the beam file and search command:

```bash
# export TEST_FILE="$PROJECT_ROOT/models/FlowER/data/$DATA_NAME/test.txt"
export TEST_FILE="$PROJECT_ROOT/models/FlowER/data/$DATA_NAME/beam.txt"
# sh scripts/eval_multiGPU.sh
sh scripts/search.sh
```

Then run:

```bash
bash external/FlowER-repo/run_FlowER_large_newData.sh
```

# Data:
* [Inorganic Impurity Dataset](https://figshare.com/articles/dataset/Text-mined_dataset_of_solid-state_syntheses_with_impurity_phases_using_Large_Language_Model/30423274)
* The Open Reaction Database
* USPTO
