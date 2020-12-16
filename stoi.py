def get_stoi(ref_wav, deg_wav):
    """
    计算语音的STOI值，范围0～1，值越大，可懂度越高.
    注意：两个音频长度一致，且需要是单声道
    :param ref_wav:
    :param deg_wav:
    :return:
    """
    import soundfile as sf
    from pystoi import stoi

    clean, fs = sf.read(ref_wav)
    denoised, fs = sf.read(deg_wav)

    # 检查是否为单声道
    import wave
    with wave.open(ref_wav, 'rb') as reg_wav_obj:
        reg_wav_channels = reg_wav_obj.getnchannels()
        if reg_wav_channels > 1:
            print("音频不是单声道，声道数为：%d，音频: %s" % (reg_wav_channels, ref_wav))
            return False

    with wave.open(deg_wav, 'rb') as deg_wav_obj:
        deg_wav_channels = deg_wav_obj.getnchannels()
        if deg_wav_channels > 1:
            print("音频不是单声道，声道数为：%d，音频: %s" % (deg_wav_channels, deg_wav))
            return False

    # 检查两个音频文件长度，帧数相差不大于10
    if abs(len(clean) - len(denoised)) > 10:
        print("ref_wav/deg_wav两个音频长度不一致: %d/%d" % (len(clean), len(denoised)))
        return False

    # Clean and den should have the same length, and be 1D
    d = stoi(clean, denoised, fs, extended=False)

    print(d)

def main():
    get_stoi("D:\misc\wav\selfAudioDatexsr1.wav","D:\misc\wav\selfAudioDateNxsr1.wav")

if __name__ == '__main__':
    main()