from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from util import jietu_xieru, image_text
import random
import os
from pathlib import Path

"""
# #截图裁剪出验证码，并写入验证码输入框中（保存地址，验证码元素，验证码输入框元素）
# jietu_xieru(driver,'img\\login\\','imgvercodeLogin','verfieldUserText')
# driver.find_element_by_xpath('//*[@id="loginForm"]/div[6]/button').click()  #点击登录

# _user_name = driver.find_element_by_xpath('//*[@id="userWrap"]/div/p').get_attribute('innerHTML')
# user_name = '用户1'
# #判断不相等，则未登录成功，则为验证码输入错误（此时，只考虑验证码，且图文识别并非百分之百正确）一直循环读取验证码输入
# while _user_name != user_name:
#     jietu_xieru(driver, 'img\\login\\', 'imgvercodeLogin', 'verfieldUserText')
#     driver.find_element_by_xpath('//*[@id="loginForm"]/div[6]/button').click()  # 点击登录
#     _user_name = driver.find_element_by_xpath('//*[@id="userWrap"]/div/p').get_attribute('innerHTML')
# else:
#     print('#############################################登录成功#############################################')
#     pass
"""



def login_post(URL, user_name, password, log_save_dirs, image_save_dirs):
    driver = webdriver.Edge()   
    driver.get(URL)
    if not os.path.exists(log_save_dirs):
        os.makedirs(log_save_dirs)
    if not os.path.exists(image_save_dirs):
        os.makedirs(image_save_dirs)
    
    log_save_path = log_save_dirs  + str(time.time())+".txt"
    
    # 输入用户名 //*[@id="ls_username"]
    run_element(driver, '//*[@id="ls_username"]', '用户名输入框', user_name, log_save_path)
    # 输入密码 //*[@id="ls_password"]
    run_element(driver, '//*[@id="ls_password"]', '密码输入框', password, log_save_path)
    # 登录按键 //*[@id="lsform"]  /div/div/table/tbody/tr[2]/td[3]/button  //*[@id="lsform"]/div/div/table/tbody/tr[2]/td[3]/button
    run_element(driver, '//*[@id="lsform"]/div/div/table/tbody/tr[2]/td[3]/button', '登录按钮', None, log_save_path) 

    # 判断是否需要重新登录 //*[@id="messagetext"] //*[@id="messagetext"]/p 
    if is_get_element(driver, '//*[@id="messagetext"]', '重新登录页面', log_save_path): # 在新的网页重新登录
        # //*[@id="username_LC41d"]  重新登录的网页
        with open(log_save_path, "a+") as fa:
            fa.write("登录失败，重新登录 \n")
        print("登录失败，重新登录 \n")
        
        # 输入用户名 //*[@id="username_LC41d"]   //*[@id="ls_username"]
        run_element(driver, '//*[@id="ls_username"]', '登录页面的用户名框', user_name, log_save_path)
        # 输入密码 //*[@id="password3_LC41d"]  //*[@id="ls_password"]
        run_element(driver, '//*[@id="ls_password"]', '登录页面的密码框', password, log_save_path)
        # 登录按键  //*[@id="loginform_LC41d"]/div/div[6]/table/tbody/tr/td[1]/button  //*[@id="lsform"]/div/div/table/tbody/tr[2]/td[3]/button
        run_element(driver, '//*[@id="lsform"]/div/div/table/tbody/tr[2]/td[3]/button', '登录页面的登录按钮', None, log_save_path) 
        

    # //*[@id="main_message"] /html/body/div[6]/div/div[2]
    # elif driver.find_element_by_xpath('//*[@id="main_message"]/div/div[1]/h3').text == "请输入验证码后继续登录":
    elif is_get_element(driver, '//*[@id="main_message"]', '图形验证码网页', log_save_path):
        # 验证码图片  //*[@id="vseccode_cSV010AF"]/img  # image_save_dirs
        yanzhengme_img_xpath = '//*[@id="main_message"]/div/div[2]/div[1]/div[1]/form/div/span/div/table/tbody/tr/td/span[2]/img'
        yanzhengma_in_xpath = '//*[@id="main_message"]/div/div[2]/div[1]/div[1]/form/div/span/div/table/tbody/tr/td/input'
        jietu_xieru(driver, image_save_dirs, yanzhengme_img_xpath, yanzhengma_in_xpath, log_save_path)
    

    # 登录成功 进行发帖
    # 发帖按钮 //*[@id="newspecial"]
    run_element(driver, '//*[@id="newspecial"]', '发帖按钮', None, log_save_path)
    # 主题框输入 //*[@id="subject"]
    title = "挖挖矿挖挖矿" + time.asctime(time.localtime(time.time())) 
    run_element(driver, '//*[@id="subject"]', '主题输入框', title, log_save_path)
    # 正文输入 //*[@id="e_textarea"]
    context = " \n".join(["挖挖挖挖挖矿"]*random.randint(1,10))
    run_element(driver, '//*[@id="e_textarea"]', '正文输入框', context, log_save_path)
    # 发表帖子 //*[@id="postsubmit"]
    run_element(driver, '//*[@id="postsubmit"]', '发表按钮', None, log_save_path)
    with open(log_save_path, "a+") as fa:
        fa.write("发布成功 \n")

    time.sleep(10)
    driver.quit()
    return True

def run_element(in_driver, xpath_str, description, in_str=None, log_save_path=None):
    time.sleep(5 + random.randint(0,5))
    try:
        element = in_driver.find_element(By.XPATH, xpath_str)
        if in_str == None:
            element.click()
        else:
            element.send_keys(in_str)
    except Exception as e:
        print(description + "元素未能获取 \n")
        with open(log_save_path, "a+") as fa:
            fa.write(time.asctime(time.localtime(time.time()))  + description + "元素未能获取 \n")

def is_get_element(in_driver, xpath_str, description, log_save_path):
    try:
        in_driver.find_element(By.XPATH, xpath_str)
        return True
    except Exception as e:
        print(description + "元素未能获取 \n")
        with open(log_save_path, "a+") as fa:
            fa.write(time.asctime(time.localtime(time.time())) + description + "元素未能获取 \n")
        return False
    
URL = "https://www.jietiandi.net/forum.php?mod=forumdisplay&fid=178"
user_name = ' '
password = ' '
nums = 30
log_dirs = "./log"
image_save_dirs = "./save_yanzhengma_img"

if not os.path.exists(log_dirs):
    os.makedirs(log_dirs)
if not os.path.exists(image_save_dirs):
    os.makedirs(image_save_dirs)


# is_run_flag = login_post(URL, user_name, password, log_dirs, image_save_dirs)
for _ in range(nums):
    sleep_time = 15*60 + random.randint(0, 60)
    try:
        login_post(URL, user_name, password, log_dirs, image_save_dirs)
        time.sleep(sleep_time)
    except Exception as e:
        log_save_path = os.path.join(log_dirs, time.asctime(time.localtime(time.time()))+".txt")
        log_save_path = Path(log_save_path).as_posix()
        with open(log_save_path, "a+") as fa:
            fa.write(e.msg + "发帖失败 \n")
        break
