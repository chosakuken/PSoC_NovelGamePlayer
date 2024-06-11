#GUI
import PySimpleGUI as sg
#シリアル通信
import serial
import serial.tools
import serial.tools.list_ports
#ファイル名→半角カタカナ変換
from pykakasi import kakasi
import os
import jaconv
#wavファイル解析
import numpy as np
import sys
import wave
from pydub import AudioSegment
import time
from datetime import datetime
#map&test
import matplotlib.pyplot as plt
import pyaudio

#wavの配列
wav_array = np.arange(0,0)
wav_dac = np.arange(0,0)
wav_python = np.arange(0,0)
freq = 0
divider = 16
#半角カタカナ→ASCIIの変換用辞書
hanASCii_data = {
    '｡':161,
    '｢':162,
    '｣':163,
    '､':164,
    '･':165,
    'ｦ':166,
    'ｧ':167,
    'ｨ':168,
    'ｩ':169,
    'ｪ':170,
    'ｫ':171,
    'ｬ':172,
    'ｭ':173,
    'ｮ':174,
    'ｯ':175,
    'ｰ':176,
    'ｱ':177,
    'ｲ':178,
    'ｳ':179,
    'ｴ':180,
    'ｵ':181,
    'ｶ':182,
    'ｷ':183,
    'ｸ':184,
    'ｹ':185,
    'ｺ':186,
    'ｻ':187,
    'ｼ':188,
    'ｽ':189,
    'ｾ':190,
    'ｿ':191,
    'ﾀ':192,
    'ﾁ':193,
    'ﾂ':194,
    'ﾃ':195,
    'ﾄ':196,
    'ﾅ':197,
    'ﾆ':198,
    'ﾇ':199,
    'ﾈ':200,
    'ﾉ':201,
    'ﾊ':202,
    'ﾋ':203,
    'ﾌ':204,
    'ﾍ':205,
    'ﾎ':206,
    'ﾏ':207,
    'ﾐ':208,
    'ﾑ':209,
    'ﾒ':210,
    'ﾓ':211,
    'ﾔ':212,
    'ﾕ':213,
    'ﾖ':214,
    'ﾗ':215,
    'ﾘ':216,
    'ﾙ':217,
    'ﾚ':218,
    'ﾛ':219,
    'ﾜ':220,
    'ﾝ':221,
    'ﾞ':222,
    'ﾟ':223
}
#pySimpleGUIの設定
#レイアウト設定
layout = [[sg.Text("PSoC Music Player")],
          [sg.Text("WAV File: "),sg.Input(key='Input',size=65),sg.FileBrowse("参照",key='Music_src',file_types=("Wav Files",".wav"),enable_events=True)],
          [sg.Text("シリアルポート名"),sg.Combo(values=[''],key='Serial_name',size=56),sg.Button("更新",key='Update_Serial')],
          [sg.Button("音源読込",key='Submit_Music')],
          [sg.Text('　　　　　　音源：'),sg.Text('',key='Music_display')],
          [sg.Text('　　　　　音源名：'),sg.Input('',key='title')],
          [sg.Text('　　　　　　　　　　※一部記号は文字化けの危険性あり！')],
          [sg.Text('シリアルポート名：'),sg.Text('',key='Serial_display')],
          [sg.Button('再生',key='Start_Serial'),sg.Button('停止',key='Stop_Serial')],
          [sg.Text('',key='NumpyNum')]]

#レイアウト等のウィンドウ設定
window = sg.Window('App', layout, finalize=True, return_keyboard_events=True)

#シリアルに特定の文字列を送信
def writeSerial(command = ''):
    command += '\r\n'
    if values['Serial_name'] != '':
        writeSer = serial.Serial(port=values['Serial_name'],baudrate=38400,bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
        writeSer.write(bytes(command,'ascii'))
        writeSer.close()

#音源名をひらがなに変換
def nameConv(name = ''):
    kks = kakasi()
    done_conv = kks.convert(name)
    result = ''
    for word in done_conv:
        result += f"{word['hira']}"
    result = jaconv.hira2hkata(result)
    return result

#16進数変換
def conv16(num = 0):
    if num == 0:
        return '0'
    if num == 1:
        return '1'
    if num == 2:
        return '2'
    if num == 3:
        return '3'
    if num == 4:
        return '4'
    if num == 5:
        return '5'
    if num == 6:
        return '6'
    if num == 7:
        return '7'
    if num == 8:
        return '8'
    if num == 9:
        return '9'
    if num == 10:
        return 'A'
    if num == 11:
        return 'B'
    if num == 12:
        return 'C'
    if num == 13:
        return 'D'
    if num == 14:
        return 'E'
    if num == 15:
        return 'F'
    #　エラー(想定以外の値が入力)
    return 'N'

#ファイル、ポート名読み込み
def readInput():
    # wavファイルが選択されていたら、ファイルを読み込む
    if values['Input'] != '':
        sounds = AudioSegment.from_file(values['Input'],'wave')
        sig = np.array(sounds.get_array_of_samples())
        wav_array = sig
    title = os.path.basename(values['Input'])
    window['Music_display'].update(title)
    window['title'].update(os.path.splitext(title)[0])
    window['Serial_display'].update(values['Serial_name'])
    print(wav_array)
    return wav_array
#サンプリング周波数読込
def readFreq():
    sample_freq = 0
    # wavファイルが選択されていたら、ファイルを読み込む
    if values['Input'] != '':
        sounds = AudioSegment.from_file(values['Input'],'wave')
        sample_freq = sounds.frame_rate
        print(sounds.frame_rate,sounds.duration_seconds)
    return sample_freq
#タイトルをシリアル通信で送り込む
def submitTitle(title = ''):
    result = '$I'
    for s in title:
        num = ord(s)
        if num > 255:
            if s in hanASCii_data.keys():
                num = hanASCii_data[s]
            else:
                num = 42
        result += conv16(int((num % 256) / 16))
        result += conv16(int(num % 16))
    result += '$'
    print(result)
    writeSerial(result)
#正規化
def min_max_normalization(a=np.arange(0,0), axis=None):
    a_min = a.min(axis=axis, keepdims=True)
    a_max = a.max(axis=axis, keepdims=True)
    print(a_max, a_min,a_max-a_min)
    return 256 * (a - a_min) / (a_max - a_min)
#wav解析
def wavAnalysis(data = np.arange(0,0)):
    for i in range(divider - (data.size % divider)):
        data = np.append(data,[0])
    data = data.reshape(int(data.size / divider), divider)
    data = data.transpose()
    wav_analysis = min_max_normalization(data[0])
    print(wav_analysis)
    return wav_analysis
#ポートリストを取得
def UpdateSerial():
    port_list = list(serial.tools.list_ports.comports())
    result_list = ['']
    for port in port_list:
        result_list += [port.device]
    window['Serial_name'].Update(values=result_list,size=56)
#音楽再生
def MusicPlay(data = np.arange(0,0),freq = 0):
    dt = divider / freq
    t = np.arange(0,data.size)
    print(data.size)
    plt.plot(t,data,label="data")
    plt.xlabel("t")
    plt.ylabel("y")
    plt.title('graph')
    plt.legend()
    plt.show()
    start_time = datetime.now()
    for i in range(data.size):
        node = data[i]
        #print(conv16(int(node/16))+conv16(int(node%16)))
        writeSerial(conv16(int((node%256)/16))+conv16(int(node%16)))
        time.sleep(dt)
    print((datetime.now() - start_time))
#GUIメイン関数
while True:
    event, values = window.read()
    # window close
    if event == sg.WIN_CLOSED:
        break
    #Config Inport
    if event == 'Submit_Music':
        wav_array = readInput()
        freq = readFreq()
        wav_dac = wavAnalysis(wav_array)
    #Serial Submit
    if event == 'Start_Serial':
        submitTitle(nameConv(values['title']))
        MusicPlay(wav_dac,freq=freq)
    if event == 'Update_Serial':
        UpdateSerial()
    if event == 'Stop_Serial':
        print('hoge')
#ウィンドウを閉じる
window.close()