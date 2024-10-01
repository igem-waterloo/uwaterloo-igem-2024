# Algae 'n' Enzymes

## Summary
For the Algae n' Enzymes project, we created a model to estimate the rate at which the C. vulgaris will be broken down in the cattle rumen, and thus estimated the amount of peir which will be released as a function of time and initial C. vulgaris fed to the cow. 
A thermodynamics-based approach was used, based on [this paper](https://animres.edpsciences.org/articles/animres/abs/2006/05/z205012/z205012.html), assuming that the majority of the cell wall is composed of cellulose. Due to the limited and contradictory information regarding C. vulgaris cell wall concentrations in literature, a Monte Carlo algorithm was implemented for the glucose percentage of the cell wall. 

### Data

### Scripts

MonteCarloMain.m: The main script containing the Monte Carlo model for glucose only.
MultiMonteCarlo.m: A modification of the main script also allowing for the Monte Carlo simulation of time spent by feed in the rumen.
odeModel.m: The ODE model from the paper.
odeModelMulti.m: A modification of the ODE model to allow for varying time length inputs.

### Assets
The graphs resulting from a given set of runs if the Monte Carlo script were included. Note that these graphs need not necessarily coincide with future runs of the same script due to the random nature of the Monte Carlo simulation. 

Average.jpg: 
CellWallConcentration.jpg:
DegradationOverTime.jpg:

## Setup
1. Make sure to install MATLAB and the ODE toolbox (which should be installed by default with your MATLAB installation) 
2. Navigate to the models directory, by running 
   `cd models\algae-n-enzymes\scripts`
3. Ensure that the ODE model and the corresponding Monte Carlo script are located in the same directory on your local device 
    (`MonteCarloMain.m` and `odeModel.m` for graphs or `MultiMonteCarlo.m` and `odeModelMulti.m` for numeric, time varying output)
4. Run the model by running 
   `MonteCarloMain.m` for the graphs or `MultiMonteCarlo.m` for the time-varying simulation.