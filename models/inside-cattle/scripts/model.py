import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Constants
k_a_CO2 = 5.13e-7
k_a_NH4 = 1.44e-9
k_a_vfa = 1.74e-5
k_H_CO2 = 2.46e-2
k_H_CH4 = 1.10e-3
k_H_H2 = 7.23e-4
k_w = 2.75e-14
P = 1.01325
T = 312.15
V_l = 0.030
w_aa = 134
w_ac = 60.05
w_bu = 88.10
w_mb = 113
w_pr = 74.08
w_su = 180.16

k_L_a = 1.07
s_cat = 0.14
f_ch_x = 0.2
f_pro_x = 0.55
k_d = 8.33e-4
k_hyd_ndf = 0.05
k_hyd_nsc = 0.2
k_hyd_pro = 0.22
k_s_su = 9e-3
k_m_su = 0.99
k_s_IN = 2e-4
y_su = 2e-4
l_1 = 0.43
l_2 = 0.29
l_3 = 0.28
k_s_aa = 6.4e-3
k_m_aa = 1.98
y_aa = 0.31
sigma_ac_aa = 0.67
sigma_bu_aa = 0.24
sigma_pr_aa = 0.062
sigma_H2_aa = 0.82
sigma_IC2_aa = 0.88
k_s_H2 = 5.84e-6
k_m_H2 = 13.93
y_H2 = 0.0016
n_aa = 110 * ((0.19+0.13)/2)
n_mb = 0.12

# Initial Conditions
z_ndf_0 = 2.5  # Neutral Detergent Fiber
z_nsc_0 = 3  # Non-structural Carbohydrates (Sugars/Starches)
z_pro_0 = 0.2  # Proteins
s_su_0 = 5   # Sugars
s_aa_0 = 0  # Amino Acids
s_H2_0 = 1e-6  # Hydrogen in liquid phase (mol/L)
s_ac_0 = 2.0   # Acetate
s_bu_0 = 10   # Butyrate
s_pr_0 = 0   # Propionate
s_IC_0 = 140   # Inorganic Carbon
s_IN_0 = 0.02  # Inorganic Nitrogen
s_CH4_0 = 0    # Methane (mol/L)
x_su_0 = 0.5   # Sugars-utilizing microbes (g/L)
x_aa_0 = 0.5   # Amino acids-utilizing microbes (g/L)
x_H2_0 = 0.75
n_g_H2_0 = 0.002
n_g_CO2_0 = 0.65
n_g_CH4_0 = 0.27

# Stoichiometric coefficients
f_su = 1 - (5/6) * y_su
y_ac_su = f_su * (2 * l_1 + (2/3) * l_2)
y_bu_su = f_su * l_3
y_pr_su = f_su * (4/3) * l_2
y_H2_su = f_su * (4 * l_1 + 2 * l_3)
y_IN_su = -y_su
y_IC_su = f_su * (2 * l_1 + (2/3) * l_2 + 2 * l_3)
f_H2 = 1 - 10 * y_H2
y_CH4_H2 = f_H2 * 0.25
y_IC_H2 = ((-0.25 * f_H2) + 0.5 * (1 - f_H2))
y_IN_H2 = -y_H2
y_H2_aa = (1 - y_aa) * sigma_H2_aa
y_ac_aa = (1 - y_aa) * sigma_ac_aa
y_bu_aa = (1 - y_aa) * sigma_bu_aa
y_pr_aa = (1 - y_aa) * sigma_pr_aa
y_IN_aa = n_aa - y_aa * n_mb
y_IC_aa = (1 - y_aa) * sigma_IC2_aa

m_ruminantium = 0.168168 # Percetage


# Define the system of ODEs
def odes(t, y):
    decay_factor = np.exp(-0.1 * t)

    z_ndf, z_nsc, z_pro, s_su, s_aa, s_H2, s_ac, s_bu, s_pr, s_IN, s_IC, s_CH4, x_su, x_aa, x_H2, n_g_H2, n_g_CO2, n_g_CH4 = y

    # Kinetic rates
    I_IN = s_IN / (s_IN + k_s_IN)
    p_ndf = k_hyd_ndf * z_ndf
    p_nsc = k_hyd_nsc * z_nsc
    p_pro = k_hyd_pro * z_pro
    p_su = k_m_su * s_su / (k_s_su + s_su) * x_su * I_IN
    p_aa = k_m_aa * s_aa / (k_s_aa + s_aa) * x_aa
    p_H2 = k_m_H2 * s_H2 / (k_s_H2 + s_H2) * x_H2 * I_IN
    p_xsu = k_d * x_su
    p_xaa = k_d * x_aa
    p_xh2 = k_d * x_H2

    # Microbial growth
    mu_su = y_su * p_su
    mu_aa = y_aa * p_aa
    mu_H2 = y_H2 * p_H2

    # Gas phase
    p_g_H2 = (n_g_H2 / (n_g_H2 + n_g_CO2 + n_g_CH4)) * P
    p_g_CO2 = (n_g_CO2 / (n_g_H2 + n_g_CO2 + n_g_CH4)) * P
    p_g_CH4 = (n_g_CH4 / (n_g_H2 + n_g_CO2 + n_g_CH4)) * P

    p_T_H2 = k_L_a * (s_H2 - k_H_H2 * p_g_H2)
    p_T_CO2 = k_L_a * (s_IC - k_H_CO2 * p_g_CO2)
    p_T_CH4 = k_L_a * (s_CH4 - k_H_CH4 * p_g_CH4)

    dn_g_H2 = V_l * p_T_H2
    dn_g_CO2 = V_l * p_T_CO2
    dn_g_CH4 = V_l * p_T_CH4
    
    # Equations
    dz_ndf = -p_ndf
    dz_nsc = -p_nsc + f_ch_x * (p_xsu + p_xaa + p_xh2)
    dz_pro = -p_pro + f_pro_x * (p_xsu + p_xaa + p_xh2)
    
    ds_su = p_ndf / w_su + p_nsc / w_su - p_su
    ds_aa = (p_pro / w_aa - p_aa) * (1 - m_ruminantium * decay_factor * (0.404-0.113))
    ds_H2 = y_H2_aa * p_aa + y_H2_su * p_su - p_H2 * (1 - m_ruminantium * decay_factor * 0.188) - p_T_H2
    ds_ac = y_ac_su * p_su + y_ac_aa * p_aa
    ds_bu = y_bu_su * p_su + y_bu_aa * p_aa
    ds_pr = y_pr_su * p_su + y_pr_aa * p_aa
    ds_CH4 = y_CH4_H2 * p_H2 * (1 - m_ruminantium * decay_factor * 0.) - p_T_CH4
    
    ds_IC = y_IC_aa * p_aa + y_IC_su * p_su + y_IC_H2 * p_H2 - p_T_CO2
    ds_IN = y_IN_aa * p_aa + y_IN_su * p_su + y_IN_H2 * p_H2
    
    dx_su = (y_su * p_su - p_xsu) 
    dx_aa = y_aa * p_aa - p_xaa
    dx_H2 = y_H2 * p_H2 - p_xh2
    
    return [dz_ndf, dz_nsc, dz_pro, ds_su, ds_aa, ds_H2, ds_ac, ds_bu, ds_pr, ds_IN, ds_IC, ds_CH4, dx_su, dx_aa, dx_H2, dn_g_H2, dn_g_CO2, dn_g_CH4]

# Initial conditions vector
y0 = [z_ndf_0, z_nsc_0, z_pro_0, s_su_0, s_aa_0, s_H2_0, s_ac_0, s_bu_0, s_pr_0, s_IN_0, s_IC_0, s_CH4_0, x_su_0, x_aa_0, x_H2_0, n_g_H2_0, n_g_CO2_0, n_g_CH4_0]

# Time span
tspan = [0, 25]

# Solving the ODE system
sol = solve_ivp(odes, tspan, y0, method='RK45')

legend_labels = [
    'z_NDF (mol)',       # Neutral Detergent Fiber
    'z_NSC (mol)',       # Non-structural Carbohydrates
    'z_pro (mol)',       # Proteins
    's_su (mol/L)',      # Sugars
    's_aa (mol/L)',      # Amino Acids
    's_H2 (mol/L)',      # Hydrogen in liquid phase
    's_ac (mol/L)',      # Acetate
    's_bu (mol/L)',      # Butyrate
    's_pr (mol/L)',      # Propionate
    's_IN (mol/L)',      # Inorganic Nitrogen
    's_IC (mol/L)',      # Inorganic Carbon
    's_CH4 (mol/L)',     # Methane
    'x_su (g/L)',        # Sugars-utilizing microbes
    'x_aa (g/L)',        # Amino acids-utilizing microbes
    'x_H2 (g/L)',         # Hydrogen-utilizing microbes
    'n_g_H2 (umol)',      # Hydrogen in gas phase
    'n_g_CO2 (umol)',     # Carbon dioxide in gas phase
    'n_g_CH4 (umol)'      # Methane in gas phase
]

# Replace all negative values with zeros
# sol.y[sol.y < 0] = 0

# Plot 15 plots
fig, axs = plt.subplots(4, 5, figsize=(12, 10))
for i, ax in enumerate(axs.flat):
    if i > 17:
        break
    if i > 14:
        ax.plot(sol.t, sol.y[i]*1e6)
    else:
        ax.plot(sol.t, sol.y[i])
    ax.set_title(legend_labels[i])

plt.tight_layout()
plt.savefig('fermentation_update.png')
# plt.show()

