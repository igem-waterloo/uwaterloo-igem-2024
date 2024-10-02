% initialize the ode system as a function of time, where y is the
% concentration of the state.
function [t, q, y, z] = fermentation_model_for_app(initial_conditions, reduced_initial_conditions)
    y0 = initial_conditions;
    y0_reduced_methanogen = reduced_initial_conditions;

    tspan = [0 30];

    % Solving the system
    [t, y] = ode45(@(t, y) system_fct(t, y), tspan, y0);
    [q, z] = ode45(@(q, z) reduced_methanogen_system_fct(q, z), tspan, y0_reduced_methanogen);
    size(t)
    size(y)
    size(q)
    size(z)
end

function dydt = system_fct(t,y)

    % constants
    KH_CO2=2.46e-2;
    KH_CH4=1.1e-3;
    KH_H2=7.23e-4;
    w_aa=134;
    w_mb=113;
    w_su=180.16;
    Vl = 0.03;
    
    % estimated parameters (Tamayo et al.)
    kL_a=1.07;
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
       
    % Kinetic Rates of each state variable.
    I_IN = y(12)/(y(12)+k_s_IN);
    P_NDF = k_hyd_NDF * y(1);
    P_NSC = k_hyd_NSC * y(2);
    P_pro = k_hyd_pro * y(3);
    P_su = k_m_su * (y(4) / (k_s_su + y(4))) * y(13) * I_IN; % Needs I_IN (y(10))
    P_aa = k_m_aa * (y(5) / (k_s_aa + y(5))) * y(14);
    P_H2 = k_m_H2 * (y(6) / (k_s_H2 + y(6))) * y(15) * I_IN; % Needs I_IN (y(10))
    P_x_su = k_d * y(13);
    P_x_aa = k_d * y(14);
    P_x_H2 = k_d * y(15);

    % Gas conversion
    P = 1.01325;
    pg_H2 = y(16) / ( y(16) + y(17) + y(18) ) *  P;
    pg_CO2 = y(17) / ( y(16) + y(17) + y(18) ) *  P;
    pg_CH4 = y(18) / ( y(16) + y(17) + y(18) ) *  P;
    P_T_H2 = kL_a*(y(6)-KH_H2*pg_H2);
    P_T_CO2 = kL_a*(y(7)-KH_CO2*pg_CO2);
    P_T_CH4 = kL_a*(y(10)-KH_CH4*pg_CH4);

    
    % Yield functions
    f_su = 1 - (5/6) * Y_su;
    Y_ac_su = f_su * (2 * lambda1 + (2/3) * lambda2);
    Y_bu_su = f_su * lambda3;
    Y_pr_su = f_su * (4/3) * lambda2;
    Y_H2_su = f_su * (4 * lambda1 + 2 * lambda3);
    Y_IN_su = -Y_su;
    Y_IC_su = f_su * (2 * lambda1 + (2/3) * lambda2 + 2 * lambda3);
    f_H2 = 1 - 10 * Y_H2;
    Y_CH4_H2 = f_H2 * 0.25;
    Y_IC_H2 = -((0.25 * f_H2) + 0.5 * (1 - f_H2));
    Y_IN_H2 = -Y_H2;
    Y_H2_aa = (1 - Y_H2) * sigma_H2_aa;
    Y_ac_aa = (1 - Y_ac_su) * sigma_ac_aa;
    Y_bu_aa = (1 - Y_bu_su) * sigma_bu_aa;
    Y_pr_aa = (1 - Y_pr_su) * sigma_pr_aa;
    Y_IN_aa = 0.067 - Y_aa*0.059;
    Y_IC_aa = (1 - Y_IC_su) * sigma_IC2_aa;

     % System of DEs
    dydt = zeros(18, 1);
    dydt(1) = -P_NDF;
    dydt(2) = -P_NSC+(f_ch_x*w_mb)*(P_x_su+P_x_aa+P_x_H2);
    dydt(3) = -P_pro+(f_pro_x*w_mb)*(P_x_su+P_x_aa+P_x_H2);
    dydt(4) = (P_NDF/w_su)+(P_NSC/w_su)-P_su;
    dydt(5) = (P_pro/w_aa)-P_aa;
    dydt(6) = Y_H2_aa*P_aa+Y_H2_su*P_su-P_T_H2;
    dydt(7) = Y_ac_su*P_su+Y_ac_aa*P_aa;
    dydt(8) =  Y_bu_su*P_su+Y_bu_aa*P_aa;
    dydt(9) = Y_pr_su*P_su+Y_pr_aa*P_aa;
    dydt(10) = Y_CH4_H2*P_H2-P_T_CH4;
    dydt(11) = Y_IC_aa*P_aa+Y_IC_su*P_su+Y_IC_H2*P_H2-P_T_CO2;
    dydt(12) = Y_IN_aa*P_aa+Y_IN_su*P_su+Y_IN_H2*P_H2;
    dydt(13) = Y_su*P_su-P_x_su;
    dydt(14) = Y_aa*P_aa-P_x_aa;
    dydt(15) = Y_H2*P_H2-P_x_H2;
    dydt(16) = Vl * P_T_H2;
    dydt(17) = Vl * P_T_CO2;
    dydt(18) = Vl * P_T_CH4;
  
end

% Reduced methanogenic state

function dzdt = reduced_methanogen_system_fct(q,z)
% constants
    KH_CO2=2.46e-2;
    KH_CH4=1.1e-3;
    KH_H2=7.23e-4;
    w_aa=134;
    w_mb=113;
    w_su=180.16; 
    Vl = 0.03;
    P = 1.01325;
    
    % estimated parameters (Tamayo et al.)
    kL_a=1.07;
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

 % Kinetic Rates of each state variable.
    I_IN = z(12)/(z(12)+k_s_IN);
    P_NDF = k_hyd_NDF * z(1);
    P_NSC = k_hyd_NSC * z(2);
    P_pro = k_hyd_pro * z(3);
    P_su = k_m_su * (z(4) / (k_s_su + z(4))) * z(13) * I_IN
    P_aa = k_m_aa * (z(5) / (k_s_aa + z(5))) * z(14);
    P_H2 = k_m_H2 * (z(6) / (k_s_H2 + z(6))) * z(15) * I_IN;
    P_x_su = k_d * z(13);
    P_x_aa = k_d * z(14);
    P_x_H2 = k_d * z(15);
    pg_H2 = z(16) / ( z(16) + z(17) + z(18) ) *  P;
    pg_CO2 = z(17) / ( z(16) + z(17) + z(18) ) *  P;
    pg_CH4 = z(18) / ( z(16) + z(17) + z(18) ) *  P;
    P_T_H2 = kL_a*(z(6)-KH_H2*pg_H2);
    P_T_CO2 = kL_a*(z(7)-KH_CO2*pg_CO2);
    P_T_CH4 = kL_a*(z(10)-KH_CH4*pg_CH4);

    % Yield equations
    f_su = 1 - (5/6) * Y_su;
    Y_ac_su = f_su * (2 * lambda1 + (2/3) * lambda2);
    Y_bu_su = f_su * lambda3;
    Y_pr_su = f_su * (4/3) * lambda2;
    Y_H2_su = f_su * (4 * lambda1 + 2 * lambda3);
    Y_IN_su = -Y_su;
    Y_IC_su = f_su * (2 * lambda1 + (2/3) * lambda2 + 2 * lambda3);
    f_H2 = 1 - 10 * Y_H2;
    Y_CH4_H2 = f_H2 * 0.25;
    Y_IC_H2 = -((0.25 * f_H2) + 0.5 * (1 - f_H2));
    Y_IN_H2 = -Y_H2;
    Y_H2_aa = (1 - Y_H2) * sigma_H2_aa;
    Y_ac_aa = (1 - Y_ac_su) * sigma_ac_aa;
    Y_bu_aa = (1 - Y_bu_su) * sigma_bu_aa;
    Y_pr_aa = (1 - Y_pr_su) * sigma_pr_aa;
    Y_IN_aa = 0.067 - Y_aa*0.059;
    Y_IC_aa = (1 - Y_IC_su) * sigma_IC2_aa;

    % system of DEs
    dzdt = zeros(18, 1);
    dzdt(1) = -P_NDF;
    dzdt(2) = -P_NSC+(f_ch_x*w_mb)*(P_x_su+P_x_aa+P_x_H2);
    dzdt(3) = -P_pro+(f_pro_x*w_mb)*(P_x_su+P_x_aa+P_x_H2);
    dzdt(4) = (P_NDF/w_su)+(P_NSC/w_su)-P_su;
    dzdt(5) = (P_pro/w_aa)-P_aa;
    dzdt(6) = Y_H2_aa*P_aa+Y_H2_su*P_su-P_T_H2;
    dzdt(7) = Y_ac_su*P_su+Y_ac_aa*P_aa;
    dzdt(8) =  Y_bu_su*P_su+Y_bu_aa*P_aa;
    dzdt(9) = Y_pr_su*P_su+Y_pr_aa*P_aa;
    dzdt(10) = Y_CH4_H2*P_H2-P_T_CH4;
    dzdt(11) = Y_IC_aa*P_aa+Y_IC_su*P_su+Y_IC_H2*P_H2-P_T_CO2;
    dzdt(12) = Y_IN_aa*P_aa+Y_IN_su*P_su+Y_IN_H2*P_H2;
    dzdt(13) = Y_su*P_su-P_x_su;
    dzdt(14) = Y_aa*P_aa-P_x_aa;
    dzdt(15) = Y_H2*P_H2-P_x_H2;
    dzdt(16) = Vl * P_T_H2;
    dzdt(17) = Vl * P_T_CO2;
    dzdt(18) = Vl * P_T_CH4;
end


