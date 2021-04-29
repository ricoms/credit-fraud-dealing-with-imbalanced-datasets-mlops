#!/usr/bin/env python

import argparse
from pathlib import Path

import pandas as pd
from pandas_profiling import ProfileReport


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data_path",
        type=Path,
    )

    parser.add_argument(
        "--output_dir",
        type=Path,
    )
    args = parser.parse_args()

    df = pd.read_csv(Path.cwd() / args.data_path)
    profile = ProfileReport(df, title="Pandas Profiling Report")
    profile.to_file(Path.cwd() / args.output_dir / "data_profile.html")
