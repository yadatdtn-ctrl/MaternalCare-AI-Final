# MaternalCare AI

MaternalCare AI is a Streamlit web app for pregnant women offering BMI calculation, expected delivery date estimation, and AI-based maternal health risk assessment.

**This branch (`ramya`) is for research only** — it contains Ramya's Jupyter notebook and dataset. For the runnable Streamlit app, use the `main` branch.

## Team

- **Yada** — Application development (BMI Module, EDD Module, and Risk Assessment Module), Streamlit interface, integration
- **Ramya** — Dataset research, model training and evaluation

## Features

- **BMI module** — Calculates body mass index from weight and height, and classifies the result (underweight, normal, or overweight).
- **EDD module** — Estimates the expected delivery date using Naegele's Rule and reports pregnancy week and trimester.
- **Risk Assessment module** — Predicts maternal health risk (low, mid, or high) using a K-Nearest Neighbors classifier (K=2) with feature scaling, achieving approximately 68.1% accuracy on the maternal health risk dataset.

## Tech stack

- Python
- Jupyter
- scikit-learn
- Pandas
- NumPy
- Matplotlib
- Seaborn

## Project structure

```
MaternalCare_LogisticRegression_RamyaPresentation.ipynb
maternal_health_risk.csv
requirements.txt
README.md
LICENSE
.streamlit/config.toml
```

## How to run

### Research notebook (this branch)

1. Clone the repo and checkout the `ramya` branch.
2. Install dependencies: `pip install -r requirements.txt`
3. Start Jupyter: `jupyter notebook`
4. Open `MaternalCare_LogisticRegression_RamyaPresentation.ipynb`

### Streamlit app

Use the `main` branch:

1. Checkout `main`.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `python -m streamlit run app.py`

## Dataset source

Maternal Health Risk dataset on Kaggle: https://www.kaggle.com/datasets/csafrit2/maternal-health-risk-data

## Disclaimer

This app supports but does not replace professional medical advice. The risk assessment model was trained on data for ages 10-70.

## License

See [LICENSE](LICENSE) in the repository root.
