from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import make_pipeline as imbalanced_make_pipeline
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import (average_precision_score, confusion_matrix,
                             f1_score, precision_recall_curve, precision_score,
                             recall_score, roc_auc_score)
from sklearn.preprocessing import StandardScaler
from utils.logger import logger


class MLModel(ABC):

    @property
    @abstractmethod
    def model_id(self) -> str:
        pass

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def predict(self, data):
        pass


@dataclass
class ProjectModel(MLModel):
    model_hyperparameters: Path = None

    @property
    def model_id(self) -> str:
        return "credit-card-fraud"

    def save(self, model_prefix):
        self.model_path = model_prefix / 'model.joblib'
        joblib.dump(self.model, self.model_path)
        return self.model_path

    def load(self, model_prefix):
        self.model_path = model_prefix / self.model_id / 'model.joblib'
        try:
            self.model = joblib.load(self.model_path)
        except FileExistsError as e:
            logger.error(e)
        except Exception as e:
            raise e
        return self.model

    def __build_model(self):
        std_scaler = StandardScaler()
        smt = SMOTE(k_neighbors=3, random_state=42, sampling_strategy='minority')
        if self.model_hyperparameters:
            log_reg_sm = SGDClassifier(**self.model_hyperparameters)
        else:
            log_reg_sm = SGDClassifier()

        pipeline = imbalanced_make_pipeline(
            std_scaler,
            smt,
            log_reg_sm,
        )
        self.model = pipeline

    def train(self, X_train, y_train):
        self.__build_model()

        self.model.fit(
            X_train,
            y_train,
        )

    def evaluate(self, X_validation, y_validation):
        prediction = self.model.predict(X_validation)

        acc = self.model.score(X_validation, y_validation)
        precision = precision_score(y_validation, prediction)
        recall = recall_score(y_validation, prediction)
        f1_lst = f1_score(y_validation, prediction)
        auc_lst = roc_auc_score(y_validation, prediction)

        return acc, precision, recall, f1_lst, auc_lst

    def gen_plots(self, X_validation, y_validation):
        y_score = self.model.decision_function(X_validation)
        average_precision = average_precision_score(y_validation, y_score)

        fig1 = plt.figure(figsize=(12, 6))
        precision, recall, _ = precision_recall_curve(y_validation, y_score)
        plt.step(recall, precision, color='r', alpha=0.2, where='post')
        plt.fill_between(
            recall,
            precision,
            step='post',
            alpha=0.2,
            color='#F59B00'
        )
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.ylim([0.0, 1.05])
        plt.xlim([0.0, 1.0])
        plt.title(
            'OverSampling Precision-Recall curve: \n Average Precision-Recall Score ={0:0.2f}'.format(
                average_precision),
            fontsize=16
        )

        prediction = self.model.predict(X_validation)
        cf = confusion_matrix(y_validation, prediction)

        fig2 = plt.figure(figsize=(12, 6))
        sns.heatmap(cf, annot=True, cmap='Blues')
        plt.title("Logistic Regression\nConfusion Matrix", fontsize=14)

        return {
            "precision-recall-curve": fig1,
            "confusion-matrix": fig2
        }

    def predict(self, ids, X):
        prediction = self.model.predict(X)
        return {i: pred for i, pred in zip(ids, prediction)}
