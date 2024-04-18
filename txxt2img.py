from PIL import Image, ImageDraw, ImageFont
import argparse
from open_file import browse

def text_to_image(txt_file_path, font_path='msyh.ttc', font_size=50, text_color='black', bg_color='white'):
    # 读取文本文件内容
    with open(txt_file_path, 'r', encoding='utf-8') as f:
        text = f.read()
        text = text.replace('\\\\r\\\\n', '\\n')
        print(text)
    # 创建一个白色背景的空白图像
    img = Image.new('RGB', (2800, 2900), color=bg_color)

    # 在图像上创建一个Draw对象
    draw = ImageDraw.Draw(img)

    # 设置要绘制的文本和字体
    font = ImageFont.truetype(font_path, size=font_size)

    # 确定文本的位置，并使用指定的字体和颜色将其绘制到图像上
    text_width, text_height = draw.textsize(text, font=font)
    x = (img.width - text_width) // 2
    y = (img.height - text_height) // 2
    draw.text((x, y), text, fill=text_color, font=font)

    # 保存图像到文件并返回文件路径
    output_file_path = txt_file_path.rsplit('.', 1)[0] + '.png'
    img.save(output_file_path)
    print('success')
    return output_file_path


text_to_image(browse(1)[1])




