# Inside Cattle
This model aims to determine the impact on both methane production and the complex cow microbiome that our solution could conceivably have. 

### Scripts
Two models are integrated:  
`build_metabolic_network.py`: focused on exploring the metabolic pathways and flux distribution towards production of methane in M.Ruminantium.
`fermentation_model.m`: focused on exploring the rumen-wide consumption and production of key metabolites by amino acid-utilizing bacteria, hydrogen-utilizing bacteria (methanogens), and sugar-utilizing bacteria, and their microbial growth in relation to nutrient availability.
`app.py`: a streamlit app that allows users to interact with the fermentation model and observe the impact of different parameters on the rumen microbiome and methane production.

### To Run:
`build_metabolic_network.py`: ensure that CobraPy is installed to a current version of python. Download `/data/M_Methanobrevibacter_ruminantium_M1__44____32__AGORA__32__version__32__1__46__03.sbml` and ensure it is placed in the same local directory, and run using an IDE of choice.
`fermentation_model.m`: ensure that MATLAB and numeric toolboxes are installed. Download the script, and run.

To run the interface:
1. Download Matlab Engine
   `python -m pip install matlabengine`
   Make sure to install the correct version of Matlab Engine for your [Matlab version](https://www.mathworks.com/support/requirements/python-compatibility.html)
2. Install streamlit
    `pip install streamlit`
3. cd into the directory containing the app.py file
    `cd models/inside-cattle/scripts`
4. Run the app
    `streamlit run app.py`

### Assets:
`fermentation_model.m` outputs a plot of fifteen major state variables, consisting of feed components, soluble metabolite concentrations, and bacterial concentrations in the cow rumen with time. It outputs a plot of all of these variables, under a typical state and a reduced methanogenic state, where hydrogen-utilizer concentration has been reduced to simulate interference with M. ruminantium microbial growth.

`fermentation_model_for_app.m` is the wrapper version of the model for the app interface 
