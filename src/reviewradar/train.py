"""
Produciton training pipeline for reviewradar sentiment model

Refactored from notebooks/01_first_model.ipynb 

Run :  python -m reviewradar.train --config/train.config.yaml
"""

import argparse 

import logging 

from pathlib import Path

import joblib 
import pandas as pd

import yaml


from datasets import load_dataset 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split

logger = logging.getLogger(__name__) 

def load_config(config_path:str)->dict:

    with open(config_path) as f:
        config = yaml.safe_load(f)

    
    logger.info(f"Loaded config from  {config_path}")

    return config


def load_data(config:dict)->pd.DataFrame:
    data_cfg = config["data"]
    logger.info(f"loading dataset '{data_cfg['dataset_name']}'...")

    dataset = load_dataset(data_cfg["dataset_name"], split="train")

    df = pd.DataFrame(dataset).sample(
        n = data_cfg["sample_size"], random_state=data_cfg["random_state"]
    ) 

    logger.info(f"loaded {len(df)} rows. Label balance:  \n {df['label'].value_counts()}") 

    return df


def split_data(df:pd.DataFrame, config: dict):

    data_cfg = config["data"]

    X_train, X_test, y_train, y_test = train_test_split(
        df["text"],
        df["label"],
        test_size=data_cfg["test_size"],
        random_state=data_cfg["random_state"],
        stratify=df["label"], 
    )

    logger.info(f"Split: {len(X_train)} train / {len(X_test)} test") 

    return X_train, X_test, y_train, y_test

def build_vectorrizer(config:dict)->TfidfVectorizer:

    feat_cfg = config["features"]

    return TfidfVectorizer(
        max_features=feat_cfg["max_features"], 
        ngram_range= tuple(feat_cfg["ngram_range"]), 
        stop_words=feat_cfg["stop_words"],
    )


def train_and_evaluate(X_train, X_test, y_train, y_test, config:dict):


    vectorizer = build_vectorrizer(config)

    logger.info("Vectorizing ( fit on train , transfrom on test -- no leakage!) ...  ") 

    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test) 


    model_cfg = config["model"]

    model = LogisticRegression(
        max_iter=model_cfg["max_iter"], random_state=model_cfg["random_state"]
    )

    logger.info("Training model ..  ") 
    model.fit(X_train_vec, y_train) 

    y_pred = model.predict(X_test_vec) 

    metrics = {
        "accuracy": round(accuracy_score(y_test, y_pred), 4), 
        "f1": round(f1_score(y_test, y_pred), 4),
    }

    logger.info(f"Metric:{metrics}")
    return model, vectorizer, metrics

def save_artifacts(model, vectorizer, metrics:dict, config:dict)->None:

    model_dir = Path(config["output"]["model_dir"])
    model_dir.mkdir(exist_ok=True) 


    joblib.dump(model, model_dir/"sentiment_model.joblib") 
    joblib.dump(vectorizer, model_dir/"vectorizer.joblib")


    with open(model_dir/"metrics.yaml", "w") as f:
        yaml.dump(metrics, f)

    logger.info(f"Artifacts saved to {model_dir}/")


def run_training(config_path:str)->dict:

    config  = load_config(config_path)

    df = load_data(config)
    X_train,  X_test, y_train, y_test = split_data(df, config)

    model, vectorizer, metrics = train_and_evaluate(X_train, X_test, y_train, y_test, config)
    save_artifacts(model,  vectorizer, metrics, config)

    logger.info("Training pipeline complete")
    return metrics


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",

    )

    parser = argparse.ArgumentParser(description="Train the reviewradar sentiment model")
    parser.add_argument(
        "--config", default="configs/train.yaml",help = "Path to trainging config YAML"

    )

    args = parser.parse_args()
    run_training(args.config)


if __name__ == "__main__":
    main()













