import matplotlib.pyplot as pyplot
import numpy as np
import subprocess
import os.path as path
import sys
from scipy.io import wavfile


def graph_spectrogram(wavFilePath, plotName):
    rate, data = getWavFileInfo(wavFilePath)
    # Length of the windowing segments
    # Sampling frequency
    monoData = data[:, 0]
    pxx, freqs, bins, im = pyplot.specgram(monoData, 4096, 256)
    pyplot.xlabel("Time (min)")
    pyplot.xticks(np.arange(min(bins), max(bins) + 1, 10000))

    pyplot.savefig("{0}.png".format(plotName),
                dpi=100,
                frameon='false',
                aspect='normal',
                bbox_inches='tight',
                pad_inches=0)
    pyplot.show()


def getWavFileInfo(wavFilePath):
    rate, data = wavfile.read(wavFilePath)
    return rate, data


if __name__ == '__main__':
    mp3FilePath = sys.argv[1]
    mp3FileName = mp3FilePath.split("\\")[-1].rsplit('.', 1)[0]
    wavFilePath = r"C:\dev\tools\WavFiles\{0}.wav".format(mp3FileName)
    if not path.isfile(wavFilePath):
        subprocess.check_output([r"C:\Dev\tools\FFmpeg\ffmpeg.exe", "-i", mp3FilePath, wavFilePath])
    graph_spectrogram(wavFilePath, mp3FileName)
