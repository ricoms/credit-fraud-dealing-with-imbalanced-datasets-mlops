import traceback
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

from utils.files import TarFile
from utils.logger import logger


@dataclass
class ExperimentArtifacts:
    run_tag: str
    model_name: str
    base_path: Path

    def _create_if_not_exist(self):
        Path(self.output_prefix).mkdir(parents=True, exist_ok=True)

    @property
    def output_prefix(self):
        return self.base_path / self.model_name

    def get_artifacts(self, artifacts: Dict[str, Any]):
        self.metrics = artifacts.get("metrics")
        self.images = artifacts.get("images")

    def save_results(self):
        self._create_if_not_exist()

        if self.metrics:
            metrics_path = str(self.output_prefix / 'metrics.txt')
            with open(metrics_path, 'w') as outfile:
                for k, v in self.metrics.items():
                    outfile.write(f"{k}: {v:.3f}\n")

        if self.images:
            for (name, figure) in self.images.items():
                file_name = self.output_prefix / f"{name}.png"
                logger.debug(f"Saving {file_name}")
                figure.savefig(file_name)

    def save(self):
        self.save_results()

    # Create single output package
    @property
    def model_package_path(self):
        return self.base_path / 'model.tar.gz'

    def create_package_with_models(self):
        logger.info(f"Loading models from {self.base_path}")
        model_paths = {}
        for p in sorted(self.base_path.glob("**/*joblib")):
            tar_path = f"{p.parent.name}/{p.name}"
            model_paths[str(p)] = tar_path
        TarFile.compress(self.model_package_path, model_paths)

    def training_error(self, error) -> None:
        # Write out an error file. This will be returned as the failureReason in the
        # DescribeTrainingJob result.
        trc = traceback.format_exc()
        with open(self.output_prefix / "failure", "w") as s:
            s.write("Exception during training: " + str(error) + "\n" + trc)
        # Printing this causes the exception to be in the training job logs, as well.
        logger.info("Exception during training: " + str(error) + "\n" + trc)
