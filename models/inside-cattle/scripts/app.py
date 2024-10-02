import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
import matlab.engine 
import seaborn as sns
import os

eng = matlab.engine.start_matlab()
eng.cd(os.path.dirname(__file__))
eng.addpath(os.path.abspath(os.path.dirname(__file__)))
print("Rerun")
print(eng.pwd())
result = eng.eval("which('fermentation_model')")
print(eng.ls())
# eng.eval("run('fermentation_model.m')")


st.title('Inside Cattle ODE using MATLAB Rumen Model')
with st.expander("Initial Conditions", expanded=True):
    st.sidebar.write("Initial conditions for the ODE system:")
    z_NDF_0 = st.sidebar.number_input('z_NDF_0 (Cell wall carbohydrates)', value=2.0, format="%.5f")
    z_NSC_0 = st.sidebar.number_input('z_NSC_0 (Non-fiber carbohydrates)', value=5.0, format="%.5f")
    z_pro_0 = st.sidebar.number_input('z_pro_0 (Proteins)', value=1.25, format="%.5f")
    s_su_0 = st.sidebar.number_input('s_su_0 (Soluble sugars)', value=0.00067, format="%.5f")
    s_aa_0 = st.sidebar.number_input('s_aa_0 (Soluble amino acids)', value=0.0, format="%.5f")
    s_H2_0 = st.sidebar.number_input('s_H2_0 (Soluble hydrogen)', value=0.000002, format="%.5f")
    s_ac_0 = st.sidebar.number_input('s_ac_0 (Soluble acetate)', value=0.006, format="%.5f")
    s_bu_0 = st.sidebar.number_input('s_bu_0 (Soluble butyrate)', value=0.01, format="%.5f")
    s_pr_0 = st.sidebar.number_input('s_pr_0 (Soluble proline)', value=0.00005, format="%.5f")
    s_IN_0 = st.sidebar.number_input('s_IN_0 (Inorganic nitrogen)', value=0.025, format="%.5f")
    s_IC_0 = st.sidebar.number_input('s_IC_0 (Inorganic carbon)', value=0.14, format="%.5f")
    s_CH4_0 = st.sidebar.number_input('s_CH4_0 (Soluble methane)', value=0.0007, format="%.5f")
    x_su_0 = st.sidebar.number_input('x_su_0 (Sugar utilizers)', value=0.01, format="%.5f")
    x_aa_0 = st.sidebar.number_input('x_aa_0 (Amino acid utilizers)', value=0.005, format="%.5f")
    x_H2_0 = st.sidebar.number_input('x_H2_0 (Hydrogen utilizers)', value=0.00075, format="%.5f")
    ng_H2_0 = st.sidebar.number_input('ng_H2_0 (Gas phase hydrogen)', value=0.00006, format="%.5f")
    ng_CO2_0 = st.sidebar.number_input('ng_CO2_0 (Gas phase CO2)', value=0.76, format="%.5f")
    ng_CH4_0 = st.sidebar.number_input('ng_CH4_0 (Gas phase methane)', value=0.35, format="%.5f")


y0 = [
    z_NDF_0, z_NSC_0, z_pro_0, s_su_0, s_aa_0, s_H2_0,
    s_ac_0, s_bu_0, s_pr_0, s_CH4_0, s_IC_0, s_IN_0,
    x_su_0, x_aa_0, x_H2_0, ng_H2_0, ng_CO2_0, ng_CH4_0
]

x_H2_1 = x_H2_0 / 1 * 0.25
x_su_1 = x_su_0 / 94 * (94 + 0.95 * 0.75)
x_aa_1 = x_aa_0 / 5 * (5 + 0.05 * 0.75)

reduced_y0 = [
    z_NDF_0, z_NSC_0, z_pro_0, s_su_0, s_aa_0, s_H2_0,
    s_ac_0, s_bu_0, s_pr_0, s_CH4_0, s_IC_0, s_IN_0,
    x_su_1, x_aa_1, x_H2_1, ng_H2_0, ng_CO2_0, ng_CH4_0
]

tspan = [0, 30]
sns.set_palette("husl")
if st.button('Run Simulation'):
    initial_conditions_mat = matlab.double(y0)
    reduced_initial_conditions_mat = matlab.double(reduced_y0)

    t, q, y, z = eng.fermentation_model_for_app(initial_conditions_mat, reduced_initial_conditions_mat, nargout=4)

    st.header("ODE Results")

    t = np.array(t)
    y = np.array(y)
    q = np.array(q)
    z = np.array(z)

    print(y)

    titles = ['Zndf', 'Znsc', 'Zpro', 'Ssu', 'Saa', 'Sh2', 'Sac', 'Sbu', 'Spr', 'Sch4', 'SIC', 'SIN', 'Xsu', 'Xaa', 'Xh2']
    scales = [[0, 3], [0, 6], [0, 2], [0, 6], [0, 2.5], [0, 20], [0, 100], [0, 25], [0, 20], [0, 5], [0, 200], [0, 26], [0, 40], [0, 15], [0, 2]]
    ylabels = ["g/L", "g/L", "g/L", "mM", "mM", "uM", "mM", "mM", "mM", "mM", "mM", "mM", "mM", "mM", "mM"]
    plot_scale_factor = [1, 1, 1, 1e3, 1e3, 1e3, 1e3, 1e3, 1e3, 1e3, 1e3, 1e3, 1e3, 1e3, 1e3]

    print(t.shape, y.shape, q.shape, z.shape)
    print(t[:, 0].shape, y[:, 0].shape)

    fig, axs = plt.subplots(3, 5, figsize=(20, 12))

    for i, ax in enumerate(axs.flatten()):
        sns.lineplot(x=t[:, 0], y=y[:, i] * plot_scale_factor[i], ax=ax, label=titles[i])
        ax.set_title(titles[i])
        ax.set_xlabel('Time (h)')
        ax.set_ylabel(ylabels[i])
        ax.set_ylim(scales[i])
        ax.legend()

    plt.tight_layout()
    st.pyplot(fig)

    st.header("ODE Results (Reduced System)")

    fig, axs = plt.subplots(3, 5, figsize=(20, 12))

    for i, ax in enumerate(axs.flatten()):
        sns.lineplot(x=q[:, 0], y=z[:, i] * plot_scale_factor[i], ax=ax, label=titles[i])
        ax.set_title(titles[i])
        ax.set_xlabel('Time (h)')
        ax.set_ylabel(ylabels[i])
        ax.set_ylim(scales[i])
        ax.legend()
    
    plt.tight_layout()
    st.pyplot(fig)

    



