from  PIL import Image
import random          #导入 random(随机数) 模块
import pytesseract     #导入识别验证码信息包
import time
import os
from pathlib import Path
#截图，裁剪图片并返回验证码图片名称
# _save_url 保存路径 yanzhengme_img_xpath 验证码元素标识
def image_cj(driver, _save_url, yanzhengme_img_xpath):
    try:
        _file_name = random.randint(0, 100000)
        _file_name_wz = str(_file_name) + '.png'
        # _file_url = _save_url + _file_name_wz
        _file_url = Path(os.path.join(_save_url, _file_name_wz)).as_posix()
        driver.get_screenshot_as_file(_file_url)  # get_screenshot_as_file截屏
        captchaElem = driver.find_element_by_xpath(yanzhengme_img_xpath)  # # 获取指定元素（验证码）
        # 因为验证码在没有缩放，直接取验证码图片的绝对坐标;这个坐标是相对于它所属的div的，而不是整个可视区域
        # location_once_scrolled_into_view 拿到的是相对于可视区域的坐标  ;  location 拿到的是相对整个html页面的坐标
        captchaX = int(captchaElem.location['x'])
        captchaY = int(captchaElem.location['y'])
        # 获取验证码宽高
        captchaWidth = captchaElem.size['width']
        captchaHeight = captchaElem.size['height']

        captchaRight = captchaX + captchaWidth
        captchaBottom = captchaY + captchaHeight

        imgObject = Image.open(_file_url)  #获得截屏的图片
        imgCaptcha = imgObject.crop((captchaX, captchaY, captchaRight, captchaBottom))  # 裁剪
        yanzhengma_file_name = str(_file_name) + '副本.png'
        imgCaptcha.save(Path(os.path.join(_save_url, yanzhengma_file_name)).as_posix())
        return  yanzhengma_file_name
    except Exception as e:
        print('错误 ：', e)



# 获取验证码图片中信息（保存地址，要识别的图片名称）
def image_text(_save_url,yanzhengma_file_name):
    # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'
    # yanzhengma_file_url = 'F:\\Python\\workspace\\selenium_demo3_test\\test\\case\\PT\\'+ _save_url
    image = Image.open(_save_url + yanzhengma_file_name)
    text = pytesseract.image_to_string(image)
    print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$图片中的内容为：', text)
    return text



#截图并写入验证码（保存地址，验证码元素，验证码输入框元素）
def jietu_xieru(driver,_save_url, yanzhengme_img_xpath, yanzhengma_in_xpath, log_save_path):
    if not os.path.exists(_save_url): # 若文件夹不存在 即建立一个文件夹
        os.makedirs(_save_url)

    # 截图当前屏幕，并裁剪出验证码保存为:_file_name副本.png，并返回名称
    yanzhengma_file_name = image_cj(driver,_save_url, yanzhengme_img_xpath)  ##对页面进行截图，弹出框宽高（因为是固定大小，暂时直接写死了）
    # 获得验证码图片中的内容
    text = image_text(_save_url, yanzhengma_file_name)
    # 写入验证码
    run_element(driver, yanzhengma_in_xpath, "验证码输入框", text, log_save_path)
    time.sleep(2)



def run_element(in_driver, xpath_str, description, in_str=None, log_save_path=None):
    time.sleep(5 + random.randint(0,5))
    try:
        element = in_driver.find_element_by_xpath(xpath_str)
        if in_str == None:
            element.click()
        else:
            element.send_keys(in_str)
    except Exception as e:
        print(description + "元素未能获取 \n")
        with open(log_save_path, "a+") as fa:
            fa.write(description + "元素未能获取 \n")

def is_get_element(in_driver, xpath_str, description, log_save_path):
    try:
        in_driver.find_element_by_xpath(xpath_str)
        return True
    except Exception as e:
        print(description + "元素未能获取 \n")
        with open(log_save_path, "a+") as fa:
            fa.write(description + "元素未能获取 \n")
        return False
    












