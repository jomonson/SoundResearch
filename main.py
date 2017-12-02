import matplotlib.pyplot as pyplot
import numpy as np
import subprocess
import os.path as path
import sys
from scipy.io import wavfile
import time


def graph_spectrogram(wavFilePath, plotName):
    rate, data = getWavFileInfo(wavFilePath)
    monoData = data[:, 0]
    pxx, freqs, bins, im = pyplot.specgram(monoData, 4096, rate)
    chunkizedBins = list(chunks(bins, 200))
    times = [time.strftime("%M:%S", time.gmtime(x)) for x in chunkizedBins]
    pyplot.xticks(chunkizedBins, times)

    pyplot.savefig("{0}.png".format(plotName),
                dpi=1000,
                frameon='false',
                aspect='normal',
                bbox_inches='tight',
                pad_inches=0)
    pyplot.show()


def getWavFileInfo(wavFilePath):
    rate, data = wavfile.read(wavFilePath)
    return rate, data

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i]

if __name__ == '__main__':
    mp3FilePath = sys.argv[1]
    mp3FileName = mp3FilePath.split("\\")[-1].rsplit('.', 1)[0]
    wavFilePath = r"C:\dev\tools\WavFiles\{0}.wav".format(mp3FileName)
    if not path.isfile(wavFilePath):
        subprocess.check_output([r"C:\Dev\tools\FFmpeg\ffmpeg.exe", "-i", mp3FilePath, wavFilePath])
    graph_spectrogram(wavFilePath, mp3FileName)
