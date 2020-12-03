import signal
import subprocess
import sys
from dataclasses import dataclass
from os import kill, wait

from .logger import logger


@dataclass
class GunicornServe:
    model_dir: str
    model_server_workers: int
    model_server_timeout: int

    def __sigterm_handler(self, nginx_pid=None, gunicorn_pid=None):
        if nginx_pid is not None:
            try:
                kill(nginx_pid, signal.SIGQUIT)
            except OSError:
                pass
        if gunicorn_pid is not None:
            try:
                kill(gunicorn_pid, signal.SIGTERM)
            except OSError:
                pass

        sys.exit(0)

    def start_server(self):
        logger.info(
            f"Starting the inference server with {self.model_server_workers} workers."
        )

        nginx = subprocess.Popen([
            "nginx", "-c", "/opt/program/api/conf/nginx.conf"
        ])

        gunicorn = subprocess.Popen([
            "gunicorn",
            "--timeout", str(self.model_server_timeout),
            "-k", "tornado",
            "-b", "unix:/tmp/gunicorn.sock",
            "-w", str(self.model_server_workers),
            f'api.app:MLAPI("{self.model_dir}").setup()',
        ])

        pids = {
            "nginx_pid": nginx.pid,
            "gunicorn_pid": gunicorn.pid,
        }

        signal.signal(
            signal.SIGTERM,
            lambda a, b: self.__sigterm_handler(**pids)
        )

        # If either subprocess exits, so do we.
        pids_set = set(pids.values())
        while True:
            pid, _ = wait()
            if pid in pids_set:
                break

        self.__sigterm_handler(**pids)

        logger.info("Inference server exiting")
