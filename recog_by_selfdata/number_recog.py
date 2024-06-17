# 事前準備
# pip install torch torchvision
# pip install pillow
# python3 mnist_sample_with_train.py を行なって model_weight.pth および model.pth を作成しておくこと
import cv2
import datetime
import os
import PIL.ImageOps    
import PIL.Image as pilimg
import torch
import torch.nn as nn
import torchvision.datasets as datasets
import torchvision.transforms as transforms

from pathlib import Path

from Net import Net

# データの前処理
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

# モデル読込
model = Net()
model.load_state_dict(torch.load('models/model_weight.pth'))

def predict_number():

    # 変数の初期化
    resultfilename = None
    result = None

    # 対象拡張子の読み込み
    with open('extensions.txt', 'r') as file:
        extensions = file.read().splitlines()

    # 入出力ディレクトリのパス
    source_dir = Path('./source.txt').read_text().strip()
    result_dir = Path('./result.txt').read_text().strip()
    backup_dir = './backup'
    temporary_dir = './temporary'
    # sourceディレクトリ内のファイル一覧を取得
    file_list = os.listdir(source_dir)

    # tempoary_dir 内のファイルを削除
    for filename in os.listdir(temporary_dir):
        os.remove(f'{temporary_dir}/{filename}')

    # 認識対象の拡張子のファイルのみを抽出し、変換を行う
    for filename in file_list:
        if any(extension in filename for extension in extensions):
            print(f'{filename}の画像変換を開始')
            # 変換時刻を取得
            datetimenow = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            # 変換後のファイル名を作成
            converted_filename = filename
            for extension in extensions:
                converted_filename = converted_filename.replace('.' + extension, '')
            # 変換後のファイル名
            resultfilename = f'{converted_filename}.txt'
            # 入力
            img = cv2.imread(source_dir + "/" + filename)
            # グレースケール
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # 2値化
            threshold = 140
            img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)[1]
            # 画像の短い方の辺の長さを取得
            shortest_side = min(img.shape[0], img.shape[1])
            # 正方形に変換
            img = cv2.resize(img, (shortest_side, shortest_side))
            # 一時フォルダへ書き出し
            cv2.imwrite(temporary_dir + "/" + filename, img)

            # 画像読込
            image = pilimg.open(temporary_dir + "/" + filename).convert('L')
            image = PIL.ImageOps.invert(image)
            transform = transforms.Compose([
                transforms.Resize((28, 28)),
                transforms.ToTensor(),
                transforms.Normalize((0.5,), (0.5,))
            ])
            image = transform(image).unsqueeze(0)
            # 数字予測結果
            with torch.no_grad():
                output = model(image)
                prediction = output.argmax(dim=1, keepdim=True)
                result = prediction.item()

            # 処理したファイルをバックアップディレクトリに移動
            os.rename(f'{source_dir}/{filename}', f'{backup_dir}/{filename}')
            # バックアップディレクトリに移動したファイルに年月日時分秒をつけてリネーム
            os.rename(f'{backup_dir}/{filename}', f'{backup_dir}/{filename}.{datetimenow}')
            # resultフォルダ内にファイルを作成し、結果を書き込む
            with open(f'{result_dir}/{resultfilename}', mode='w+') as f:
                f.write(str(result))

    # tempoary_dir 内のファイルを削除
    for filename in os.listdir(temporary_dir):
        os.remove(f'{temporary_dir}/{filename}')
    return resultfilename, result

if __name__ == '__main__':
    resultfilename, result = predict_number()
    print(resultfilename, result)