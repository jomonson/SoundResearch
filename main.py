import seaborn
import numpy, scipy, matplotlib.pyplot as plt, sklearn, IPython.display as ipd
import librosa, librosa.display
import subprocess
from dtw import dtw, fastdtw
from numpy.linalg import norm
from sklearn.metrics.pairwise import pairwise_distances
import os.path as path

def doStuff():
    plt.figure(figsize=(20, 80))
    offset = 40
    duration = 1
    x, sr = librosa.load(r'C:\Dev\tools\WavFiles\Kool & The Gang - Get Down On It.wav', offset=offset,duration=duration)
    print(x.shape)
    ipd.display(ipd.Audio(x, rate=sr))
    hop_length = 128
    n_fft = 4096
    D = librosa.stft(x, n_fft=n_fft, hop_length=hop_length)
    plt.subplot(3, 1, 1)
    librosa.display.specshow(librosa.amplitude_to_db(librosa.magphase(D)[0], ref=numpy.max), y_axis='log',x_axis='time')
    pitches, magnitudes = librosa.core.piptrack(y=x, sr=sr, S=D, threshold=0.1)
    plt.subplot(3, 1, 2)
    librosa.display.specshow(pitches, y_axis='linear', x_axis='time')
    print(pitches.shape)
    plt.subplot(3, 1, 3)
    librosa.display.specshow(magnitudes, y_axis='linear', x_axis='time')
    average_magnitudes = numpy.average(magnitudes, 1)
    max_avg_mag = numpy.int(max(average_magnitudes))
    step = 0.01
    bins = numpy.arange(0,0.5,step)
    hist, bin_edges = numpy.histogram(average_magnitudes, bins)
    plt.clf()
    plt.bar(bin_edges[:-1], hist, width=step)
    plt.xlim(min(bin_edges), max(bin_edges))
    mag_thresh = [index for index,val in average_magnitudes if val > 0.5]
    print(len(mag_thresh))
    plt.draw()
    plt.show()

    m = pairwise_distances(magnitudes, metric=dtw_metric)
    # agg = sklearn.cluster.AgglomerativeClustering(n_clusters=4, affinity='precomputed',linkage='average')
    # result = agg.fit_predict(distance_matrix)

def dtw_metric(x, y):
    x = x.reshape(-1,1)
    y = y.reshape(-1,1)
    dist, cost, acc, path = fastdtw(x, y, dist = lambda x, y: norm(x - y, ord=1))
    return dist

def convertMp3ToWav(mp3FilePath, wavFilePath = None):
    if(wavFilePath == None):
        mp3FileName = mp3FilePath.split("\\")[-1].rsplit('.', 1)[0]
        wavFilePath = r"C:\dev\tools\WavFiles\{0}.wav".format(mp3FileName)
    if not path.isfile(wavFilePath):
        subprocess.check_output([r"C:\Dev\tools\FFmpeg\ffmpeg.exe", "-i", mp3FilePath, wavFilePath])
    graph_spectrogram(wavFilePath, mp3FileName)

if __name__ == '__main__':
    doStuff();