# Outside Cattle

## Summary
For the Outside Cattle project, we explored different machine learning models to predict cattle methane emissions. 
Multiple models perform well. We initially explored suggestions from [this paper](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10749206/) (eg. multiple linear regression, random forest regression), then transitioned to experimentation with other algorithms, such as Multilayer Perceptron, Gradient Boosting, and Elastic Net. 

### Data
 
wallace_metadata.csv: contains feed component data, herd data, and rumen microbiome data from Wallace et al. ([2019](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6609165/))

### Scripts
 
main.py: Streamlit Interface for the Outside Cattle project
utils.py: Support Classes and Functions for the Interface
outside_cattle.ipynb: Juypter Notebook with data visualization and models experimentation
requirements.txt: Required packages for the project

### Assets
feature_selection.png: Feature Selection for the Outside Cattle project
interface.png: Interface for the Outside Cattle project
elastic_net_actual_vs_predicted.png: Elastic Net Actual vs Predicted
knn_actual_vs_predicted.png: KNN Actual vs Predicted
mlp_actual_vs_predicted.png: MLP Actual vs Predicted
random_forest_actual_vs_predicted.png: Random Forest Actual vs Predicted
svr_actual_vs_predicted.png: SVR Actual vs Predicted
xgboost_actual_vs_predicted.png: XGBoost Actual vs Predicted
lightgbm_actual_vs_predicted.png: LightGBM Actual vs Predicted
mlp_loss_curve.png: MLP training and validation loss curves
heatmap_microbiome.png: Heatmap of the microbiome data correlation
trimmed_data.png: Trimmed data for the Wallace's Dataset base on standard deviation
smogn.png: SMOGN algorithm to balance the dataset for better results
knn_herd_model.png: KNN model to predict herd data base on feed information

## Setup
1. Make sure to install git lfs by running 
   `git lfs install`
   If any problems refer to the website [here](https://git-lfs.github.com/)
2. Make sure you are in the right directory by running 
   `cd models/outside-cattle/scripts`
3. Install the required packages by running 
   `pip install -r requirements.txt`
4. Run the interface by running 
   `streamlit run main.py`

If you have conda/anaconda/mamba:
3. Create a new environment by running 
   `conda create --name outside-cattle -f environment.yml`
4. Activate the environment by running
   `conda activate outside-cattle`
5. Run the interface by running
   `streamlit run main.py`
