PSoC NovelGame Player
written by Shunsei Takemura

【使用方法】
まず、Pythonアプリ(PSoC_NovelGamePlayer.py)を起動させるために、以下の操作を行ってください。
    1. Python (開発した環境は Python 3.12.4)をインストール
    2. pip をインストール(基本的に操作1.に内包されているはずです)
    3. 以下のコマンドを実行し、Pythonアプリを実行するために必要なライブラリをインストールしてください。
        pip install PySimpleGUI
        pip install Pyserial
        pip install pykakasi
        pip install jaconv
    4. これで、Pythonアプリを起動してみて、起動しなければ、1.～3.を見直してください！
次に、フォーマットからストーリーを作成してください！以下の注意点に留意してください。
    ・1行目は改変しないでください！データが正しく読み込めません!
    ・$selectで指定する行数の先に$コマンドを入れないでください！
    ・1列目(人物欄)に空文字を入れないでください。何も表示したくない場合は、" "(半角スペース)を入れてください！
これで操作は終わりです！お好みのノベルゲームを作って楽しんでください！

【FAQ】
PSoCのLCDに"!ERROR!"と出た場合は、Python側のエラーです。csvの書き込みルールに相違があるはずです。もう1度確認してください。
その他想定しないバグは、shunpc2018@outlook.jpに画像とともに送ってください。多分対応しません。(大学の実習で作っただけなので  )
