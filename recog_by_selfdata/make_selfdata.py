from pathlib import Path
import shutil
import cv2

def make_train_data():
    '''
    過去に認識したデータを元に、学習データを作成する
    '''
    # 過去に認識したデータのディレクトリを取得
    srcimg_dir = Path('./img_dir.txt').read_text().strip()
    srclbl_dir = Path('./lbl_dir.txt').read_text().strip()
    srclbl_list = sorted(list(Path(srclbl_dir).glob('*')))
    srclbl_list = [file for file in srclbl_list if 'readme.txt' not in file.name]
    srcimg_list = sorted(list(Path(srcimg_dir).glob('*')))
    srcimg_list = [file for file in srcimg_list if 'readme.txt' not in file.name]

    # 学習データのディレクトリを取得
    target_dir = Path('./target.txt').read_text().strip()

    # 学習データのディレクトリを作成
    if not Path(target_dir).exists():
        Path(target_dir).mkdir(parents=True, exist_ok=True)

    # 学習データのディレクトリを初期化
    for i in range(10):
        if Path(target_dir + '/' + str(i)).exists():
            shutil.rmtree(target_dir + '/' + str(i))
        Path(target_dir + '/' + str(i)).mkdir(parents=True, exist_ok=True)

    # 学習データを過去に認識したデータから作成
    index = 0
    for lbl_file in srclbl_list:
        lbl_content = lbl_file.read_text()
        print(lbl_file, lbl_content, srcimg_list[index])
        shutil.copy(srcimg_list[index], target_dir + "/" + str(lbl_content) + "/" + srcimg_list[index].name)
        index += 1
        
    # ファイル名を連番に変更
    index1 = 0
    for i in range(10):
        temp_list = sorted(list(Path(target_dir + '/' + str(i)).glob('*')))
        temp_list = [file for file in temp_list if 'readme.txt' not in file.name]
        for file in temp_list:
            new_name = file.parent / (str(index1) + '.png')
            index1 += 1
            file.rename(new_name)
            img = cv2.imread(str(new_name), cv2.IMREAD_GRAYSCALE)
            # 28x28にリサイズ
            resized_img = cv2.resize(img, (28, 28))
            # 保存
            cv2.imwrite(str(new_name), resized_img)

    print('誤認識していたデータは該当する数字フォルダへ手で移動してください。')

if __name__ == '__main__':
    make_train_data()