from pathlib import Path
from PIL import Image

import csv
import datetime
import os
import sqlite3

def insert_records():
    # 入出力ディレクトリのパス
    source_dir = Path('./source.txt').read_text().strip()
    backup_dir = './backup'

    # sourceディレクトリ内のファイル一覧を取得
    file_list = sorted(os.listdir(source_dir))

    # 作業記録のための変数を初期化
    employee_code = ''
    rec1_starttime = ''
    rec1_endtime = ''
    rec1_workcode = ''
    rec2_starttime = ''
    rec2_endtime = ''
    rec2_workcode = ''
    rec3_starttime = ''
    rec3_endtime = ''
    rec3_workcode = ''
    rec4_starttime = ''
    rec4_endtime = ''
    rec4_workcode = ''
    rec5_starttime = ''
    rec5_endtime = ''
    rec5_workcode = ''

    # 登録形式に変換
    dataarray = []
    for filename in file_list:
        # ファイルを開く
        with open(f'{source_dir}/{filename}', 'r', encoding='utf-8') as f:
            # ファイルを読み込む
            reader = csv.reader(f)
            for row in reader:
                dataarray.append(row)

    employee_code = dataarray[0]+dataarray[1]+dataarray[2]+dataarray[3]
    employee_code = ''.join(employee_code)

    rec1_starttime = dataarray[4]+dataarray[5]+dataarray[6]+dataarray[7]
    rec1_starttime = ''.join(rec1_starttime)
    rec1_endtime = dataarray[8]+dataarray[9]+dataarray[10]+dataarray[11]
    rec1_endtime = ''.join(rec1_endtime)
    rec1_workcode = dataarray[12]
    rec1_workcode = ''.join(rec1_workcode)

    if len(dataarray) > 13:
        rec2_starttime = dataarray[13]+dataarray[14]+dataarray[15]+dataarray[16]
        rec2_starttime = ''.join(rec2_starttime)
        rec2_endtime = dataarray[17]+dataarray[18]+dataarray[19]+dataarray[20]
        rec2_endtime = ''.join(rec2_endtime)
        rec2_workcode = dataarray[21]
        rec2_workcode = ''.join(rec2_workcode)
    if len(dataarray) > 22:
        rec3_starttime = dataarray[22]+dataarray[23]+dataarray[24]+dataarray[25]
        rec3_starttime = ''.join(rec3_starttime)
        rec3_endtime = dataarray[26]+dataarray[27]+dataarray[28]+dataarray[29]
        rec3_endtime = ''.join(rec3_endtime)
        rec3_workcode = dataarray[30]
        rec3_workcode = ''.join(rec3_workcode)
    if len(dataarray) > 31:
        rec4_starttime = dataarray[31]+dataarray[32]+dataarray[33]+dataarray[34]
        rec4_starttime = ''.join(rec4_starttime)
        rec4_endtime = dataarray[35]+dataarray[36]+dataarray[37]+dataarray[38]
        rec4_endtime = ''.join(rec4_endtime)
        rec4_workcode = dataarray[39]
        rec4_workcode = ''.join(rec4_workcode)
    if len(dataarray) > 40:
        rec5_starttime = dataarray[40]+dataarray[41]+dataarray[42]+dataarray[43]
        rec5_starttime = ''.join(rec5_starttime)
        rec5_endtime = dataarray[44]+dataarray[45]+dataarray[46]+dataarray[47]
        rec5_endtime = ''.join(rec5_endtime)
        rec5_workcode = dataarray[48]
        rec5_workcode = ''.join(rec5_workcode)

    # データベースに接続
    conn = sqlite3.connect('sample.db')
    c = conn.cursor()

    # 作業記録のテーブルが存在するか確認
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='work_record'")
    table_exists = c.fetchone()
    if not table_exists:
        c.execute('''CREATE TABLE work_record (
                        employee_code TEXT,
                        rec1_starttime TEXT,
                        rec1_endtime TEXT,
                        rec1_workcode TEXT,
                        rec2_starttime TEXT,
                        rec2_endtime TEXT,
                        rec2_workcode TEXT,
                        rec3_starttime TEXT,
                        rec3_endtime TEXT,
                        rec3_workcode TEXT,
                        rec4_starttime TEXT,
                        rec4_endtime TEXT,
                        rec4_workcode TEXT,
                        rec5_starttime TEXT,
                        rec5_endtime TEXT,
                        rec5_workcode TEXT
                    )''')

    # 作業記録を登録
    c.execute('''INSERT INTO work_record (
                    employee_code,
                    rec1_starttime,
                    rec1_endtime,
                    rec1_workcode,
                    rec2_starttime,
                    rec2_endtime,
                    rec2_workcode,
                    rec3_starttime,
                    rec3_endtime,
                    rec3_workcode,
                    rec4_starttime,
                    rec4_endtime,
                    rec4_workcode,
                    rec5_starttime,
                    rec5_endtime,
                    rec5_workcode
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (employee_code,
                 rec1_starttime,
                 rec1_endtime,
                 rec1_workcode,
                 rec2_starttime,
                 rec2_endtime,
                 rec2_workcode,
                 rec3_starttime,
                 rec3_endtime,
                 rec3_workcode,
                 rec4_starttime,
                 rec4_endtime,
                 rec4_workcode,
                 rec5_starttime,
                 rec5_endtime,
                 rec5_workcode))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    
    # sourceディレクトリ内のファイルをbackupディレクトリに移動
    for filename in file_list:
        # 登録時刻を取得
        datetimenow = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        # 処理したファイルをバックアップディレクトリに移動
        os.rename(f'{source_dir}/{filename}', f'{backup_dir}/{filename}')
        # バックアップディレクトリに移動したファイルに年月日時分秒をつけてリネーム
        os.rename(f'{backup_dir}/{filename}', f'{backup_dir}/{filename}.{datetimenow}')


if __name__ == '__main__':
    insert_records()