# Evaluation Report: Loan Default Prediction

## The Task

The goal was to predict whether a loan applicant will default, using four pieces of information: their credit score, income, loan amount, and employment type (Salaried, Self-Employed, or Contract).

The dataset has 1,200 applicants. One wrinkle: 90 of them (7.5%) are missing a credit score — this happens in real life when bureau data isn't available for an applicant. How that gap gets filled matters a lot: if you fill it in using information from the whole dataset *before* splitting into training and test sets, you accidentally let the test set "leak" into training, and your evaluation numbers end up looking better than the model would actually perform in the real world. To avoid this, the data was split into training (960 applicants) and test (240 applicants) sets first, and only then was the missing credit score filled in — using the median credit score computed from the training set alone (649), applied to both sets.

Also worth noting: 60% of applicants in this dataset defaulted. That means "default" is actually the majority outcome here, which is the opposite of what you'd expect from a typical loan portfolio and affects how a baseline model behaves.

## The Baseline

Before building any real model, a simple baseline was set: always guess the majority class (default). This isn't intelligent, but it defines the bar any real model needs to clear.

| Metric | Baseline Score |
|---|---|
| Accuracy | 0.600 |
| Precision | 0.600 |
| Recall | 1.000 |
| F1 | 0.750 |
| ROC-AUC | 0.500 |

The baseline's recall is a perfect 1.000 only because it labels *everyone* a defaulter — it never misses one, but that's not a useful signal. Its ROC-AUC of 0.500 is the real tell: that's the score of pure random guessing. Any model that can't beat 0.500 on ROC-AUC hasn't learned anything.

## Model Comparison

Three real models were trained on the same data and compared: Logistic Regression, a Decision Tree, and a Random Forest.

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---|---|---|---|---|
| Baseline | 0.600 | 0.600 | 1.000 | 0.750 | 0.500 |
| Logistic Regression | 0.746 | 0.768 | 0.826 | 0.796 | 0.845 |
| Decision Tree | 0.729 | 0.776 | 0.771 | 0.774 | 0.821 |
| Random Forest | 0.767 | 0.782 | 0.847 | 0.813 | 0.853 |

All three real models comfortably beat the baseline — most clearly on ROC-AUC (baseline 0.500 vs. 0.82–0.85 for the real models), which confirms they picked up genuine signal from credit score, income, loan amount, and employment type rather than just guessing.

Among the three, **Random Forest came out on top on every single metric**, followed closely by Logistic Regression, with the Decision Tree trailing both.

## Final Model: Random Forest

**Random Forest was selected as the final model.** The case for it isn't just one good number — it wins across the board (accuracy 0.767, precision 0.782, recall 0.847, F1 0.813, ROC-AUC 0.853), and it holds up under closer inspection too (see error analysis below). Logistic Regression is a close second and would be a very defensible pick if a simpler, more interpretable model were a priority, but on raw performance Random Forest is the stronger choice.

## Error Analysis

Aggregate scores can hide a bad pattern of mistakes — a model can look fine "on paper" while quietly missing the cases that matter most. Here, missing an actual defaulter (a false negative) is the costlier kind of error, since it means approving a loan that shouldn't be approved. Looking at how each model's errors break down on the 240-applicant test set:

| Model | False Negatives (missed defaulters) | False Positives |
|---|---|---|
| Logistic Regression | 25 | 36 |
| Decision Tree | 33 | 32 |
| Random Forest | **22** | 34 |

**Finding:** Random Forest doesn't just win on the summary metrics — it also makes the fewest costly mistakes, missing only 22 of 144 actual defaulters, versus 25 for Logistic Regression and 33 for the Decision Tree. That consistency between the headline numbers and the actual error pattern is reassuring: it's not a model that looks good on average while hiding a weak spot. The Decision Tree, by contrast, is the weakest on both counts — its single-tree structure appears to capture less of the real pattern than either the linear boundary of Logistic Regression or the ensemble approach of Random Forest.

## Calibration

Beyond just classifying applicants as "default" or "no default," it's worth asking whether the model's predicted probabilities can be trusted — if it says an applicant has an 80% chance of defaulting, do roughly 80% of similar applicants actually default?

**Finding:** Random Forest's predicted probabilities are reasonably well-calibrated. Its Brier score (a measure of how close predicted probabilities are to actual outcomes, where lower is better and 0 is perfect) came out to **0.155**. The calibration curve tracks the ideal diagonal fairly closely, with some wobble at the extreme ends — likely just noise, since the test set is small enough that each probability bucket only has about 24 applicants in it.

## Honest Limitation

This dataset is synthetic — it was generated from a fixed formula rather than collected from real loan applicants, and the test set is only 240 applicants. Both of those limit how far these results should be trusted: a Brier score of 0.155 and a small edge over Decision Tree could shift meaningfully on a bigger, real-world sample, and none of the relationships learned here (e.g., how loan-to-income ratio or employment type drives risk) are guaranteed to hold on an actual loan portfolio. This pipeline is best read as a correctly-built methodology exercise — clean split, no leakage, honest evaluation — rather than a model ready to make real lending decisions.
