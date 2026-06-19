# MaternalCare AI

MaternalCare AI is a Streamlit web app for pregnant women offering BMI calculation, expected delivery date estimation, and AI-based maternal health risk assessment.

## Team

- **Yada** - Application development, Streamlit interface, integration
- **Ramya** - Dataset research, model training and evaluation

## Features

- **BMI module** - Calculates body mass index from weight and height, and classifies the result (underweight, normal, or overweight).
- **EDD module** - Estimates the expected delivery date using Naegele's Rule and reports pregnancy week and trimester.
- **Risk Assessment module** - Predicts maternal health risk (low, mid, or high) using a K-Nearest Neighbors classifier (K=2) with feature scaling, achieving approximately 68.1% accuracy on the maternal health risk dataset.

## Tech stack

- Python
- Streamlit
- scikit-learn
- Pandas
- NumPy

## Project structure

```
   app.py
   src/
     __init__.py
     bmi_module.py
     edd_module.py
     risk_module.py
   data/
     maternal_health_risk.csv
   requirements.txt
   .streamlit/config.toml
```

## How to run

1. Clone the repo.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `python -m streamlit run app.py`

## Dataset source

Maternal Health Risk dataset on Kaggle: https://www.kaggle.com/datasets/csafrit2/maternal-health-risk-data

## Disclaimer

This app supports but does not replace professional medical advice. The risk assessment model was trained on data for ages 10-70.

## License

See [LICENSE](LICENSE) in the repository root.
