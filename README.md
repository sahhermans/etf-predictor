# ETF Predictor: Machine Learning Pipeline for ETF Price Prediction

Predict ETF prices using historical data. This project includes data collection, preprocessing, model training, evaluation, and deployment with MLFlow. Built with `pandas`, `scikit-learn`, `yfinance`, and `mlflow`. 

Current organisation of this repository:
project-root/
├── src/
│   ├── data_ingestion/          # Download ETF data and store in SQLite
│   │   └── data_ingestion.py
│   ├── data_pipeline/           # Load and clean raw data
│   │   ├── load_data.py
│   │   └── clean_data.py
│   └── features/                # Feature engineering + export
│       ├── feature_engineering.py
│       └── save.py              # save_features_to_sqlite()
│
├── scripts/                     # Entry points / orchestration scripts
│   ├── fetch_data.py            # Runs data download
│   ├── inspect_cleaned_data.py  # View cleaned data
│   ├── inspect_features.py      # View engineered features
│   └── run_data_pipeline.py     # Full pipeline: load → clean → build features → save
│
├── data/                        # Data artifacts
│   ├── raw/                     # Downloaded raw data
│   └── processed/               # Final SQLite DB with enriched features
│
└── environment.yml              # Conda environment specification
