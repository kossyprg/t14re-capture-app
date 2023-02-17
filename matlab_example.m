clear variables;
close all;
clc;

%% basic parameters
c = 3*1e8;
f = 79*1e9;
lmd = c/f;    % wave length
d0 = lmd/2;   % element spacing
B = 3.6*1e9;  % bandwidth
dr = c/(2*B); % range resolution
NTx = 3;
NRx = 4;

%%
folderName = 'data_t14re\2023-02-16-17-15-10-300604_t14re';
matFiles = [folderName,'\*.mat'];
fileInfo = dir(matFiles);
fileNum = size(fileInfo,1);

N_rfft = 1024;
N_afft = 1024;
FS = 16;

figure(1);
for I=1:fileNum
    clf(1);
    fprintf('%d/%d\n',I,fileNum);
    filepath = [folderName,'\',fileInfo(I).name];
    load(filepath);
    if I==1
        [FramesPerData,ChirpsetsPerFrame,N,numAdcSamples] = size(signals);
        dr_pad = dr*numAdcSamples/N_rfft;
        range = (0:1:N_rfft-1)*dr_pad;
        theta = asin(lmd*(-N_afft/2:N_afft/2-1)./(N_afft*d0));
        [Range,Theta] = meshgrid(range,theta);
        X = Range.*sin(Theta);
        Y = Range.*cos(Theta);
    end
    S = squeeze(mean(signals,2)); % coherent integration
    S = fft(S,N_rfft,3);
    S = fftshift(fft(S,N_afft,2),2);
    S = squeeze(mean(S,1));
    Z = 20*log10(abs(S));
    
    surface(X,Y,Z,'EdgeColor','none');
    xlabel('x (m)');
    ylabel('y (m)');
    cb = colorbar;
    cb.Label.String = 'Intensity (dB)';
    xlim([-3,3]);
    ylim([0,3]);
    caxis([-50,0]+max(max(Z)));
    set(gca,'fontsize',FS);
    drawnow;
end