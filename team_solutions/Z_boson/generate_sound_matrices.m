%% Generate a random sound matrix

freqs = [220.00 246.94 261.63 293.66 329.63 349.23 392.00]*(2^(1/12))^4;
amplitudes = randi(10, 10, 7);
for i = 1:10
    for j = 1:7
        amplitudes(i, j) = amplitudes(i, j)*(amplitudes(i, j) > 7);
    end
end
amplitudes = amplitudes/10;
%% Convert the matrix to a sound file

n_durations = height(amplitudes);
n_notes = width(amplitudes);
durations = 0.4; % [s]
Fs = 48000; % sampling rate [Hz]
t=0:1/Fs:1;
x = [];
for dur_num = 1:n_durations
 time = 0:1/Fs:durations;
 waveform = zeros(size(time));
 for note_num = 1:n_notes
  waveform = waveform ...
      + amplitudes(dur_num,note_num)*sin(2*pi*freqs(note_num)*time);
 end
 x = [x waveform];
end
soundsc(x, Fs);
audiowrite('AB1.0.mp4', x, Fs);
writematrix(amplitudes, 'AB1.0.csv');
