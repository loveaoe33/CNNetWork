import os
import xml.etree.ElementTree as ET

def convert_coordinates(image_width, image_height, box):
    # 将边界框坐标转换为YOLO格式的归一化坐标
    x_min, y_min, x_max, y_max = box
    x_center = (x_min + x_max) / (2.0 * image_width)
    y_center = (y_min + y_max) / (2.0 * image_height)
    width = (x_max - x_min) / image_width
    height = (y_max - y_min) / image_height
    return x_center, y_center, width, height

def xml_to_yolo(xml_path, yolo_output_path):
    # 打开XML文件
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # 获取图像的宽度和高度
    size = root.find("size")
    image_width = int(size.find("width").text)
    image_height = int(size.find("height").text)

    # 创建输出文件
    with open(yolo_output_path, "w") as f_out:
        print(f"number:{xml_path}")
        for obj in root.findall("object"):
            # 获取对象的类别名称和边界框坐标
            class_name = obj.find("name").text
            box = obj.find("bndbox")

            # 检查 <bndbox> 是否存在
            if box is None:
                print(f"Error: 'bndbox' tag not found in {xml_path}")
                continue

            # 获取边界框坐标
            x_min = int(box.find("xmin").text)
            y_min = int(box.find("ymin").text)
            x_max = int(box.find("xmax").text)
            y_max = int(box.find("ymax").text)

            # 将边界框坐标转换为YOLO格式的归一化坐标
            x_center, y_center, width, height = convert_coordinates(image_width, image_height, (x_min, y_min, x_max, y_max))

            # 获取类别索引（如果您有类别映射表，可以使用映射表来获取索引）
            class_index = 0  # 这里默认类别索引为0

            # 将YOLO格式的目标信息写入输出文件
            f_out.write(f"{class_index} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

if __name__ == "__main__":
    # 指定包含XML文件的文件夹路径和输出的YOLO格式txt文件夹路径
    xml_folder_path = "C:\\Users\\loveaoe33\\Desktop\\train"
    yolo_output_folder_path ="C:\\Users\\loveaoe33\\Desktop\\Yolo_train"
    test_xml_folder_path = "C:\\Users\\loveaoe33\\Desktop\\test"
    test_yolo_output_folder_path = "C:\\Users\\anaconda3\\Desktop\\Yolo_test" 
    # 进行转换
    xml_to_yolo(test_xml_folder_path, test_yolo_output_folder_path)
    xml_to_yolo(xml_folder_path, yolo_output_folder_path)
