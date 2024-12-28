import os
import math
import re
from PIL import Image


def natural_sort_key(path):
    file_name = os.path.basename(path)  # 获取文件名
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', file_name)]

def create_mosaic(
    input_folder: str,
    output_path: str,
    target_width: int = 300,
    target_height: int = 300,
    background_color: tuple = (240, 240, 240)
):
    """
    将给定文件夹中的图片合并为一张大图并保存。
    
    参数：
    - input_folder: 图片所在文件夹路径
    - output_path: 输出的大图保存路径
    - target_width: 缩放后单张图片的宽度
    - target_height: 缩放后单张图片的高度
    - background_color: 背景颜色 (R, G, B)
    """
    
    # 1. 获取文件夹内所有图片路径
    image_paths = [
        os.path.join(input_folder, fname) 
        for fname in os.listdir(input_folder)
        if fname.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))
    ]
    


    # 对文件路径列表进行排序
    image_paths = sorted(image_paths, key=natural_sort_key)
    print(image_paths)
    
    if not image_paths:
        print("指定文件夹内没有找到可用的图片。")
        return

    # 2. 根据图片数量，决定排布(行数和列数)
    num_images = len(image_paths)
    # 这里选择“接近正方形”的排布方式，也可以根据需求自定义
    columns = int(math.ceil(math.sqrt(num_images)))  
    rows = int(math.ceil(num_images / columns))
    
    # 计算最终拼接图的宽度与高度
    mosaic_width = columns * target_width
    mosaic_height = rows * target_height
    
    # 3. 创建一个新的空白图像，用于放置所有缩放后的图片
    mosaic_image = Image.new(mode='RGB', size=(mosaic_width, mosaic_height), color=background_color)
    
    # 4. 逐一读取图片，按顺序粘贴到背景图上
    for index, image_path in enumerate(image_paths):
        # 打开并缩放图片
        img = Image.open(image_path)
        # 等比例缩放至指定大小，如果希望强制缩放为固定宽高，可替换为 img = img.resize((target_width, target_height))
        # img.thumbnail((target_width, target_height))#, Image.ANTIALIAS
        img = img.resize((target_width, target_height))
        
        # 计算在拼接图中的位置
        row_idx = index // columns
        col_idx = index % columns
        
        # 每张图左上角坐标
        x_offset = col_idx * target_width
        y_offset = row_idx * target_height
        
        # 如果缩放后的图像没有完全占满 target_width / target_height，可以在中心贴图
        # 这里演示居中的做法，也可根据需要直接贴左上角
        paste_x = x_offset + (target_width - img.width) // 2
        paste_y = y_offset + (target_height - img.height) // 2
        
        mosaic_image.paste(img, (paste_x, paste_y))
    
    # 5. 保存最终的大图
    mosaic_image.save(output_path, quality=95)
    print(f"拼接完成，图像已保存至：{output_path}")


if __name__ == "__main__":
    # 示例调用
    input_folder_path = "./img/"  # 替换为你的文件夹路径
    output_file_path = "./final_mosaic.jpg"
    
    create_mosaic(
        input_folder=input_folder_path,
        output_path=output_file_path,
        target_width=600, 
        target_height=800,
        background_color=(240, 240, 340)  # 浅色背景
    )