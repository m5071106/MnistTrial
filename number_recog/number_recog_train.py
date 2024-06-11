# 事前準備
# pip install torch torchvision
# pip install pillow
# 初回はこちらを実行すること
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.datasets as datasets
import torchvision.transforms as transforms
import PIL.ImageOps    
import PIL.Image as pilimg

from Net import Net

# データの前処理
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

# MNISTデータセットの読み込み
train_dataset = datasets.MNIST(root='./data', train=True, transform=transform, download=True)
test_dataset = datasets.MNIST(root='./data', train=False, transform=transform)

# DataLoaderの作成 batch_size の値変更で学習を調整する 128, 64, 32 など
train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=64, shuffle=False)

# モデルのインスタンス化
model = Net()

# ハイパーパラメータの設定 学習率(0.01 や 0.1 などで調整)とエポック数(10, 20, 30などで調整)
learning_rate = 0.01
epochs = 30

# 損失関数と最適化アルゴリズムの定義
criterion = nn.CrossEntropyLoss()
# 最適化アルゴリズムの種類: Adam, SGD, Adagrad, RMSprop, Adadelta など
optimizer = optim.Adagrad(model.parameters(), lr=learning_rate)

# 学習ループ
for epoch in range(epochs):
    for batch_idx, (data, target) in enumerate(train_loader):
        # 入力データとラベルの取得
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()

    # 1エポックごとにテストデータでモデルを評価
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            output = model(data)
            test_loss += criterion(output, target).item()
            pred = output.argmax(dim=1, keepdim=True)
            correct += pred.eq(target.view_as(pred)).sum().item()

    test_loss /= len(test_loader.dataset)
    accuracy = 100. * correct / len(test_loader.dataset)
    print('Epoch: {} Test set: Average loss: {:.4f}, Accuracy: {}/{} ({:.2f}%)'.format(epoch, test_loss, correct, len(test_loader.dataset), accuracy))

# モデルのパラメータを保存
torch.save(model.state_dict(), 'models/model_weight.pth')
# モデル全体を保存
torch.save(model, 'models/model.pth')

# ここから文字認識のテスト
model = Net()
model.load_state_dict(torch.load('models/model_weight.pth'))

# 例：手書き数字の画像を読み込む
image = pilimg.open("sample/sample.png").convert('L')
image = PIL.ImageOps.invert(image)
transform = transforms.Compose([
    transforms.Resize((28, 28)),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])
image = transform(image).unsqueeze(0)

with torch.no_grad():
    output = model(image)
    # 出力の中で最大の値を持つインデックスを取得
    prediction = output.argmax(dim=1, keepdim=True)
    print("\nPrediction:", prediction.item())
