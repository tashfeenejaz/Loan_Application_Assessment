# Evaluation Q&A

**1. Random Forest's accuracy is close to (or below) Logistic Regression's — does that mean Logistic Regression should always win for a problem shaped like this?**

No. Random Forest's accuracy (0.767) is actually above Logistic Regression's (0.746) here, and it also leads on precision, recall, F1, and ROC-AUC (0.853 vs. 0.845). More importantly, one metric being close on one dataset split isn't grounds for a blanket rule — that's why the error analysis mattered: Random Forest made fewer false negatives (22 vs. 25), the costlier error type for loan default. My pick is Random Forest because it wins on the full picture, not because ensembles universally beat linear models.

**2. Why is computing the credit_score fill value from the entire dataset before splitting wrong, even though "it's just imputation, not modeling"?**

Imputation *is* modeling — it estimates a value from the data, and any value borrowed from the test set contaminates the evaluation. Here the train-only median was 649.0 vs. 650.0 for the full dataset, just a 1.0 difference, but the size doesn't matter — the full-dataset number was computed partly from the test set's own credit scores, which is textbook leakage. A leak that got lucky is still a leak.

**3. For a loan-default decision, is overall accuracy or recall on the "will default" class more important?**

Recall matters more. A false negative — approving someone who defaults — costs real money directly, while a false positive only costs a missed opportunity. Accuracy also misleads here since defaulters are the majority class (60%): the baseline hits 0.600 accuracy just by guessing "default" every time. Random Forest's 22 false negatives out of 144 defaulters (recall 0.847) is the number I'd defend, over its 0.767 accuracy.

**4. Walk through the calibration curve — would you trust this model's predicted probabilities directly to set a risk-based interest rate?**

Random Forest's curve tracks the perfect-calibration diagonal reasonably closely, and its Brier score (0.155) supports "reasonably calibrated," though there's noise at the extremes since each of the 10 bins only has ~24 of the 240 test points. I would not trust these probabilities directly for pricing — setting a rate off a specific number like 65% vs. 75% risk needs more precision than this small, noisy test set can back up.

**5. Name one real-world factor this pipeline doesn't have that you'd want before this model made actual lending decisions.**

One important real-world factor missing from this pipeline is the applicant's existing debt obligations (debt-to-income ratio) — how much other debt they're already carrying, beyond this loan. Two applicants with the same income and loan amount can have very different risk if one already has heavy existing debt and the other doesn't. This could have been added directly to this dataset as another feature, making its absence a concrete, fixable gap. Without it, the model is missing a core part of the applicant's financial profile that real underwriting would check, so it shouldn't be fully trusted for actual lending decisions yet.