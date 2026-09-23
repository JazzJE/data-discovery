from pathlib import Path

class Config:
    class FolderPaths:
        ROOT = Path(__file__).resolve().parent

        DATA_DIR = ROOT / "data"
        SRC_DIR = ROOT / "src"

        INORGANIC_DATA_DIR = DATA_DIR / "Inorganic Impurity Dataset"
        INORGANIC_DATASET = INORGANIC_DATA_DIR / "SS_rxns_80806_dupremoved.json"