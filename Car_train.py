import os
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision.transforms import ToTensor
from tqdm import tqdm
from PIL import Image

# 載入YOLOv5相關套件
from models import yolo
from utils.dataloaders import *
from utils.general import check_requirements, set_logging





# 設定相關參數
img_size = 640
Trainfolder_AC_Img_path="C:/Car_Data/AOLP/Subset_AC/Subset_AC/Image"
Trainfolder_AC_label_path="C:/Car_Data/AOLP/Subset_AC/Subset_AC/groundtruth_localization"
Trainfolder_AC_Imgtest_path="C:/Car_Data/AOLP/Subset_AC/Subset_AC/test_Image"
Trainfolder_AC_labeltest_path="C:/Car_Data/AOLP/Subset_AC/Subset_AC/test_Label"


Trainfolder_LE_Img_path="C:/Car_Data/AOLP/Subset_LE/Subset_LE/Subset_LE/Image"
Trainfolder_LE_label_path="C:/Car_Data/AOLP/Subset_LE/Subset_LE/Subset_LE/groundtruth_localization"
Trainfolder_LE_Imgtest_path="C:/Car_Data/AOLP/Subset_LE/Subset_LE/Subset_LE/test_Image"
Trainfolder_LE_labeltest_path="C:/Car_Data/AOLP/Subset_LE/Subset_LE/Subset_LE/test_Label"


Trainfolder_RP_Img_path="C:/Car_Data/AOLP/Subset_RP/Subset_RP/Subset_RP/Image"
Trainfolder_RP_label_path="C:/Car_Data/AOLP/Subset_RP/Subset_RP/Subset_RP/groundtruth_localization"
Trainfolder_RP_Imgtest_path="C:/Car_Data/AOLP/Subset_RP/Subset_RP/Subset_RP/test_Image"
Trainfolder_RP_labeltest_path="C:/Car_Data/AOLP/Subset_RP/Subset_RP/Subset_RP/test_Label"

# 驗證資料
test_Img_datasets = [Trainfolder_AC_Img_path,Trainfolder_LE_Img_path,Trainfolder_RP_Img_path]
test_Label_datasets=[Trainfolder_AC_label_path,Trainfolder_LE_label_path,Trainfolder_RP_label_path]
# 訓練資料
Img_datasets = [Trainfolder_AC_Imgtest_path,Trainfolder_LE_Imgtest_path,Trainfolder_RP_Imgtest_path]
Label_datasets=[Trainfolder_AC_labeltest_path,Trainfolder_LE_labeltest_path,Trainfolder_RP_labeltest_path]

weights_path="yolov5s.pt"
batch_size =8
epochs=10
# 資料集合併
datasets = []
# 驗證資料集合併
datasets_test=[]

# 檢查相關套件版本
check_requirements("gitpython")

# 訓練日誌
set_logging()

for data_dir, label_dir in zip(Img_datasets, Label_datasets):
    dataset = LoadImagesAndLabels(image_path=data_dir,label_path=label_dir, img_size=(416, 416), augment=True)
    datasets.append(dataset)
train_dataset=ConcatDataset(datasets)


for test_data_dir, test_label_dir in zip(test_Img_datasets, test_Label_datasets):
    dataset = LoadImagesAndLabels(image_path=test_data_dir,label_path=test_label_dir,img_size=(416, 416), augment=True)
    datasets.append(dataset)
test_datase=ConcatDataset(datasets)


# 建立訓練資料集
train_dataloader=DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
# 建立驗證資料集
test_dataloader=DataLoader(test_datase, batch_size=batch_size, shuffle=True)
# 設定YOLOv5模型
model=YOLOv5("yolov5s.yaml")
# 定義損失函數和優化器
criterion=tourch.nn.MSELoss()
optimizer=tourch.optim.Adam(model.parameters(), lr=0.001)

for epoch in range(epochs):
    mdoel.train()
    train_loss=0.0
    pbar=tqdm(train_dataloader,desc=f"Epoch {epoch+1}/{epochs}")
    for images, targets in pbar:
        # 將輸入和目標轉換為模型所需的張量形式
        images=images.to(model.device)
        targets=targets.to(model.device)
        
        # 正向傳播計算預測結果
        outputs=model(images)
        # 計算損失
        loss=criterion(outputs, targets)
         # 反向傳播和優化
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        train_loss+=loss.item()
train_loss/=len(train_dataloader)
print(f"Epoch {epoch+1}/{epochs}, Train Loss: {train_loss:.4f}")


model.eval()
val_loss=0.0
with torch.no_grad():
    for val_Image,val_targets in test_dataloader:
        val_Image=val_Imgae.to(model.device)
        val_targets=_targets.to(model.device)
        val_outputs=model(val_Image)
        val_loss+=criterion(val_outputs, val_targets).item()
val_loss /= len(val_dataloader)
# 在日誌中顯示驗證損失
print(f"Epoch {epoch+1}/{epochs}, Validation Loss: {val_loss:.4f}")
torch.save(model.state.dict(),'Car_Iden.pth')


















