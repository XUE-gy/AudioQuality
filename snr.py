import numpy as np
import soundfile as sf
import librosa

def numpy_SNR(clean_wav, noise_wav):
    # 原始语音
    origianl, sr0 = librosa.load(clean_wav , sr=32000)
    # 噪音
    target, sr1 = librosa.load(noise_wav , sr=32000)
    # origianl, sr0 = sf.read(clean_wav)  #数据，采样率
    # target, sr1 = sf.read(noise_wav)

    if abs(sr0 - sr1) > 10:
        print("ref_wav/deg_wav两个音频长度不一致: %d/%d" % (sr0, sr1))
        return False

    signal = np.sum(origianl ** 2)
    noise = np.sum(target ** 2)
    snr = 10 * np.log10(signal / noise)
    print(snr)
    return snr

# def tf_compute_snr(labels, logits):
#     # labels和logits都是三维数组 (batch_size, wav_data, 1)
#     signal = tf.reduce_mean(labels ** 2, axis=[1, 2])
#     noise = tf.reduce_mean((logits - labels) ** 2, axis=[1, 2])
#     noise = tf.reduce_mean((logits - labels) ** 2 + 1e-6, axis=[1, 2])
#     snr = 10 * tf.log(signal / noise) / tf.log(10.)
#     # snr = 10 * tf.log(signal / noise + 1e-8) / tf.log(10.)
#     snr = tf.reduce_mean(snr, axis=0)
#     return snr

def pcm2wav(pcm_file):
    """
    音频原始文件转wav
    :param pcm_file:
    :return:
    """
    import wave
    with open(pcm_file+'.pcm', 'rb') as pcmfile:
        pcmdata = pcmfile.read()

    with wave.open(pcm_file + '.wav', 'wb') as wavfile:
        # nchannels（声道数量）
        # sampwidth(采样位数, 跟Bit Depth一样)
        # framerate（采样率）
        # nframes（帧数）
        # comptype(压缩类型)
        # compname(压缩名)
        # wavfile.setparams((1, 2, 16000, 0, 'NONE', 'NONE'))
        wavfile.setnchannels(1)
        wavfile.setsampwidth(2)
        wavfile.setframerate(32000)
        wavfile.writeframes(pcmdata)

def make_SNR(clean_wav, noise_wav):
    # 原始语音
    a, a_sr = librosa.load(clean_wav+ '.wav', sr=32000)
    # 噪音
    b, b_sr = librosa.load(noise_wav+ '.wav', sr=32000)

    # 平方求和
    sum_s = np.sum(a ** 2)
    sum_n = np.sum(b ** 2)
    # 信噪比为20dB时的权重
    snr = 2
    x = np.sqrt(sum_s / (sum_n * pow(10, snr)))

    noise = x * b
    target = a + noise
    sf.write(clean_wav + "mix_SNR_2" + '.wav', target, 32000)
    sf.write(clean_wav + "clean_SNR_2" + '.wav', a, 32000)
    sf.write(clean_wav + "noise_SNR_2" + '.wav', noise, 32000)

    signal1 = np.sum(a ** 2)
    noise1 = np.sum((a - noise) ** 2)
    snr = 10 * np.log10(signal1 / noise1)
    print(snr)

if __name__ == '__main__':
    # 转换
    # pcm = "/Users/hopeworld/Documents/实验室/agc/SNR/wrl200"
    # pcm2wav(pcm)


    original = "D:\misc\snr\wrl1clean_SNR_2.wav"
    target = "D:\misc\snr\wrl1noise_SNR_2.wav"

    #make_SNR(,target)
    numpy_SNR(original, target)
    # snr = numpy_SNR(original,target)
    # print(snr)
