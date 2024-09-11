clear all;
clc;

%Parameter of interest
%NDF = neutral detergent fibers (structural fibers)

%Numerical Parameters from paper

%Constants
Ka_CO2=5.13e-7;
Ka_NH4=1.44e-9;
Ka_VFA=1.74e-5;
KH_CO2=2.46e-2;
KH_CH4=1.1e-3;
KH_H2=7.23e-4;
Kw=2.75e-14;
P=1.01325;%bar
T=312.15;%K
V=0.03;%L
w_aa=134;
w_ac=60.05;
w_bu=88.1;
w_mb=113;
w_pr=74.08;
w_su=180.16;

%Estimated Parameters
kL_a=1.07;
s_cat=0.14;
f_ch_x=0.2;
f_pro_x=0.55;
k_d=8.33e-4;
k_hyd_NDF=0.05;
k_hyd_NSC=0.2;
k_hyd_pro=0.22;
k_s_su=9e-3;
k_m_su=0.99;
k_s_IN=2e-4;
Y_su=2e-4;
lambda1=0.43;
lambda2=0.29;
lambda3=0.28;
k_s_aa=6.4e-3;
k_m_aa=1.98;
Y_aa=0.31;
sigma_ac_aa=0.67;
sigma_bu_aa=0.24;
sigma_pr_aa=0.062;
sigma_H2_aa=0.82;
sigma_IC2_aa=0.88;
k_s_H2=5.84e-6;
k_m_H2=13.93;
Y_H2=0.0016;

% Initial Conditions
z_NDF_0 = 0;
z_NSC_0 = 0;
z_pro_0 = 0;
s_su_0 = 0;
s_aa_0 = 0;
s_H2_0 = 0; 
s_ac_0 = 0;
s_bu_0 = 0;
s_pr_0 = 0;
s_IN_0 = 0;
s_IC_0 = 0;
s_CH4_0 = 0;
x_su_0 = 0;
x_aa_0 = 0;
x_H2_0 = 0;

%Made-up numbers
s_IN = 1;
s_su = 2;
x_su = 3;
s_aa = 4;
x_aa = 5;
s_H2 = 6;
x_H2 = 7;
pg_H2 = 8;
P_T_CH4 = 9;
P_T_CO2 = 10;

%Kinetic Rates

I_IN = s_IN;
P_NDF = k_hyd_NDF * z_NDF_0;
P_NSC = k_hyd_NSC * z_NSC_0;
P_pro = k_hyd_pro * z_pro_0;
P_su = k_m_su * (s_su / (k_s_su + s_su)) * x_su; % Needs I_IN (y(10))
P_aa = k_m_aa * (s_aa / (k_s_aa + s_aa)) * x_aa;
P_H2 = k_m_H2 * (s_H2 / (k_s_H2 + s_H2)) * x_H2; % Needs I_IN (y(10))
P_x_su = k_d * x_su;
P_x_aa = k_d * x_aa;
P_x_H2 = k_d * x_H2;
P_T_H2 = kL_a*(s_H2-KH_H2*pg_H2);

% Equations from paper
f_su = 1 - (5/6) * Y_su;
Y_ac_su = f_su * (2 * lambda1 + (2/3) * lambda2);
Y_bu_su = f_su * lambda3;
Y_pr_su = f_su * (4/3) * lambda2;
Y_H2_su = f_su * (4 * lambda1 + 2 * lambda3);
Y_IN_su = -Y_su;
Y_IC_su = f_su * (2 * lambda1 + (2/3) * lambda2 + 2 * lambda3);
f_H2 = 1 - 10 * Y_H2;
Y_CH4_H2 = f_H2 * 0.25;
Y_IC_H2 = ((-0.25 * f_H2) + 0.5 * (1 - f_H2));
Y_IN_H2 = -Y_H2;
Y_H2_aa = (1 - Y_H2) * sigma_H2_aa;
Y_ac_aa = (1 - Y_ac_su) * sigma_ac_aa;
Y_bu_aa = (1 - Y_bu_su) * sigma_bu_aa;
Y_pr_aa = (1 - Y_pr_su) * sigma_pr_aa;
Y_IN_aa = 1 - Y_aa;
Y_IC_aa = (1 - Y_IC_su) * sigma_IC2_aa;
Y_IN = Y_IN_su;

%Petersen Matrix
pm = [-1, 0, 0, 1/w_su, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0;
      0, -1, 0, 1/w_su, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0;
      0, 0, -1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0;
      0, 0, 0, -1, 0, Y_H2_su, Y_ac_su, Y_bu_su, Y_pr_su, Y_IN_su, Y_IC_su, 0, Y_su, 0, 0;
      0, 0, 0, 0, -1, Y_H2_aa, Y_ac_aa, Y_bu_aa, Y_pr_aa, Y_IN_aa, Y_IC_aa, 0, 0, Y_aa, 0;
      0, 0, 0, 0, 0, -1, 0, 0, 0, Y_IN_H2, Y_IC_H2, Y_CH4_H2, 0, 0, Y_H2;
      0, f_ch_x*w_mb, f_pro_x*w_mb, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0;
      0, f_ch_x*w_mb, f_pro_x*w_mb, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0;
      0, f_ch_x*w_mb, f_pro_x*w_mb, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1];

y0 = [z_NDF_0, z_NSC_0, z_pro_0, s_su_0, s_aa_0, s_H2_0, s_ac_0, s_bu_0, s_pr_0, s_IN_0, s_IC_0, s_CH4_0, x_su_0, x_aa_0, x_H2_0];

Sz = size(pm)
Sz = size(y0)

tspan=[0,1];
% WARNING: Make sure P_su and P_H2 are multiplied by y(10)
odeFunction = @(t,y) [
    -P_NDF;
    -P_NSC+(f_ch_x*w_mb)*(P_x_su+P_x_aa+P_x_H2);
    -P_pro+(f_pro_x*w_mb)*(P_x_su+P_x_aa+P_x_H2);
    (P_NDF/w_su)+(P_NSC/w_su)-P_su*(y(10)/(y(10)+k_s_IN));
    (P_pro/w_aa)-P_aa;
    Y_H2_aa*P_aa+Y_H2_su*P_su*(y(10)/(y(10)+k_s_IN))-P_H2*(y(10)/(y(10)+k_s_IN))-P_T_H2;
    Y_ac_su*P_aa+Y_ac_aa*P_aa;
    Y_bu_su*P_su+Y_bu_aa*P_aa;
    Y_pr_su*P_su+Y_pr_aa*P_aa;
    Y_CH4_H2*P_H2-P_T_CH4;
    Y_IC_aa*P_aa+Y_IC_su*P_su+Y_IC_H2*P_H2-P_T_CO2;
    Y_IN_aa*P_aa+Y_IN_su*P_su+Y_IN_H2*P_H2;
    Y_su*P_su-P_x_su;
    Y_aa*P_aa-P_x_aa;
    Y_H2*P_H2-P_x_H2;
]
[t,y] = ode45(odeFunction, tspan, y0);

plot(t,y);
