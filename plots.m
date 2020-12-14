clc
clear all
close all

%%
% Steering Plots

steerX = linspace(-30, 30, 500);
steerX1 = linspace(-3, 3, 500);
steer11 = trapmf(steerX, [-30, -30, -20, -10]);
steer12 = trimf(steerX, [-20, -10, 0]);
steer13 = trimf(steerX, [-1, 0, 1]);
steer14 = trimf(steerX, [0, 10, 20]);
steer15 = trapmf(steerX, [10, 20, 30, 30]);
steer21 = trapmf(steerX1, [-3, -3, -2, -1]);
steer22 = trimf(steerX1, [-2, -1, 0]);
steer23 = trimf(steerX1, [-0.25, 0, 0.25]);
steer24 = trimf(steerX1, [0, 1, 2]);
steer25 = trapmf(steerX1, [1, 2, 3, 3]);



figure(1)
hold on
plot(steerX,steer11)
plot(steerX,steer12)
plot(steerX,steer13)
plot(steerX,steer14)
plot(steerX,steer15)
title('steer FIS Input MFs')
xlabel('Angle Deviation (deg)')
ylabel('Membership')
legend('NL','NS','ZE','PS','PL','Location','Best')
hold off

figure(2)
hold on
plot(steerX1,steer21)
plot(steerX1,steer22)
plot(steerX1,steer23)
plot(steerX1,steer24)
plot(steerX1,steer25)
title('steer FIS Output MFs')
xlabel('Steering Control (deg)')
ylabel('Membership')
legend('NL','NS','ZE','PS','PL','Location','Best')
hold off

%%
% fire Plots

fireX = linspace(-3, 3, 500);
fireX1 = linspace(0,10,500);
fire11 = trapmf(fireX, [-3, -3, -2, -1]);
fire12 = trimf(fireX, [-2, -1, 0]);
fire13 = trimf(fireX, [-0.25, 0, 0.25]);
fire14 = trimf(fireX, [0, 1, 2]);
fire15 = trapmf(fireX, [1, 2, 3, 3]);
fire21 = trimf(fireX1, [0, 1, 2]);
fire22 = trimf(fireX1, [8, 9, 10]);

figure(3)
hold on
plot(fireX,fire11)
plot(fireX,fire12)
plot(fireX,fire13)
plot(fireX,fire14)
plot(fireX,fire15)
title('fire FIS Input MFs')
xlabel('Angle Deviation (deg)')
ylabel('Membership')
legend('NL','NS','ZE','PS','PL','Location','Best')
hold off

figure(4)
hold on
plot(fireX1,fire21)
plot(fireX1,fire22)

title('fire FIS Output MFs')
xlabel('Fire Control')
ylabel('Membership')
legend('DN','FR','Location','Best')
hold off

%%
% Genes from GA
% Gene for training method 1
gene1raw = [9, 9, 2, 6, 4, 4, 26, 4, 2, 6, 3, 10, 23, 23, 31, 7, 28, 5, 21, 3, 24, 2, 8, 11,...
        22, 32, 5, 4, 2, 0, -4, -1, -5, -2, 0, 2, 4, 5, 10, 6, 9, 1, 4, 6, 2, 1, 2, 3,...
        2, 2, 2, 3, 3, 2, 1, 2, 3, 2, 3, 1, 2, 2, 1, 2, 2, 2, 3, 3, 1, 3, 2, 2,...
        2, 2, 1, 1, 2, 2, 1, 1, 1, 3, 3, 3, 1, 3, 1, 2, 2, 2, 3, 1, 2, 1];

gene1 = zeros(1,length(gene1raw));

% I have to conduct some operations on the values I get from GA
% The input MF values are multiplied by 32
% The output MF values are multipleid by 10
% The rules are left untouched.
 for i= 1:length(gene1raw)
     if i <= 26
         gene1(i) = gene1raw(i)*32;
     elseif i > 26 && i <= 44
         gene1(i) = gene1raw(i)*10;
     else
         gene1(i) = gene1raw(i);
     end
 end
WIDTH = 800;
Xin = linspace(0,WIDTH,500);
in11 = trapmf(Xin, sort([0, 0, gene1(1), gene1(2)]));
in12 = trimf(Xin, sort([gene1(3), gene1(4), gene1(5)]));
in13 = trimf(Xin, sort([gene1(6), gene1(7), gene1(8)]));
in14 = trimf(Xin, sort([gene1(9), gene1(10), gene1(11)]));
in15 = trapmf(Xin, sort([gene1(12), gene1(13), 800, 800]));

in21 = trapmf(Xin, sort([0, 0, gene1(14), gene1(15)]));
in22 = trimf(Xin, sort([gene1(16), gene1(17), gene1(18)]));
in23 = trimf(Xin, sort([gene1(19), gene1(20), gene1(21)]));
in24 = trimf(Xin, sort([gene1(22), gene1(23), gene1(24)]));
in25 = trapmf(Xin, sort([gene1(25), gene1(26), 800, 800]));

Xout1 = linspace(-50,50,500);
Xout2 = linspace(0,100,500);

out11 = trimf(Xout1, sort([gene1(27), gene1(28), gene1(29)]));
out12 = trimf(Xout1, sort([gene1(30), gene1(31), gene1(32)]));
out13 = trimf(Xout1, sort([gene1(33), gene1(34), gene1(35)]));

out21 = trimf(Xout2, sort([gene1(36), gene1(37), gene1(38)]));
out22 = trimf(Xout2, sort([gene1(39), gene1(40), gene1(41)]));
out23 = trimf(Xout2, sort([gene1(42), gene1(43), gene1(44)]));

figure(5)
hold on
plot(Xin,in11)
plot(Xin,in12)
plot(Xin,in13)
plot(Xin,in14)
plot(Xin,in15)
title('aim FIS X Input MFs Method 1')
xlabel('Position (pixels)')
ylabel('Membership')
legend('NL','NS','ZE','PS','PL','Location','East')
hold off


figure(6)
hold on
plot(Xin,in21)
plot(Xin,in22)
plot(Xin,in23)
plot(Xin,in24)
plot(Xin,in25)
title('aim FIS Y Input MFs: Method 1')
xlabel('Position (pixels)')
ylabel('Membership')
legend('NL','NS','ZE','PS','PL','Location','East')
hold off

figure(7)
hold on
plot(Xout1,out11)
plot(Xout1,out12)
plot(Xout1,out13)
title('aim FIS X Output MFs: Method 1')
xlabel('Aiming Value (pixels)')
ylabel('Membership')
legend('NS','ZE','PS','Location','East')
hold off

figure(8)
hold on
plot(Xout2,out11)
plot(Xout2,out12)
plot(Xout2,out13)
title('aim FIS Y Output MFs: Method 1')
xlabel('Aiming Value (pixels)')
ylabel('Membership')
legend('NS','ZE','PS','Location','East')
hold off

%%
% Gene for training method 2

gene2raw = [9,0,10,7,13,0,1,27,18,18,28,20,22,6,9,29,19,25,24,18,27,8,18,1,...
            4,0,0,-2,1,-3,-4,-5,-5,-5,2,1,6,4,1,4,8,9,7,10,1,2,2,3,...
            1,2,2,2,3,2,2,2,2,1,2,1,1,1,3,1,2,3,3,3,3,3,2,1,...
            1,1,3,1,3,3,2,2,1,1,1,2,2,3,1,1,1,2,1,3,1,3];
        
gene2 = zeros(1,length(gene2raw));

 for i= 1:length(gene2raw)
     if i <= 26
         gene2(i) = gene2raw(i)*32;
     elseif i > 26 && i <= 44
         gene2(i) = gene2raw(i)*10;
     else
         gene2(i) = gene2raw(i);
     end
 end
WIDTH = 800;
Xin = linspace(0,WIDTH,500);
in211 = trapmf(Xin, sort([0, 0, gene2(1), gene2(2)]));
in212 = trimf(Xin, sort([gene2(3), gene2(4), gene2(5)]));
in213 = trimf(Xin, sort([gene2(6), gene2(7), gene2(8)]));
in214 = trimf(Xin, sort([gene2(9), gene2(10), gene2(11)]));
in215 = trapmf(Xin, sort([gene2(12), gene2(13), 800, 800]));

in221 = trapmf(Xin, sort([0, 0, gene2(14), gene2(15)]));
in222 = trimf(Xin, sort([gene2(16), gene2(17), gene2(18)]));
in223 = trimf(Xin, sort([gene2(19), gene2(20), gene2(21)]));
in224 = trimf(Xin, sort([gene2(22), gene2(23), gene2(24)]));
in225 = trapmf(Xin, sort([gene2(25), gene2(26), 800, 800]));

Xout21 = linspace(-50,50,500);
Xout22 = linspace(0,100,500);

out211 = trimf(Xout21, sort([gene2(27), gene2(28), gene2(29)]));
out212 = trimf(Xout21, sort([gene2(30), gene2(31), gene2(32)]));
out213 = trimf(Xout21, sort([gene2(33), gene2(34), gene2(35)]));

out221 = trimf(Xout22, sort([gene2(36), gene2(37), gene2(38)]));
out222 = trimf(Xout22, sort([gene2(39), gene2(40), gene2(41)]));
out223 = trimf(Xout22, sort([gene2(42), gene2(43), gene2(44)]));

figure(9)
hold on
plot(Xin,in211)
plot(Xin,in212)
plot(Xin,in213)
plot(Xin,in214)
plot(Xin,in215)
title('aim FIS X Input MFs: Method 2')
xlabel('Position (pixels)')
ylabel('Membership')
legend('NL','NS','ZE','PS','PL','Location','East')
hold off


figure(10)
hold on
plot(Xin,in221)
plot(Xin,in222)
plot(Xin,in223)
plot(Xin,in224)
plot(Xin,in225)
title('aim FIS Y Input MFs: Method 2')
xlabel('Position (pixels)')
ylabel('Membership')
legend('NL','NS','ZE','PS','PL','Location','East')
hold off

figure(11)
hold on
plot(Xout21,out211)
plot(Xout21,out212)
plot(Xout21,out213)
title('aim FIS X Output MFs: Method 2')
xlabel('Aiming Value (pixels)')
ylabel('Membership')
legend('NS','ZE','PS','Location','East')
hold off

figure(12)
hold on
plot(Xout22,out211)
plot(Xout22,out212)
plot(Xout22,out213)
title('aim FIS Y Output MFs: Method 2')
xlabel('Aiming Value (pixels)')
ylabel('Membership')
legend('NS','ZE','PS','Location','East')
hold off

%%
% Ga Convergence

Xcon = linspace(1,70, 70);
Converge = load('convergance.mat');
Con1 = Converge.TablesS1.Con1;
Con2 = Converge.TablesS1.Con2;

figure(13)
plot(Xcon,Con1)
title('Convergance for Method 1')
xlabel('Generations')
ylabel('Fitness Value')

figure(14)
plot(Xcon,Con2)
title('Convergance for Method 2')
xlabel('Generations')
ylabel('Fitness Value')