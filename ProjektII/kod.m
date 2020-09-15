close all; clear; clc;

N =  imread('por_03_N_1N.jpg');
XN = imread('por_03_N_XN.jpg');

bin_N = N(:,:,1) > 60 & N(:,:,2) > 60 & N(:,:,3) > 60;
bin_XN = XN(:,:,1) < 20 & XN(:,:,2) < 20 & XN(:,:,3) < 20;

pory_bin = bin_N & bin_XN;

pory_bin = imfill(pory_bin, 'holes');
pory_bin = imclose(pory_bin, strel('disk', 5));
pory_bin = imfill(pory_bin, 'holes');
pory_bin = imopen(pory_bin, strel('disk', 11));
%pory_bin = imclose(pory_bin, strel('disk', 8));

pory_edge = imdilate(edge(pory_bin), ones(3));

XN_over = imoverlay(XN, pory_edge, 'blue');

%imshow(XN_over);
imshow(pory_bin)
pory_size = sum(pory_bin(:)) / 3690^2
%%
XN_300 = imread('por_03_300_XN.jpg');
XN_330 = imread('por_03_330_XN.jpg');
XN_300 = imrotate(XN_300, 60, 'crop');
XN_330 = imrotate(XN_330, 30, 'crop');

XN = XN .* uint8(~pory_bin);
XN_300 = XN_300 .* uint8(~pory_bin);
XN_330 = XN_330 .* uint8(~pory_bin);

kwarc1_bin = XN(:,:,3) > (0.99 * XN(:,:,2)) & XN(:,:,2) >  (0.99*XN(:,:,1));
kwarc2_bin = XN_300(:,:,3) > (0.99 *XN_300(:,:,2)) & XN_300(:,:,2) > (0.99 *XN_300(:,:,1));
kwarc3_bin = XN_330(:,:,3) > (0.99 *XN_330(:,:,2)) & XN_330(:,:,2) > (0.99 *XN_330(:,:,1));

kwarc1_bin = imclose(kwarc1_bin, strel('disk', 4));
%subplot(131);imshow(kwarc1_bin);
kwarc2_bin = imclose(kwarc2_bin, strel('disk', 4));
%subplot(132);imshow(kwarc2_bin);
kwarc3_bin = imclose(kwarc3_bin, strel('disk', 4));
%subplot(133);imshow(kwarc3_bin);

kwarc_bin = kwarc1_bin | kwarc2_bin | kwarc3_bin;
kwarc_bin = imerode(kwarc_bin, strel('disk', 3));
kwarc_bin = imfill(kwarc_bin, 'holes');
kwarc_bin = imopen(kwarc_bin, strel('square', 10));

%imshow(kwarc_bin)
kwarc_size = sum(kwarc_bin(:)) / 3690^2

kwarc_edge = imdilate(edge(kwarc_bin), ones(3));

XN_over = imoverlay(XN_over, kwarc_edge, 'red');
%imshow(XN_over)
imshow(XN_over)