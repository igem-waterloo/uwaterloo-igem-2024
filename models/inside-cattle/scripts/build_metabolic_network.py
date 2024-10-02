############################################# BUILD METABOLIC NETWORK ###############################################
# dependencies
import cobra
from cobra import *
import os
import d3flux as d3f
from d3flux.core.flux_layouts import render_model
from jinja2 import Template

curdir = os.getcwd()

# load in SBML file for methanobrevibacter ruminantium M1 - to run, download this from AGORA
m_ruminantium = cobra.io.read_sbml_model(f"{curdir}/M_Methanobrevibacter_ruminantium_M1__44____32__AGORA__32__version__32__1__46__03.sbml")

optimize = False # set this to run an optimization to minimize biomass

if optimize:
    # by default, the network is set to optimize biomass production when a flux balance analysis is run. set the objective function to also minimize the methane production and biomass production.
    # preview objective function
    print(m_ruminantium.objective)

    # optimize on 'minimum' setting, return the objective value of solution
    solution = m_ruminantium.optimize(min).objective_value

    # preview solution
    print(solution)

summary = m_ruminantium.summary()
print("Flux balance saved to 'assets/m_ruminantium_flux.txt'.")

# with open("../assets/m_ruminantium_flux.txt", "w") as file:
with open(f"{curdir}/assets/m_ruminantium_flux.txt", "w") as file:
    file.write(f"{summary}")
