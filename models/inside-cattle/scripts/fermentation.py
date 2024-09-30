import cobra

# Load the SBML file
model = cobra.io.read_sbml_model("../data//M_Methanobrevibacter_ruminantium_M1__44____32__AGORA__32__version__32__1__46__03.sbml")
model.optimize()
print(model.summary())