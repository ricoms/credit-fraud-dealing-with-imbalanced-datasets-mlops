from pathlib import Path

from experiment.artifacts import ExperimentArtifacts
from experiment.experiment import Experiment
from experiment.model import ProjectModel


class TestModel:

    def test_model_id(self):
        o = ProjectModel()
        assert o.model_id == "divorce"

    def test_save(self, tmp_path):
        dataset_path = Path('ml/input/test/sample.csv')
        o = ProjectModel()
        artifacts_handler = ExperimentArtifacts(
            run_tag='test',
            model_name=o.model_id,
            base_path=tmp_path,
        )
        e = Experiment(
            model=o,
            input_dir=dataset_path,
            artifacts_handler=artifacts_handler,
        )
        e.run()
        assert o.model_path.is_file()

    def test_load(self, tmp_path):
        dataset_path = Path('ml/input/data/sample.csv')
        o = ProjectModel()
        artifacts_handler = ExperimentArtifacts(
            run_tag='test',
            model_name=o.model_id,
            base_path=tmp_path,
        )
        e = Experiment(
            model=o,
            input_dir=dataset_path,
            artifacts_handler=artifacts_handler,
        )
        e.run()
        o2 = ProjectModel()
        o2.load(tmp_path)
        model = o.model
        model_ = o2.model
        assert type(model_) == type(model)  # must return the same type of object
        assert model_ is not model          # object identity MUST be different

    def test_predict(self, tmp_path):
        dataset_path = Path('ml/input/data/sample.csv')
        o = ProjectModel()
        artifacts_handler = ExperimentArtifacts(
            run_tag='test',
            model_name=o.model_id,
            base_path=tmp_path,
        )
        e = Experiment(
            model=o,
            input_dir=dataset_path,
            artifacts_handler=artifacts_handler,
        )
        e.run()
        p = o.predict(
            ids=["1"],
            X=["2;2;4;1;0;0;0;0;0;0;1;0;1;1;0;1;0;0;0;1;0;0;0;0;0;0;0;0;0;1;1;2;1;2;0;1;2;1;3;3;2;1;1;2;3;2;1;3;3;3;2;3;2;1;1".split(";")[:-1]],  # noqa: E501
        )
        assert "1" in p
        assert p["1"] in [0.0, 1.0]