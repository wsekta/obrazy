close all; clear; clc;

SE = strel('line',20,90);

a = imread('im1.png');

a = imopen(a,SE);

subplot(121);imshow(a);

intervals = [[1 0 0; 
            1 0 1; 
            1 -1 0];
            
            [0 1 0;
             1 0 -1;
             0 1 0];
             ]


for j = 1:1000000
    for i = 1:2
        b=bwhitmiss(a,intervals(3*(i-1)+1:3*(i-1)+3,:));
        a=a+b;
    end
end
subplot(122);imshow(a);