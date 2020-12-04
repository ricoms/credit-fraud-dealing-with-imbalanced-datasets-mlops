import sys
from dataclasses import dataclass
from io import StringIO
from pathlib import Path
from typing import Any

import numpy as np
from sklearn.model_selection import StratifiedKFold
from utils.logger import logger

from .artifacts import ExperimentArtifacts

INPUT_COLUMNS = [
    "Time", "V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9",
    "V10", "V11", "V12", "V13", "V14", "V15", "V16", "V17", "V18", "V19", "V20",
    "V21", "V22", "V23", "V24", "V25", "V26", "V27", "V28", "Amount", "Class",
]


@dataclass
class Experiment:
    run_tag: str
    model: Any
    input_dir: Path
    artifacts_handler: ExperimentArtifacts
    training_portion: float = .8
    random_state: int = 42

    def load_data(self):
        with open(self.input_dir, 'r') as file:
            data = file.read().replace('"', '')
        data = np.genfromtxt(StringIO(data), delimiter=',', skip_header=1)  # , dtype=None
        self.artifacts_handler.profile(data, INPUT_COLUMNS)
        self.X, self.y = data[:, :-1], data[:, -1]
        shape0 = self.y.shape[0]
        bin_counts = np.bincount(self.y.astype(np.int32))
        number_no_frauds = round(bin_counts[0]/shape0 * 100, 2)
        number_frauds = round(bin_counts[1]/shape0 * 100, 2)

        logger.info(f'Number of instances of the dataset: {shape0}')
        logger.info(f'No Frauds {number_no_frauds} of the dataset')
        logger.info(f'Frauds {number_frauds} of the dataset')

    def split_data(self):
        self.sss = StratifiedKFold(n_splits=5, random_state=None, shuffle=False)

    def train(self):
        accuracy_lst = []
        precision_lst = []
        recall_lst = []
        f1_lst = []
        auc_lst = []

        for train, validation in self.sss.split(self.X, self.y):
            self.model.train(
                self.X[train],
                self.y[train],
            )
            acc, precision, recall, f1, auc = self.model.evaluate(
                self.X[validation],
                self.y[validation],
            )
            accuracy_lst.append(acc)
            precision_lst.append(precision)
            recall_lst.append(recall)
            f1_lst.append(f1)
            auc_lst.append(auc)

        visual_results = self.model.gen_plots(
            self.X[validation],
            self.y[validation],
        )
        artifacts = {
            "metrics": {
                "avg_accuracy": np.mean(accuracy_lst),
                "avg_precision": np.mean(precision_lst),
                "avg_recall": np.mean(recall_lst),
                "avg_f1": np.mean(f1_lst),
                "avg_auc": np.mean(auc_lst),
            },
            "images": visual_results,
        }

        logger.info(artifacts)
        return artifacts

    def save(self):
        self.artifacts_handler.save()
        self.model.save(self.artifacts_handler.output_prefix)

    def run(self):
        logger.info(f"Begin Experiment {self.run_tag} for model {self.model.model_id}.")
        self.load_data()
        self.split_data()
        try:
            artifacts = self.train()
        except Exception as e:
            self.artifacts_handler.training_error(e)
            sys.exit(255)

        self.artifacts_handler.get_artifacts(
            artifacts
        )
        self.save()
        self.artifacts_handler.create_package_with_models()
