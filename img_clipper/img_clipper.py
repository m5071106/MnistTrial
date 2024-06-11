from pathlib import Path
from PIL import Image

import csv
import datetime
import os

# 指定された領域を切り取って保存する関数
def clip_image(top: int, left: int, height: int, width: int, input_file: str, output_file: str):
    image = Image.open(input_file)
    right = left + width
    bottom = top + height
    # 画像抽出
    clipped_image = image.crop((left, top, right, bottom))
    # 画像保存
    clipped_image.save(output_file)

def read_files():
    # 対象拡張子の読み込み
    with open('extensions.txt', 'r') as file:
        extensions = file.read().splitlines()

    # 入出力ディレクトリのパス
    source_dir = Path('./source.txt').read_text().strip()
    result_dir = Path('./result.txt').read_text().strip()
    backup_dir = './backup'

    # sourceディレクトリ内のファイル一覧を取得
    file_list = os.listdir(source_dir)

    # 認識対象の拡張子のファイルのみを抽出し、変換を行う
    for filename in file_list:
        if any(extension in filename for extension in extensions):
            # ファイル名から拡張子を除外
            converted_filename = filename
            for extension in extensions:
                converted_filename = converted_filename.replace('.' + extension, '')

            print(f'{converted_filename}の画像変換を開始')
            # 変換時刻を取得
            datetimenow = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

            # 読み込み用パラメタファイル
            with open('parameter.txt', 'r') as csvfile:
                reader = csv.reader(csvfile)
                index = 1
                for row in reader:
                    top, left, height, width = map(int, row[:4])
                    # 画像抽出関数呼び出し
                    clip_image(top, left, height, width, source_dir + "/" + filename, result_dir + "/" + converted_filename + '_' + f'{index:02}' + '.png')
                    index += 1

            # 処理したファイルをバックアップディレクトリに移動
            os.rename(f'{source_dir}/{filename}', f'{backup_dir}/{filename}')
            # バックアップディレクトリに移動したファイルに年月日時分秒をつけてリネーム
            os.rename(f'{backup_dir}/{filename}', f'{backup_dir}/{filename}.{datetimenow}')

if __name__ == '__main__':
    read_files()