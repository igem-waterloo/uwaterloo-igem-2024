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
yy_su = 2e-4
l_1 = 0.43
l_2 = 0.29
l_3 = 0.28
k_s_aa = 6.4e-3
k_m_aa = 1.98
yy_aa = 0.31
sigma_ac_aa = 0.67
sigma_bu_aa = 0.24
sigma_pr_aa = 0.062
sigma_H2_aa = 0.82
sigma_IC2_aa = 0.88
k_s_H2 = 5.84e-6
k_m_H2 = 13.93
yy_H2 = 0.0016

# Initial Conditions
z_ndf_0 = 2.5
z_nsc_0 = 3.0
z_pro_0 = 1.25
s_su_0 = 0.65
s_aa_0 = 0
s_H2_0 = 2
s_ac_0 = 28
s_bu_0 = 7.5
s_pr_0 = 5
s_IC_0 = 140
s_IN_0 = 0
s_CH4_0 = 0
x_su_0 = 0
x_aa_0 = 5
x_H2_0 = 1

# Define the system of ODEs
def odes(t, y):
    z_ndf, z_nsc, z_pro, s_su, s_aa, s_H2, s_ac, s_bu, s_pr, s_IN, s_IC, s_CH4, x_su, x_aa, x_H2 = y

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
    
    # Gas phase
    p_T_H2 = k_L_a * (s_H2 - k_H_H2 * p_H2)
    p_T_CO2 = k_L_a * (s_IC - k_H_CO2 * s_IC)
    p_T_CH4 = k_L_a * (s_CH4 - k_H_CH4 * s_CH4)
    
    # Equations
    dz_ndf = -p_ndf
    dz_nsc = -p_nsc + f_ch_x * (p_xsu + p_xaa + p_xh2)
    dz_pro = -p_pro + f_pro_x * (p_xsu + p_xaa + p_xh2)
    
    ds_su = p_ndf / w_su + p_nsc / w_su - p_su
    ds_aa = p_pro / w_aa - p_aa
    ds_H2 = yy_aa * p_aa + yy_su * p_su - p_H2 - p_T_H2
    ds_ac = p_su * (2 * l_1 + (2 / 3) * l_2) + p_aa * (1 - yy_aa)
    ds_bu = f_ch_x * l_3
    ds_pr = p_su * (4 / 3) * l_2 + p_aa * (1 - sigma_pr_aa)
    ds_CH4 = yy_H2 * p_H2 - p_T_CH4
    
    ds_IC = p_aa * (1 - sigma_IC2_aa) + p_su * (2 * l_1 + (2 / 3) * l_2) + p_H2 * (1 - sigma_IC2_aa) - p_T_CO2
    ds_IN = (1 - sigma_ac_aa) * p_aa + p_su * (1 - sigma_H2_aa)
    
    dx_su = yy_su * p_su - p_xsu
    dx_aa = yy_aa * p_aa - p_xaa
    dx_H2 = yy_H2 * p_H2 - p_xh2
    
    return [dz_ndf, dz_nsc, dz_pro, ds_su, ds_aa, ds_H2, ds_ac, ds_bu, ds_pr, ds_IN, ds_IC, ds_CH4, dx_su, dx_aa, dx_H2]

# Initial conditions vector
y0 = [z_ndf_0, z_nsc_0, z_pro_0, s_su_0, s_aa_0, s_H2_0, s_ac_0, s_bu_0, s_pr_0, s_IN_0, s_IC_0, s_CH4_0, x_su_0, x_aa_0, x_H2_0]

# Time span
tspan = [0, 1]

# Solving the ODE system
sol = solve_ivp(odes, tspan, y0, method='RK45')

# Plot results
for i in range(len(y0)):
    plt.plot(sol.t, sol.y[i], label=f'y{i+1}')
plt.legend()
plt.xlabel('Time')
plt.ylabel('y(t)')
plt.title('ODE Solution')
plt.show()