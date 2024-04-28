import speech_recognition as sr
from aip import AipSpeech

# 请自己注册百度云语音识别：https://ai.baidu.com/tech/speech/asr
VOICE_APP_ID = 'YOUR_ASR_APP_ID'
VOICE_API_KEY = 'YOUR_ASR_APP_KEY'
VOICE_SECRET_KEY = 'YOUR_ASR_SECRET_KEY'
voice_client = AipSpeech(VOICE_APP_ID, VOICE_API_KEY, VOICE_SECRET_KEY)


# 百度云语音识别
def asr(audio_data):
    wav_data = audio_data.get_wav_data(
        convert_rate=16000,
        convert_width=2
    )
    res = voice_client.asr(wav_data, 'wav', 16000, {
        'dev_pid': 1737,
    })
    if res['err_no'] == 0:
        return ''.join(res['result'])
    else:
        return ''


def recognize_speech_from_mic(recognizer, microphone):
    '''
    麦克风录音并转文字 `microphone`.
    :param recognizer: 语音识别器
    :param microphone: 麦克风
    :return: `None` 如果识别失败返回None，否则返回语音文字
    '''
    print('开始朗读')
    # 录音并去除噪音
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # 使用百度云语音识别
    try:
        text = asr(audio)
    except Exception as e:
        print(e)
        text = None

    return text


if __name__ == '__main__':
    # 输入
    text = input('请输入一句英语: ').strip()

    # 创建语音识别器和麦克风
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # 录音并获取文字
    speech_text = recognize_speech_from_mic(recognizer, microphone)

    while speech_text != None and text.lower() != speech_text.lower():
        print('{} ×'.format(speech_text))
        speech_text = recognize_speech_from_mic(recognizer, microphone)

    if speech_text:
        print('{} {}'.format(speech_text, '✓'))
    else:
        print('语音识别服务暂不可用，请稍后再试。')
