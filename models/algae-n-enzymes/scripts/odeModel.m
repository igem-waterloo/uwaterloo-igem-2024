function [t_sol,y_sol] = odeModel(GluPer,resolution)

%Parameters
ST = 0;
CW = 0.05;
GLU = 1e-4;
PYR = 1e-8;
LAC = 1e-3;
ACL = 2e-6;
PRO = 0.02;
ACP = 4e-4;
ACE = 0.07;
ACA = 1e-3;
BUT = 0.01;
ACB = 2e-4;
VAL = 0.0008;
ACV = 2e-4;
CH4 = 0.03;
CO2 = 0.7;
H2 = 0.0005;
HCO3 = 0.08;
HPLUS = 3e-7;
NADH = 1e-3;
NAD = 1e-3;
ATP = 1.5e-3;
ADP = 1.5e-3;
MDM = 2;

k = 1;
C = 10;
KA = 1e2;
KA1 = 0.0001;
KA2 = 0.005;
KCW = 0.0008;
KOUTCW = 0.0001;
KST = 0.003;
KOUTST = 0.0001;
KM = 0.0001;
KMU = 0.075;
MUBAS = 0.001;

%Constants
F = 96.487;
R = 0.00831451;
T = 311;
Gibbs = -9;

%Redox potientials
EvOV = 0.512;        %Pyruvate/Valerate
EvOL = 0.418;        %Lactate/Propionate
EvOPP = 0.318;       %Pyruvate/Propionate
EvOP = 0.229;        %Pyruvate/Lactate
EvOCO2ch = 0.170;    %CO2/CH4
EvOCO2ac = 0.124;    %CO2/Acetate
EvOH = 0;            %H+/H2
EvON = -0.113;       %NAD/NADH
EvOA = -0.228;       %Acetate/Pyruvate
EvOG = -0.290;       %Pyruvate/Glucose

%pKA values
pKhco = 7.74;        %HCO3-
pKlac = 3.86;        %Lactate
pKpro = 4.87;        %Propionate
pKace = 4.75;        %Acetate
pKbut = 4.82;        %Butyrate
pKval = 4.84;        %Valerate

%Auxilliary variables

%Ratio NADH/NAD, ATP/ADP
RNHN = NADH/NAD;
RATDP = ATP/ADP;

%VFA molar proportions
SOMVFA = ACE + ACA + PRO + ACP + BUT + ACB + VAL + ACV;   %Total sum of VFA
PACE = 100 * (ACA + ACE)/SOMVFA;    %Respective proportions of each VFA
PPRO = 100 * (ACP + PRO)/SOMVFA;
PBUT = 100 * (ACB + BUT)/SOMVFA;
PVAL = 100 * (ACV + VAL)/SOMVFA;
ACEsPRO = (ACE + ACA)/(PRO + ACP);  %Acetate to propionate ratio

%pH calculation
PH =-log10(HPLUS);                  %pH calculation in a mechanistic way
PHVFA = 6.96 - 6.94 * SOMVFA;       %pH calculation in an empirical way using [VFA - volatile fatty acids]
PHCO3 = pKhco + log10(HCO3/CO2);      %Calculation for each acid using pKa
PHACE = pKace + log10(ACE/ACA);
PHPRO = pKpro + log10(PRO/ACP);
PHBUT = pKbut + log10(BUT/ACB);
PHLAC = pKlac + log10(LAC/ACL);
PHVAL = pKval + log10(VAL/ACV);

%Gas pressures
PRES = CH4 + CO2 + H2;        %Total pressure in the rumen
XCH4 = CH4/PRES;              %Partial pressures
XCO2 = CO2/PRES;
XH2 = H2/PRES;

%Thermodynamical variables

%Standard potentials of each redox couple at rumen pH
Ev0pHN = EvON - (R*T / (2*F)) * log(10) * PH;
Ev0pHG = EvOG - (6*R*T/(8*F)) * log(10) * PH;
Ev0pHP = EvOP - (R*T/F) * log(10) * PH;
Ev0pHL = EvOL - (R*T/F) * log(10) * PH;
Ev0pHPP = EvOPP - (R*T/F) * log(10) * PH;
Ev0pHA = EvOA - (R*T/F) * log(10) * PH;
Ev0pHH = EvOH - (R*T/F) * log(10) * PH;
Ev0pHCch = EvOCO2ch - (R*T/F) * log(10) * PH;
Ev0pHCac = EvOCO2ac - (7*R*T/(8*F)) * log(10) * PH;
Ev0pHV = EvOV - (7*R*T/(6*F)) * log(10) * PH;

%Standard potentials of rxns at rumen pH
Ev0pHr1 = Ev0pHN - Ev0pHG;
Ev0pHr2 = Ev0pHP - Ev0pHN;
Ev0pHr3 = Ev0pHL - Ev0pHN;
Ev0pHr4 = Ev0pHPP - Ev0pHN;
Ev0pHr5 = Ev0pHN - Ev0pHA;
Ev0pHr7 = Ev0pHV - Ev0pHN;
Ev0pHr8 = Ev0pHCch - Ev0pHN;
Ev0pHr9 = Ev0pHCac - Ev0pHN;
Ev0pHr10 = Ev0pHH - Ev0pHN;

%Gibbs energies of the rxns
G0pHr1 = -4*F * Ev0pHr1;
G0pHr2 = -2*F * Ev0pHr2;
G0pHr3 = -2*F * Ev0pHr3;
G0pHr4 = -4*F * Ev0pHr4;
G0pHr5 = -2*F * Ev0pHr5;
G0pHr6 = -177.7 + R*T * log(10) * PH;
G0pHr7 = -6*F * Ev0pHr7;
G0pHr8 = -8*F * Ev0pHr8;
G0pHr9 = -8*F * Ev0pHr9;
G0pHr10 = -2*F * Ev0pHr10;

%Gibbs energy for ATP formation
G0ATPpH = Gibbs + R*T * log(10) * PH;

%Equilibrium constants of the rxns
Keq1 = exp(-(G0pHr1 + 2*G0ATPpH)/R*T);
Keq2 = exp(Ev0pHr2 /(R*T/2*F));
Keq3 = exp(Ev0pHr3 /(R*T/2*F));
Keq4 = exp(-(G0pHr4 + G0ATPpH) /R*T);
Keq5 = exp(-(G0pHr5 + G0ATPpH) /R*T);
Keq6 = exp(-(G0pHr6 + G0ATPpH) /R*T);
Keq7 = exp(-G0pHr7 /R*T);
Keq8 = exp(-(G0pHr8 + G0ATPpH) /R*T);
Keq9 = exp(-(G0pHr9 + 0.25*G0ATPpH) /R*T);
Keq10 = exp((EvOH - EvON) /(R*T/2*F));
Keq11 = 1/10^(-pKhco);
Keq12 = 1/10^(-pKlac);
Keq13 = 1/10^(-pKpro);
Keq14 = 1/10^(-pKace);
Keq15 = 1/10^(-pKbut);
Keq16 = 1/10^(-pKval);

%Gibbs energy of the rxns in rumen conditions
Gr1 = G0pHr1 + 2*G0ATPpH + R*T * log(((PYR^2)*(NADH^2)*(ATP^2)) / (GLU *(NAD^2)*(ADP^2)));
Gr2 = G0pHr2 + R*T * log((LAC * NAD) /(PYR * NADH));
Gr3 = G0pHr3 + R*T * log((PRO * NAD) /(LAC * NADH));
Gr4 = G0pHr4 + G0ATPpH + R*T * log((PRO * ATP * (NAD^2)) /(PYR * ADP * (NADH^2)));
Gr5 = G0pHr5 + G0ATPpH + R*T * log((ACE * NADH * CO2 * ATP) /(PYR * NAD * ADP));
Gr6 = G0pHr6 + G0ATPpH + R*T * log((BUT * ATP * (CO2^2))/((PYR^2) * ADP));
Gr7 = G0pHr7 + R*T * log((VAL * CO2 * (NAD^3))/((PYR^2) * (NADH^3)));
Gr8 = G0pHr8 + G0ATPpH + R*T * log((CH4 * (NAD^4)* ATP)/(CO2 * (NADH^4) * ADP));
Gr9 = G0pHr9 + 0.25*G0ATPpH + R*T * log((ACE * (NAD^4) * (ATP^(0.25))) /((CO2^2) * (NADH^4) * (ADP^(0.25))));
Gr10 = G0pHr10 + R*T * log((H2 * NAD)/NADH);
Gr11 = R*T * log((CO2/HCO3)/Keq11);
Gr12 = R*T * log((ACL/LAC)/Keq12);
Gr13 = R*T * log((ACP/PRO)/Keq13);
Gr14 = R*T * log((ACA/ACE)/Keq14);
Gr15 = R*T * log((ACB/BUT)/Keq15);
Gr16 = R*T * log((ACV/VAL)/Keq16);

%Potential values of each couple
ENAD = Ev0pHN + (R*T/2*F) * log(NAD/NADH);
EGLU = Ev0pHG + (R*T/4*F) * log((PYR^2)/(GLU));
EPYR = Ev0pHP + (R*T/2*F) * log(PYR/LAC);
ELAC = Ev0pHL + (R*T/2*F) * log(LAC/PRO);
EPRO = Ev0pHPP + (R*T/(4*F)) * log(PYR/PRO);
EACE = Ev0pHA +(R*T/2*F) * log((ACE * CO2)/PYR);
EH = Ev0pHH + (R*T/2*F) * log(1/H2);
ECO2ch = Ev0pHCch + (R*T/8*F) * log(CO2/CH4);
ECO2ac = Ev0pHCac + (R*T/8*F) * log(CO2^2/ACE);
EVAL = Ev0pHV + (R*T/6*F) * log((PYR^2)/(VAL * CO2));

%Determination of average redox potential in the rumen
H2M = 0.0008143 * H2;         %Gas concentrations determined thanks to the Henry constant
CO2M = 0.0229 * CO2;
CH4M = 2 * 10^(-5) * CH4;

SOMOL = GLU + PYR + LAC + PRO + ACE + VAL + NAD + NADH + H2M + HPLUS + CO2M + CH4M;

PROPNAD = (NAD + NADH) /SOMOL;   %Calculation of the weighting aﬀected to eachredox couple
PROPGLPY = (GLU + (2/7)*PYR) /SOMOL;
PROPPYLA = ((1/7)*PYR + (1/2)*LAC) /SOMOL;
PROPLAPRO = ((1/2)*LAC + (1/2)*PRO) /SOMOL;
PROPPROPY = ((1/2)*PRO + (1/7)*PYR) /SOMOL;
PROPPYAC = ((1/7)*PYR + (1/2)*ACE + (1/5)*CO2M) /SOMOL;
PROPHPH2 = (HPLUS + H2M) /SOMOL;
PROPCOCH4 = ((1/5)*CO2M + CH4M) /SOMOL;
PROPCOAC = ((2/5)*CO2M + (1/2)*ACE) /SOMOL;
PROPPYVAL = ((2/7)*PYR + VAL +(1/5)*CO2M) /SOMOL;
EPMOY = (ENAD * PROPNAD) + (EGLU * PROPGLPY) + (EPYR * PROPPYLA) + (ELAC * PROPLAPRO) + (EPRO * PROPPROPY) + (EACE * PROPPYAC) + (EH * PROPHPH2) + (ECO2ch * PROPCOCH4) + (ECO2ac * PROPCOAC) +(EVAL * PROPPYVAL);

%Difference to average potential
DEGLU = EPMOY - EGLU;
DEPYR = EPYR - EPMOY;
DELAC = ELAC - EPMOY;
DEPRO = EPRO - EPMOY;
DEACE = EPMOY - EACE;
DEH = EH - EPMOY;
DECO2CH = ECO2ch - EPMOY;
DECO2AC = ECO2ac - EPMOY;
DEVAL = EVAL - EPMOY;

%Potentials of oxydoreduction rxns
Evr1 = ENAD - EGLU;
Evr2 = EPYR - ENAD;
Evr3 = ELAC - ENAD;
Evr4 = EPRO - ENAD;
Evr5 = ENAD - EACE;
Evr7 = EVAL - ENAD;
Evr8 = ECO2ch - ENAD;
Evr9 = ECO2ac - ENAD;
Evr10 = EH - ENAD;

%Params of Pulse signal
amplitude = 50/180;             %Amplitude of pulse
pulse_duration = 1;             %Duration of each pulse
t_start = 0;                    %Time of the first pulse
period = 1440;                  %Period of pulse repetition
t_end = 2880;                   %Total simulation time
t = 0:t_end;                    %Time vector

%Cell wall compartment (CW)

%INCW pulse signal
INCW = amplitude * (mod(t - t_start, period) < pulse_duration);
%Interpolate INCW to make it continuous for the ODE solver
INCW_interp = @(t_interp) interp1(t, INCW, t_interp, 'previous', 0);

CWGLU = KCW * GluPer * CW;
OUTCW = KOUTCW * CW;

%Starch compartment (ST)

%INST pulse signal
INST = amplitude * (mod(t - t_start, period) < pulse_duration);
%Interpolate INST to make it continuous for the ODE solver
INST_interp = @(t_interp) interp1(t, INST, t_interp, 'previous', 0);

STGLU = KST * ST;
OUTST = KOUTST * ST;

%Glucose compartment (GLU)

    %Glucose-pyruvate (1)
GLPY = 2E10 * GLU * (NAD)^2 * (ADP)^2 * exp(C * DEGLU);
PYGL = (2E10/Keq1) * (PYR)^2 * (NADH)^2 * (ATP)^2 * exp(-C * DEGLU);
OUTGLU = 0.0001 * GLU;

%Pyruvate compartment (PYR)
OUTPY = KA2 * PYR;
    %Pyruvate-lactate (2)
PYLA = k * PYR * NADH * exp(C * DEPYR);
LAPY = (k/Keq4) * PRO * ATP * NAD * exp(-C * DEPRO);
    %Pyruvate-propionate (4) via succinate
PYPRO = 100 * k * PYR * ADP * (NADH)^2 * exp(C * DEPRO);
PROPY =(100 * k/Keq4) * PRO * ATP * (NAD)^2 * exp(-C * DEPRO);
    %Pyruvate-acetate (5)
PYAC = 10000 * k * PYR * NAD * ADP * exp(C * DEACE);
ACPY = (10000 * k/Keq5) * ACE * NADH * CO2 * ATP * exp(-C * DEACE);
    %Pyruvate-butyrate (6)
PYBU = 1000 * k * (PYR)^2 * ADP;
BUPY = (1000 * k/Keq6) * BUT * ATP * (CO2)^2;
    %Pyruvate-valerate (7)
PYVAL = k * (PYR)^2 * (NADH)^3 * exp(C * DEVAL);
VALPY = (k /Keq7) * VAL * CO2 * (NAD)^3 * exp(-C * DEVAL);

%Lactate compartment (LAC)
OUTLAC = KA2 * LAC;
    %Lactate-propionate (3)
LAPRO = k * LAC * NADH * exp(C * DELAC);
PROLA = (k /Keq3) * PRO * NAD * exp(-C * DELAC);
    %Lactic acid formation (12)
LACA = KA * LAC * HPLUS;
ALAC = (KA /Keq12) * ACL;

%Microbial compartment
%diff(MDM,t) == CRMDM - LYSMDM - OUTMDM;
OUTMDM = KM * MDM;
CRMDM = MUBAS * MDM * exp(KMU * (RATDP - 1));
LYSMDM = MUBAS * MDM * exp(-KMU * (RATDP - 1));
BCRMDM = CRMDM - LYSMDM;          %Apparent Growth
SCRMDM = max(0, BCRMDM - 0);      %Replace RAMP(BCRMDM,0) with max(0, BCRMDM - 0)
MUAMDM = 60 * BCRMDM/MDM;         %Apparent growth rate in h^−1
MURMDM = 60 * CRMDM/MDM;          %Real growth rate in h^−1
UTCM = CRMDM/25;                  %C mol used for growth
    %ATP utilizing ﬂow by microorganisms
ATPMM = 0.001 * 1.6 * MDM/60;     %Maintenance
BESATPM = CRMDM/30;               %Growth
    %C outﬂow for microorganism growth
PYMIC = BCRMDM/25;                %C pyruvate mol used
    %NADH utilizing ﬂow by microorganisms
NADHMM = 1*10^(-5) * MDM;         %Maintenance
BESNADHM = 0.5 * UTCM;            %Growth


%DEs for the ODE solver:
ode_system = @(t, y) [
  
  %y(1) corresponds to CW
  %dCW/dt = INCW - CWGLU - OUTCW
  INCW_interp(t) - KCW * GluPer * y(1) - KOUTCW * y(1);

];

initial_conditions = [CW];
%Solve the system of DEs using ode45
[t_sol, y_sol] = ode45(ode_system, linspace(0,t_end,resolution), initial_conditions);

%Extract solutions
CW_sol = y_sol(:, 1);

%plot(t_sol, CW_sol, 'r', 'DisplayName', 'CW_percentage');

hold on;
%plot(t_sol, LAC_sol, 'c', 'DisplayName', 'LAC');
xlabel('Time (min)');
ylabel('Concentration (mol/L)');
%legend show;
title('Compartment Concentrations over Time');