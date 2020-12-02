import argparse
import configparser
import datetime
import os
import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict


class ArgParser(ABC):

    def __init__(self):
        self.environment = os.environ.get("ENVIRON", "DOCKER")

        config = configparser.ConfigParser()
        config.read(self.configuration_file_path)

        for key, value in config[self.environment].items():
            os.environ[key.upper()] = value

        self.run_tag = datetime.datetime \
            .fromtimestamp(time.time()) \
            .strftime('%Y-%m-%d-%H%M%S')

    @property
    def configuration_file_path(self) -> str:
        return "config.ini"

    @property
    def hyperparameters_file_name(self) -> str:
        return "hyperparameters.json"

    @abstractmethod
    def get_arguments(self) -> Dict[str, Any]:
        pass


class TrainArgParser(ArgParser):

    def get_arguments(self) -> Dict[str, Any]:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--input_dir",
            type=Path,
            default=Path(os.environ["SM_INPUT_DIR"]),
        )
        parser.add_argument(
            "--output_dir",
            type=Path,
            default=Path(os.environ["SM_OUTPUT_DIR"]),
        )
        parser.add_argument(
            '--project_name',
            default="",
            type=str,
            help="Project name (default: '')",
        )
        parser.add_argument(
            '--run_tag',
            default=self.run_tag,
            type=str,
            help=f"Run ID (default: '{self.run_tag}')",
        )
        args = parser.parse_args()

        return args


class APIArgParser(ArgParser):

    def get_arguments(self) -> Dict[str, Any]:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--model_dir",
            type=Path,
            default=Path(os.environ["SM_OUTPUT_DIR"]),
        )
        parser.add_argument(
            "--model_name",
            default="customer-lifetime-values",
            type=str,
            help="Project name",
        )
        parser.add_argument(
            "--num_cpus",
            type=int,
            default=os.environ["SM_NUM_CPUS"],
        )
        parser.add_argument(
            "--model_server_timeout",
            default=60,
            type=int,
            help="Number of model server workers (default: 60)",
        )
        parser.add_argument(
            "--run_tag",
            default=self.run_tag,
            type=str,
            help=f"Run ID (default: \"{self.run_tag}\")",
        )
        args = parser.parse_args()

        return args
