clear all;

numsimulations = 50;
resolution = 1000;
AA = [zeros([numsimulations resolution])];
BB = [zeros([numsimulations resolution])];
T_sol = zeros([numsimulations resolution]);
AV = [zeros([numsimulations 2])];

for i = 1:numsimulations

t_min = 60*24;
t_max = 60*24*2;
t_end = t_min+(t_max-t_min)*rand();
%disp(t_end);
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

[t_sol,y_sol]=odeModelMulti(GluPer, resolution, t_end);
%disp(size(t_sol));
CW_sol = y_sol/y_sol(2);
%disp(size(CW_sol'));
%disp(size(AA))
%plot(t_sol,CW_sol);
for q = 1:resolution
AA(i,q)=CW_sol(q);
BB(i,q)=y_sol(q);
T_sol(i,q) = t_sol(q);
end
AV(i,1) = t_sol(resolution);
AV(i,2) = y_sol(resolution);
end

%disp(AA);
avg = mean(AA);
%disp(AV);
disp("AVERAGE");
disp(mean(AV));

% figure(1)
% hold on
% title('Monte Carlo Concentration')
% for l=1:size(BB,1)
% plot(T_sol, BB(l,:), 'r', 'DisplayName', 'CW_concentration')
% end
% hold off;
% 
% figure(2)
% hold on
% title('Monte Carlo Percentage')
% for p=1:size(AA,1)
% plot(T_sol, AA(p,:), 'b')
% end
% ylabel('% Undegraded Cell Wall')
% xlabel('Time (min)')
% hold off;
% 
% figure(3)
% title('Average')
% hold on;
% plot(T_sol, avg, 'g')
% ylabel('% Undegraded Cell Wall')
% xlabel('Time (min)')
% hold off;
% 
% figure (4)
% hold on;
% title('Overlay')
% for p=1:size(AA,1)
% plot(T_sol(p,:), AA(p,:), 'b')
% end
% plot(T_sol, avg, 'g', 'LineWidth', 1.5)
% ylabel('% Undegraded Cell Wall')
% xlabel('Time (min)')
% hold off;
% 
% figure (5)
% hold on;
% title('Degradation of C. vulgaris Over Time')
% for p=1:size(AA,1)
% plot(T_sol(p,:), 1-AA(p,:), 'b')
% end
% plot(T_sol, 1-avg, 'g', 'LineWidth', 1.5)
% ylabel('% Degraded C. vulgaris')
% xlabel('Time (min)')
% xlim([5 1000])
% % legend()
% hold off;