############################################# BUILD FBA NETWORK ###############################################
# sydney sherwood <s3sherwo@uwaterloo.ca>
# july 19, 2024

# dependencies
import cobra
from cobra import *
import os
import d3flux as d3f
from d3flux.core.flux_layouts import render_model
from jinja2 import Template

curdir = os.getcwd()
print(curdir);

# load in SBML file for methanobrevibacter ruminantium M1 - to run, download this from AGORA
m_ruminantium = cobra.io.read_sbml_model(f"{curdir}/../data/M_Methanobrevibacter_ruminantium_M1__44____32__AGORA__32__version__32__1__46__03.sbml")

# by default, the network is set to optimize biomass production. set the objective function to also minimize the methane production and biomass production.
m_ruminantium.reactions.get_by_id('EX_ch4(e)').objective_coefficient = 1.0
m_ruminantium.reactions.get_by_id("EX_ch4(e)").upper_bound = 10000

# double-check objective function
# print(m_ruminantium.objective)

# optimize on 'minimum' setting, return the objective value of solution
solution = m_ruminantium.optimize(min).objective_value
print(solution)

summary = m_ruminantium.summary()
print(summary)

# visualize the model
custom_css = \
"""
{% for item in items %}
text#{{ item }} {
    font-weight: 900;
}
{% endfor %}
text.cofactor {
    fill: #778899;
}
"""

css = Template(custom_css).render(items=['succ_c', 'ac_c', 'etoh_c', 'for_c', 'co2_c', 'lac__D_c'])
from cobra.flux_analysis import pfba
pfba = pfba(m_ruminantium)

html = d3f.flux_map(m_ruminantium, custom_css=css,figsize =(520, 660), default_flux_width=2.5, fontsize=14)

with open("../assets/m_ruminantium_flux.html", "w") as file:
    file.write(str(html))

# html.save("m_ruminantium_flux.svg")
print(html)

# im gna hold off on the rest of the constraint stuff im working on rn cause haha it's bad but this should print the barebones network;)
