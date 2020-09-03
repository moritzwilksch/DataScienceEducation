# Fast.ai
- On structured data, start with tree ensembles (Random Forest or CatBoost), maybe try DL
- Exception: many high-cardinality categorical features which are very important
Summary: https://medium.com/@hiromi_suenaga/machine-learning-1-lesson-1-84a1dc2b5236
## Random Forests

- Useful starting values for min_samples_leaf = 1, 3, 5, 10, 25
- max_samples per bootstrap helps decorrelate trees
- Examine ***feature importance!***
- OHE can be useful for RF, try for your data set. OHE is especially useful for examining feature importance
- Use the variance of the single trees estimates as a proxy of **prediction confidence**
- Use hierarchical clustering (dendrogram plot) to find similar/redundant features
- For the important features, plot partial dependence to understand relationships in more detail
    - Idea: use partial dependence on *clusters* of similar samples to see different behaviors for different groups of samples
- Random forest have extrapolation issues (feature range not in training set)
    - stop using time variables
    > So you could put the test set and training set together, create a new column called is_test and see if you can predict it.  
    > If you can, you don’t have a random sample which means ***you have to figure out how to create a validation set*** from it.
    - Example: Put train and validation set together, add is_val which is 1 for samples from the validation set and 0 for the training set, and train on this combined set a model that predicts is_val. Any features that are predictive are probably time dependent.

## Test-Validation Set Calibration
- idea from kaggle: create serveral models and make sure that the performance of all of them on the VALIDATION and TEST set is as close to each other as possible. Subsequently, you have a validation set that represents test data nicely.