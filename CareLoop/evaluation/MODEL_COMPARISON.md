# Model Comparison

All three models were trained and evaluated using the same preprocessed training and testing data.

| Model | Accuracy | Precision | Recall | F1 Score | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Decision Tree | 0.5974 | 0.1470 | 0.5769 | 0.2342 | 0.6075 |
| Logistic Regression | 0.6554 | 0.1665 | 0.5560 | 0.2562 | 0.6558 |
| Random Forest | 0.8524 | 0.2568 | 0.2022 | 0.2263 | 0.6730 |

## Selected model: Logistic Regression

Logistic Regression was selected because it achieved the highest F1 score in this comparison. Decision Tree achieved slightly higher recall, while Random Forest achieved the highest accuracy but had much lower recall. Since the dataset is imbalanced, accuracy alone is not a suitable selection measure.

These are baseline results from the current processed dataset and settings. They do not prove that the selected model is clinically reliable. Further validation and threshold analysis would be needed before any real-world use.