## Baseline diagnostic

A DistilBERT classifier trained on the FormatBench training set achieves **100% accuracy on the held-out test set** but only **1.2% on the adversarial held-out set** which confirms that naive training on the
dataset learns surface formatting markers rather than context-sensitive judgment. This baseline establishes the gap that the DPO-trained model needs to close.

Full notebook with results on Kaggle: https://www.kaggle.com/code/techiekd/formatbench-100-test-1-2-on-adversarial
