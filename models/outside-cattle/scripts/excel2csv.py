import pandas as pd

table2 = "/Users/wallacelee/Downloads/Table_2.XLSX"
table3 = "/Users/wallacelee/Downloads/Table_3.XLSX"

wallace_metadata = pd.read_excel(table2, sheet_name="Wallace_metadata")
wallace_microbiome = pd.read_excel(table2, sheet_name="Wallace_microbiome")

wallace_methane = pd.read_excel(table3, sheet_name="Wallace_methane")


print(wallace_metadata.head())
print(wallace_microbiome.head())
print(wallace_methane.head())

# Join the tables
wallace_metadata = wallace_metadata.merge(wallace_microbiome, on="sample_id")
wallace_metadata = wallace_metadata.merge(wallace_methane, on="sample_id")

# wallace_metadata.to_csv("wallace_metadata.csv", index=False)
wallace_metadata.info()