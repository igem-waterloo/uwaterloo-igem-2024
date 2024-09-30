# Outside Cattle

##Summary
For the Outside Cattle project, we explored different machine learning models to predict cattle methane emissions. 
Multiple models perform well. We initially explored suggestions from [this paper](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10749206/) (eg. multiple linear regression, random forest regression), then transitioned to experimentation with other algorithms, such as Multilayer Perceptron, Gradient Boosting, and Elastic Net. 

###Data
 
wallace_metadata.csv: contains feed component data, herd data, and rumen microbiome data from Wallace et al. ([2019](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6609165/))

###Scripts
 
main.py: [enter short description here]
utils.py: [enter short description here]
...

###Assets
...

##Setup
1. Make sure you are in the right directory by running 
   `cd models/outside-cattle/scripts`
2. Install the required packages by running 
   `pip install -r requirements.txt`
3. Run the interface by running 
   `streamlit run main.py`
