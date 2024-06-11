# 事前準備
# pip install pdf2image
# brew install poppler # Macの場合
# sudo apt install poppler-utils # Ubuntuの場合
from pathlib import Path
from pdf2image import convert_from_path

import datetime
import os

def convert_pdf():
    # 対象拡張子の読み込み
    with open('extensions.txt', 'r') as file:
        extensions = file.read().splitlines()

    # 入出力ディレクトリのパス
    source_dir = Path('./source.txt').read_text().strip()
    result_dir = Path('./result.txt').read_text().strip()
    backup_dir = './backup'
    poppler_path = '/opt/homebrew/opt/poppler/bin/' # Macの場合
    # poppler_path = '/usr/bin/' # Ubuntuの場合

    # sourceディレクトリ内のファイル一覧を取得
    file_list = os.listdir(source_dir)

    # 変換時刻を取得
    datetimenow = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    # 認識対象の拡張子のファイルのみを抽出し、変換を行う
    for filename in file_list:
        if any(extension in filename for extension in extensions):
            file_name_without_extension = os.path.splitext(filename)[0]
            images = convert_from_path(f'{source_dir}/{filename}', poppler_path=poppler_path, dpi=300)            
            for i, image in enumerate(images):
                # 1024より幅が大きい時、1024にリサイズ
                if image.width > 1024:
                    new_height = int((1024 / image.width) * image.height)
                    image = image.resize((1024, new_height))
                # 750より高さが大きい時、750にリサイズ
                if image.height > 750:
                    new_width = int((750 / image.height) * image.width)
                    image = image.resize((new_width, 750))
                image.save(f'{result_dir}/{file_name_without_extension}_{i}.png', "PNG")

            # 処理したファイルをバックアップディレクトリに移動
            os.rename(f'{source_dir}/{filename}', f'{backup_dir}/{filename}')
            # バックアップディレクトリに移動したファイルに年月日時分秒をつけてリネーム
            os.rename(f'{backup_dir}/{filename}', f'{backup_dir}/{filename}.{datetimenow}')


if __name__ == "__main__":
    convert_pdf()