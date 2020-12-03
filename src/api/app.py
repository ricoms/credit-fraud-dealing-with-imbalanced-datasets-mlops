import inspect
from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import experiment
import falcon
from utils.logger import logger

from api.resources import HealthCheckResource, PredictionService

logger.info('Starting server.')


@dataclass
class MLAPI:
    model_dir: str

    def __get_models(self) -> Dict[str, experiment.MLModel]:
        models = inspect.getmembers(
            experiment,
            lambda cls:
                inspect.isclass(cls) and not inspect.isabstract(cls)
        )
        return dict(models)

    def __extend_api(self):
        logger.info("Set /health-check/liveness route")
        self.api.add_route(
            '/health-check/liveness',
            HealthCheckResource()
        )
        logger.info("Set /invocations route")
        models = self.__get_models()
        self.api.add_route(
            '/invocations',
            PredictionService(
                models,
                Path(self.model_dir),
            )
        )
        logger.info("Set /ping route")
        self.api.add_route(
            '/ping',
            HealthCheckResource()
        )

    def setup(self):
        logger.info('Starting server.')
        self.api = falcon.API()
        self.__extend_api()
        return self.api


def app():
    return MLAPI("/opt/ml/output").setup()