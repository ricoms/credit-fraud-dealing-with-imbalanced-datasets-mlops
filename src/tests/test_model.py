from pathlib import Path

from experiment.artifacts import ExperimentArtifacts
from experiment.experiment import Experiment
from experiment.model import ProjectModel


class TestModel:

    def test_model_id(self):
        o = ProjectModel()
        assert o.model_id == "credit-card-fraud"

    def test_save(self, tmp_path):
        dataset_path = Path('ml/input/test/sample.csv')
        o = ProjectModel()
        artifacts_handler = ExperimentArtifacts(
            run_tag='test',
            model_name=o.model_id,
            base_path=tmp_path,
        )
        e = Experiment(
            run_tag='test',
            model=o,
            input_dir=dataset_path,
            artifacts_handler=artifacts_handler,
        )
        e.run()
        assert o.model_path.is_file()

    def test_load(self, tmp_path):
        dataset_path = Path('ml/input/test/sample.csv')
        o = ProjectModel()
        artifacts_handler = ExperimentArtifacts(
            run_tag='test',
            model_name=o.model_id,
            base_path=tmp_path,
        )
        e = Experiment(
            run_tag='test',
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
        dataset_path = Path('ml/input/test/sample.csv')
        o = ProjectModel()
        artifacts_handler = ExperimentArtifacts(
            run_tag='test',
            model_name=o.model_id,
            base_path=tmp_path,
        )
        e = Experiment(
            run_tag='test',
            model=o,
            input_dir=dataset_path,
            artifacts_handler=artifacts_handler,
        )
        e.run()
        p = o.predict(
            ids=["1"],
            X=["406,-2.3122265423263,1.95199201064158,-1.60985073229769,3.9979055875468,-0.522187864667764,-1.42654531920595,-2.53738730624579,1.39165724829804,-2.77008927719433,-2.77227214465915,3.20203320709635,-2.89990738849473,-0.595221881324605,-4.28925378244217,0.389724120274487,-1.14074717980657,-2.83005567450437,-0.0168224681808257,0.416955705037907,0.126910559061474,0.517232370861764,-0.0350493686052974,-0.465211076182388,0.320198198514526,0.0445191674731724,0.177839798284401,0.261145002567677,-0.143275874698919,0,1".split(",")[:-1]],  # noqa: E501
        )
        assert "1" in p
        assert p["1"] in [0.0, 1.0]
