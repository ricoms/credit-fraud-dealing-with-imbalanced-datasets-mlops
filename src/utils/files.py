import json
import pickle
import tarfile
from abc import ABC, abstractmethod
from io import StringIO
from pathlib import Path
from typing import Dict

import dask.dataframe as dd
import yaml
from dask.dataframe import from_delayed
from dask.delayed import delayed
from pandas import read_csv

from .logger import logger


class BaseFile(ABC):

    @staticmethod
    @abstractmethod
    def read(origin, **kwargs):
        pass

    @staticmethod
    @abstractmethod
    def write(destination, content):
        pass


class ParquetFile(BaseFile):

    @staticmethod
    def read(origin: str, dtypes: Dict[str, str] = None) -> dd.core.DataFrame:
        logger.debug(f"read data from {origin}")
        data = dd.read_parquet(origin, engine='pyarrow')
        if dtypes:
            data.columns = list(dtypes.keys())
            data = data.astype(dtypes)
        return data

    @staticmethod
    def write(destination: str, content: dd.core.DataFrame) -> None:
        logger.debug(f"save data to {destination}")
        content.to_parquet(destination)


class JsonFile(BaseFile):

    @staticmethod
    def read(origin: str, **kwargs) -> dict:
        logger.debug(f"read data from {origin}")
        with open(origin) as file:
            documents = json.load(file)
        return documents

    @staticmethod
    def write(destination: str, content: dict) -> None:
        logger.debug(f"save data to {destination}")
        with open(destination, 'w') as file:
            json.dump(content, file, sort_keys=True, indent=4)

    @staticmethod
    def parse_string(js: str) -> dict:
        logger.debug("parse yaml formatted string to dict")
        documents = json.loads(js)
        return documents


class YAMLFile(BaseFile):

    @staticmethod
    def read(origin: str, **kwargs) -> dict:
        logger.debug(f"read data from {origin}")
        with open(origin) as file:
            documents = yaml.full_load(file)
        return documents

    @staticmethod
    def write(destination: str, content: dict) -> None:
        logger.debug(f"save data to {destination}")
        with open(destination, 'w') as file:
            yaml.dump(content, file)

    @staticmethod
    def parse_string(ys: str) -> dict:
        logger.debug("parse yaml formatted string to dict")
        file = StringIO(ys)
        documents = yaml.full_load(file) or {}
        return documents


class PickleFile(BaseFile):

    @staticmethod
    def read(origin: str, **kwargs) -> dict:
        logger.debug(f"read data from {origin}")
        with open(origin, 'rb') as file:
            documents = pickle.load(file)
        return documents

    @staticmethod
    def write(destination: str, content) -> None:
        logger.debug(f"save data to {destination}")
        with open(destination, 'wb') as file:
            pickle.dump(content, file)


class TarFile:

    @staticmethod
    def uncompress(origin: str, path: str):
        with tarfile.open(origin) as tar:
            tar.extractall(path=path)

    @staticmethod
    def compress(destination: str, content: Dict[str, str]) -> None:
        with tarfile.open(destination, "w:gz") as tar:
            for local_path, tar_path in content.items():
                tar.add(local_path, arcname=tar_path)


def convert_gz2parquet(directory, output_dir, output_format, output_chunk_sizes):
    list_of_files = [f for f in Path(str(directory)).glob("*gz")]
    dfs = [delayed(read_csv)(
            f, sep=';',
            header=None,
            dtype=str,
            compression='gzip'
        ) for f in list_of_files]
    df = from_delayed(dfs)
    npartitions = 1+df.memory_usage().sum().compute() // output_chunk_sizes
    df = df.repartition(npartitions=npartitions)

    logger.info(f"Converting {len(list_of_files)} files into {npartitions} {output_format} files...")
    method_name = "to_" + output_format
    method = getattr(df, method_name)
    method(str(output_dir / f"data.{output_format}"))
    logger.info("...conversion done.")
