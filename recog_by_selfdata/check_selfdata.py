# https://tanalib.com/pytorch-datasets/
from torch.utils.data import Dataset
from PIL import Image

import matplotlib.pyplot as plt
import os
import random

class MyDatasets(Dataset):
    def __init__(self, directory = None, transform = None):
        self.directory = directory
        self.transform = transform
        self.label, self.label_to_index = self._find_classes()
        self.img_path_and_label = self.create_img_path_and_label()

    def __len__(self):
        '''
        データセットのサイズを返す
        '''
        return len(self.img_path_and_label)
    
    def __getitem__(self, idx):
        '''
        機械学習用の画像とラベルを生成
        '''
        img_path, label = self.img_path_and_label[idx]
        # 学習用データ以外を除外するようif文を追加
        if '.DS_Store' in img_path:
            print("DS_Store is detected")
            return None
        else:
            img = Image.open(img_path)
            if self.transform:
                img = self.transform(img)
            return img, label

    def _find_classes(self):
        '''
        ディレクトリ名を画像に対するインデックスとして割り当てる
        '''
        classes = [d.name for d in os.scandir(self.directory)]
        classes.sort()
        class_to_idx = {class_name: i for i, class_name in enumerate(classes)}
        return classes, class_to_idx

    def create_img_path_and_label(self):
        '''
        画像のパスとラベルをリストに格納
        '''
        if self.directory:
            img_path_and_label_list = []
            directory = os.path.expanduser(self.directory)
            for target_label in sorted(self.label_to_index):
                label_index = self.label_to_index[target_label]
                target_dir = os.path.join(directory, target_label)

                for root, _, fnames in sorted(os.walk(target_dir, followlinks=True)):
                    for fname in sorted(fnames):
                        img_path = os.path.join(root, fname)
                        img_path_and_label = img_path, target_label
                        img_path_and_label_list.append(img_path_and_label)


            random.shuffle(img_path_and_label_list) 

        return img_path_and_label_list    
    
if __name__ == '__main__':
    dataset = MyDatasets(directory = './train_data')
    print("Call __len__ and get length of datasets: " + str(len(dataset)))
    temp = 0
    for i in dataset:
        # 画像の表示
        print("Call __getitem__ and get image and label: " + str(i))
        # try:
        #     img, label = i
        #     print(label)
        #     plt.imshow(img)
        #     plt.show()
        
        # except:
        #     print("Not image file")
        #     continue
        # temp += 1
        # # 確認のためだけなので5枚で終了
        # if temp >= 5:
        #     break
    
