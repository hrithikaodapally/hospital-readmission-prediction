# Model Training and Comparison

We tested three classification algorithms on the same preprocessed data:

1. Decision Tree
2. Logistic Regression
3. Random Forest

Each model has its own folder. Open the folder's `README.md` for instructions.

## Current comparison

| Model | Accuracy | Precision | Recall | F1 Score |
|---|---:|---:|---:|---:|
| Decision Tree | 0.5974 | 0.1470 | 0.5769 | 0.2342 |
| Logistic Regression | 0.6554 | 0.1665 | 0.5560 | 0.2562 |
| Random Forest | 0.8524 | 0.2568 | 0.2022 | 0.2263 |

## Selected model

Logistic Regression is selected for the next backend integration step because it achieved the highest F1 score in this experiment. Decision Tree had slightly higher recall. Random Forest had the highest accuracy, but its recall was much lower.

The dataset is imbalanced. This is why accuracy alone was not used to select the model. These results are for an academic demonstration only and are not suitable for clinical decisions.
