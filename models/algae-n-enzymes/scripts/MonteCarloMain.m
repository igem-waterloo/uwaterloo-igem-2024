clear all;

numsimulations = 100;
resolution = 1000;
AA = [zeros([numsimulations resolution])];
BB = [zeros([numsimulations resolution])];
T_sol = zeros(resolution);

for i = 1:numsimulations

% Define the number of random numbers
n = 6;

% Define the ranges for each number as [min, max]

ranges = [
    0.04, 0.54;  % Range for Rhamnose
    0.004, 0.2;  % Range for Arabinose
    0.01, 0.73; % Range for Glucose 
    0, 0.26;  % Range for Galactose
    0, 0.19; % Range for Xylose
    0.025, 0.07   % Range for Mannose 
];

% Generate random numbers within the defined ranges
randomNumbers = zeros(1, n);
for k = 1:n
    randomNumbers(k) = ranges(k, 1) + (ranges(k, 2) - ranges(k, 1)) * rand();
end

% Calculate the adjustment factor
total = sum(randomNumbers);
adjustmentFactor = 1 / total;

% Adjust the numbers to sum to 1 while maintaining their proportion
adjustedNumbers = randomNumbers * adjustmentFactor;

RhaPer = adjustedNumbers(1);
AraPer = adjustedNumbers(2);
GluPer = adjustedNumbers(3);
FucPer = adjustedNumbers(4);
GalPer = adjustedNumbers(5);
ManPer = adjustedNumbers(6);

[t_sol,y_sol]=odeModel(GluPer, resolution);
CW_sol = y_sol/y_sol(2);
T_sol = t_sol;
%disp(size(CW_sol'));
%disp(size(AA))
%plot(t_sol,CW_sol);
for q = 1:resolution
AA(i,q)=CW_sol(q);
BB(i,q)=y_sol(q);
end
end

disp(AA);
avg = mean(AA);


figure(1)
hold on
title('Monte Carlo Concentration')
for l=1:size(BB,1)
plot(T_sol, BB(l,:), 'r', 'DisplayName', 'CW_concentration')
end
hold off;

figure(2)
hold on
title('Monte Carlo Percentage')
for p=1:size(AA,1)
plot(T_sol, AA(p,:), 'b')
end
ylabel('% Undegraded Cell Wall')
xlabel('Time (min)')
hold off;

figure(3)
title('Average')
hold on;
plot(T_sol, avg, 'g')
ylabel('% Undegraded Cell Wall')
xlabel('Time (min)')
hold off;

figure (4)
hold on;
title('Overlay')
for p=1:size(AA,1)
plot(T_sol, AA(p,:), 'b')
end
plot(T_sol, avg, 'g', 'LineWidth', 1.5)
ylabel('% Undegraded Cell Wall')
xlabel('Time (min)')
hold off;

figure (5)
hold on;
title('Degradation of C. vulgaris Over Time')
for p=1:size(AA,1)
plot(T_sol, 1-AA(p,:), 'b')
end
plot(T_sol, 1-avg, 'g', 'LineWidth', 1.5)
ylabel('% Degraded C. vulgaris')
xlabel('Time (min)')
hold off;
