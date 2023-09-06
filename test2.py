import os
import xml.etree.ElementTree as ET

# 設定輸入和輸出資料夾路徑
input_folder = "C:\\Users\\loveaoe33\\Desktop\\train"  # 輸入的資料夾
output_folder = "C:\\Users\\loveaoe33\\Desktop\\train"  # 輸出的資料夾

 
    
    
# 創建輸出資料夾（如果不存在）
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 取得資料夾中的所有 XML 檔案
xml_files = [file for file in os.listdir(input_folder) if file.endswith(".xml")]

for xml_file in xml_files:
    # 讀取 XML 檔案
    xml_path = os.path.join(input_folder, xml_file)
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # 取得影像寬度和高度
    size = root.find("size")
    width = float(size.find("width").text)
    height = float(size.find("height").text)

    # 創建對應的 TXT 檔案
    txt_file = os.path.splitext(xml_file)[0] + ".txt"
    txt_path = os.path.join(output_folder, txt_file)

    with open(txt_path, "w") as f:
        try:
            # 修改第一個標記索引值為 15
            obj = root.findall("object")[0]
            obj_name = obj.find("name").text
            bbox = obj.find("bndbox")
            x_min = float(bbox.find("xmin").text)
            y_min = float(bbox.find("ymin").text)
            x_max = float(bbox.find("xmax").text)
            y_max = float(bbox.find("ymax").text)

            # 轉換為 YOLO 格式的座標
            x_center = (x_min + x_max) / (2 * width)
            y_center = (y_min + y_max) / (2 * height)
            obj_width = (x_max - x_min) / width
            obj_height = (y_max - y_min) / height

            # 寫入 YOLO 格式的座標到 TXT 檔案
            f.write(f"{obj_name} {x_center} {y_center} {obj_width} {obj_height}\n")
            print(f"轉換完成: {xml_file} -> {txt_file}")
        except AttributeError as e:
            obj = root.findall("object")[0]
            obj_name = obj.find("name").text

            # 取得旋轉效正的資訊
            robndbox = obj.find("robndbox")
            cx = float(robndbox.find("cx").text)
            cy = float(robndbox.find("cy").text)
            w = float(robndbox.find("w").text)
            h = float(robndbox.find("h").text)
            angle = float(robndbox.find("angle").text)

            # 計算邊界框的座標
            x_min = cx - w / 2
            y_min = cy - h / 2
            x_max = cx + w / 2
            y_max = cy + h / 2

            # 轉換為 YOLO 格式的座標
            x_center = cx / width
            y_center = cy / height
            obj_width = w / width
            obj_height = h / height

            # 寫入 YOLO 格式的座標到 TXT 檔案
            f.write(f"{obj_name} {x_center} {y_center} {obj_width} {obj_height} {angle}\n")
            print(f"旋轉物件轉換完成: {xml_file} -> {txt_file}")

