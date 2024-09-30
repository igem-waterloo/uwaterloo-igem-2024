import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Constants
Ka_CO2 = 5.13e-7
Ka_NH4 = 1.44e-9
Ka_VFA = 1.74e-5
KH_CO2 = 2.46e-2
KH_CH4 = 1.1e-3
KH_H2 = 7.23e-4
Kw = 2.75e-14
P = 1.01325  # bar
T = 312.15  # K
V = 0.03  # L
w_aa = 134
w_ac = 60.05
w_bu = 88.1
w_mb = 113
w_pr = 74.08
w_su = 180.16

# Estimated parameters
kL_a = 1.07
s_cat = 0.14
f_ch_x = 0.2
f_pro_x = 0.55
k_d = 8.33e-4
k_hyd_NDF = 0.001875
k_hyd_NSC = 0.00625
k_hyd_pro = 0.009375
k_s_su = 9e-3
k_m_su = 0.99
k_s_IN = 2e-4
Y_su = 2e-4
lambda1 = 0.43
lambda2 = 0.29
lambda3 = 0.28
k_s_aa = 6.4e-3
k_m_aa = 1.98
Y_aa = 0.31
sigma_ac_aa = 0.67
sigma_bu_aa = 0.24
sigma_pr_aa = 0.062
sigma_H2_aa = 0.82
sigma_IC2_aa = 0.88
k_s_H2 = 5.84e-6
k_m_H2 = 13.93
Y_H2 = 0.0016

# Initial conditions
y0 = [2.5, 3.0, 1.25, 0.65, 0, 2, 28, 7.5, 5, 0, 140, 0, 0, 5, 1]  # Placeholder

# Example data (replace with actual values)
s_IN = 0.02    # Inorganic nitrogen concentration (mol/L), based on rumen fluid nitrogen content
s_su = 0.1     # Sugars concentration (mol/L), typical range for available carbohydrates in rumen
x_su = 0.02    # Concentration of sugars-utilizing microbes (g/L), based on microbial biomass in rumen
s_aa = 0.03    # Average amino acids concentration (mol/L), based on amino acid availability in rumen
x_aa = 0.03    # Concentration of amino acids-utilizing microbes (g/L), microbial biomass
s_H2 = 1e-6    # Hydrogen concentration in liquid phase (mol/L), based on typical H2 concentrations in rumen
x_H2 = 0.001   # Concentration of hydrogen-utilizing microbes (g/L), hydrogenotrophic microbes
pg_H2 = 0.01   # Partial pressure of hydrogen (atm), typically low in rumen
P_T_CH4 = 0.005  # Methane production rate (mol/L/hr), typical range in rumen methane production
P_T_CO2 = 0.01   # Carbon dioxide production rate (mol/L/hr), based on CO2 emissions from fermentation


# Equations
f_su = 1 - (5/6) * Y_su
Y_ac_su = f_su * (2 * lambda1 + (2/3) * lambda2)
Y_bu_su = f_su * lambda3
Y_pr_su = f_su * (4/3) * lambda2
Y_H2_su = f_su * (4 * lambda1 + 2 * lambda3)
Y_IN_su = -Y_su
Y_IC_su = f_su * (2 * lambda1 + (2/3) * lambda2 + 2 * lambda3)
f_H2 = 1 - 10 * Y_H2
Y_CH4_H2 = f_H2 * 0.25
Y_IC_H2 = ((-0.25 * f_H2) + 0.5 * (1 - f_H2))
Y_IN_H2 = -Y_H2
Y_H2_aa = (1 - Y_H2) * sigma_H2_aa
Y_ac_aa = (1 - Y_ac_su) * sigma_ac_aa
Y_bu_aa = (1 - Y_bu_su) * sigma_bu_aa
Y_pr_aa = (1 - Y_pr_su) * sigma_pr_aa
Y_IN_aa = 1 - Y_aa
Y_IC_aa = (1 - Y_IC_su) * sigma_IC2_aa
Y_IN = Y_IN_su


# Kinetic rates
def kinetic_rates(y):
    z_ndf, z_nsc, z_pro, s_su, s_aa, s_H2, s_ac, s_bu, s_pr, s_IN, s_IC, s_CH4, x_su, x_aa, x_H2 = y

    I_IN = s_IN / (s_IN + k_s_IN)
    P_NDF = k_hyd_NDF * z_ndf
    P_NSC = k_hyd_NSC * z_nsc
    P_pro = k_hyd_pro * z_pro
    P_su = k_m_su * (s_su / (k_s_su + s_su)) * x_su * I_IN
    P_aa = k_m_aa * (s_aa / (k_s_aa + s_aa)) * x_aa
    P_H2 = k_m_H2 * (s_H2 / (k_s_H2 + s_H2)) * x_H2 * I_IN
    P_x_su = k_d * x_su
    P_x_aa = k_d * x_aa
    P_x_H2 = k_d * x_H2
    P_T_H2 = kL_a * (s_H2 - KH_H2 * pg_H2)
    
    return P_NDF, P_NSC, P_pro, P_su, P_aa, P_H2, P_x_su, P_x_aa, P_x_H2, P_T_H2

# ODE system
def odeFunction(t, y):
    P_NDF, P_NSC, P_pro, P_su, P_aa, P_H2, P_x_su, P_x_aa, P_x_H2, P_T_H2 = kinetic_rates(y)

    dz_ndf = -P_NDF
    dz_nsc = -P_NSC + (f_ch_x * w_mb) * (P_x_su + P_x_aa + P_x_H2)
    dz_pro = -P_pro + (f_pro_x * w_mb) * (P_x_su + P_x_aa + P_x_H2)
    
    ds_su = (P_NDF / w_su) + (P_NSC / w_su) - P_su # * (y[9] / (y[9] + k_s_IN))  # y[9] = s_IN
    ds_aa = (P_pro / w_aa) - P_aa
    ds_H2 = Y_H2 * P_aa + Y_H2 * P_su - P_H2 - P_T_H2
    
    ds_ac = Y_ac_su * P_aa + Y_ac_aa * P_aa  
    ds_bu = Y_bu_su * P_su + Y_bu_aa * P_aa  
    ds_pr = Y_pr_su * P_su + Y_pr_aa * P_aa 

    ds_CH4 = Y_CH4_H2 * P_H2 - P_T_CH4
    ds_IC = Y_IC_aa * P_aa + Y_IC_su * P_su + Y_IC_H2 * P_H2 - P_T_CO2
    ds_IN = Y_IN_aa * P_aa + Y_IN_su * P_su + Y_IN_H2 * P_H2
    
    dx_su = Y_su * P_su - P_x_su
    dx_aa = Y_aa * P_aa - P_x_aa
    dx_H2 = Y_H2 * P_H2 - P_x_H2

    return [
        dz_ndf, dz_nsc, dz_pro, ds_su, ds_aa, ds_H2, ds_ac, ds_bu, ds_pr, ds_CH4, ds_IC, ds_IN, dx_su, dx_aa, dx_H2
    ]



# Time span
tspan = [0, 25]

# Solve the system of ODEs
sol = solve_ivp(odeFunction, tspan, y0, method='RK45')

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
    'x_H2 (g/L)'         # Hydrogen-utilizing microbes
]

# Create subplots (5 rows, 3 columns for 15 subplots)
fig, axes = plt.subplots(5, 3, figsize=(15, 10))
axes = axes.flatten() 
# Plot the solution with labeled units
for i in range(len(y0)):
    ax = axes[i]
    ax.plot(sol.t, sol.y[i], label=legend_labels[i])
    ax.set_title(legend_labels[i])
    ax.set_xlabel('Time (hours)')
    ax.set_ylabel(f'Concentration of {legend_labels[i]}')
    ax.legend()

plt.tight_layout()
plt.show()