#GUI
import PySimpleGUI as sg
#シリアル通信
import serial
import serial.tools
import serial.tools.list_ports
#日本語文字列→半角カタカナ変換
from pykakasi import kakasi
import jaconv
#wavファイル解析
import csv

#ストーリー格納用
story = [['',''],['','']]
current = 0
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
layout = [[sg.Text("PSoC NobelGame Player")],
          [sg.Text("CSV File: "),sg.Input(key='Input',size=65),sg.FileBrowse("参照",key='src',file_types=(('CSV Files','.csv'),),enable_events=True)],
          [sg.Text("シリアルポート名"),sg.Combo(values=[''],key='Serial_name',size=56),sg.Button("更新",key='Update_Serial')],
          [sg.Button("データ読込",key='Submit')],
          [sg.Text('シリアルポート名：'),sg.Text('',key='Serial_display')],
          [sg.Text('')],
          [sg.Text('選択ボタン')],
          [sg.Button('Selection1',key='sele_1'),sg.Button('Selection2',key='sele_2'),sg.Button('次へ',key='next')]]

#レイアウト等のウィンドウ設定
window = sg.Window('PSoC NovelGame Player', layout, finalize=True, return_keyboard_events=True)

#シリアルに特定の文字列を送信
def writeSerial(command = ''):
    #終了記号追加
    command += '\r\n'
    #シリアルが選択されていれば、コマンド送信
    if values['Serial_name'] != '':
        writeSer = serial.Serial(port=values['Serial_name'],baudrate=38400,bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
        writeSer.write(bytes(command,'ascii'))
        writeSer.close()

#ひらがな→カタカナ変換
def nameConv(name = ''):
    #Pykakasiのインスタンス作成
    kks = kakasi()
    #漢字→ひらがな変換の表を作成
    done_conv = kks.convert(name)
    #結果に表からひらがなのみを取り出し、半角カタカナに変換して格納
    result = ''
    for word in done_conv:
        result += f"{word['hira']}"
    result = jaconv.hira2hkata(result)
    return result

#16進数→文字列変換
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
#タイトルをシリアル通信で送り込む
def submit(text = '',column = 0):
    #内容を半角カタカナ変換
    text = nameConv(text)
    #$Wコマンドと、書き込む行数をコマンドにする。
    result = '$W' + str(column)
    #文字列が溢れないように
    index = 0
    #文字列を実際に送る16進数に変換する
    for s in text:
        num = ord(s)
        if index >= 16:
            break
        if num > 255:
            if s in hanASCii_data.keys():
                num = hanASCii_data[s]
            else:
                num = 42
        result += conv16(int((num % 256) / 16))
        result += conv16(int(num % 16))
        index += 1
    #終了記号追加
    result += '$'
    #シリアルに書き込む
    writeSerial(result)
#ポートリストを取得,反映
def UpdateSerial():
    port_list = list(serial.tools.list_ports.comports())
    result_list = ['']
    for port in port_list:
        result_list += [port.device]
    window['Serial_name'].Update(values=result_list,size=56)
#ストーリー読み込み
def ReadStory(path=''):
    l = [['',''],['','']]
    #ストーリー読み込み
    if path != '':
        with open(path,encoding='utf-8') as f:
            reader = csv.reader(f)
            l = [row for row in reader]
    #シリアルポート設定を反映
    if values['Serial_name'] == '':
        window['Serial_display'].update('シリアルポートが選択されていません')
    else :
        window['Serial_display'].update(values['Serial_name'])
    return l
#ストーリー進行
def next_story(index=0):
    #Storyが正常に読み込めていないとき
    if story[0][0] in 'human':
        ERROR()
        return 0
    #現在位置がコマンドであるかどうか
    if story[index][0][0] != '$':
        #コマンドでなければ次に進む
        index += 1
        submit(story[index][0],0)
        submit(story[index][1],1)
    else:
        #コマンドであれば、次に進まない
        return index
    if story[index][0][0] != '$':
        #次に進んだ場合,そのまま今の位置を返す
        return index
    elif story[index][0] in '$select':
        #$selectコマンド用の書き込み
        WriteSelect(story[index][1],story[index][2],story[index][4])
        return index
    elif story[index][0] in '$end':
        #終了用の書き込み
        WriteEnd(story[index][1])
        return index
    #どれにも当てはまらない場合⇔エラー処理
    ERROR()
    return -1
#$selectコマンド書き込み
def WriteSelect(text='',sel1='',sel2=''):
    submit(text,0)
    col1_text = '1:' + sel1 + ' 2:' + sel2
    submit(col1_text,1)
#$endコマンド書き込み
def WriteEnd(text=''):
    submit(text,0)
    submit('',1)
#ERROR書き込み
def ERROR():
    submit('!ERROR!',0)
    submit('!ERROR!',1)
#select
def Select(index = 0, selection_num = 0):
    #selectコマンドでなければ、操作不能
    if not (story[index][0] in '$select'):
        return index
    jump = 0
    #Selection1の場合
    if selection_num == 1:
        jump = int(story[index][3]) - 1
    #Selection2の場合
    elif selection_num == 2:
        jump = int(story[index][5]) - 1
    #jump先に想定外の値がきた場合⇔エラー処理
    if jump > len(story) or jump == 0:
        ERROR()
        return -1
    #jump先がコマンドであった場合⇔エラー処理
    if story[jump][0] in '$':
        ERROR()
        return -1
    #jump先に飛ぶ
    submit(story[jump][1],1)
    submit(story[jump][0],0)
    return jump 
#GUIメイン関数
while True:
    event, values = window.read()
    # window close
    if event == sg.WIN_CLOSED:
        break
    #ストーリー、シリアルポート読み込み
    if event == 'Submit':
        story = ReadStory(values['src'])
        current = next_story(0)
    #現在のシリアルポート一覧をアップデートする
    if event == 'Update_Serial':
        UpdateSerial()
    #Selection1ボタンが押された
    if event == 'sele_1':
        current = Select(current,1)
    #Selection2ボタンが押された
    if event == 'sele_2':
        current = Select(current,2)
    #次へボタンが押された
    if event == 'next':
        current = next_story(current)
#ウィンドウを閉じる
window.close()