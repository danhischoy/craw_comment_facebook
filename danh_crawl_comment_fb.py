from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from random import randint
from time import sleep
import pandas as pd
import os

# Khai báo biến browser:
service = Service("C:/Users/LAPTOP/OneDrive/Máy tính/webdriver/chromedriver.exe")
browser = webdriver.Chrome(service=service)

# Mở trang web facebook:
browser.get("http://facebook.com")
sleep(randint(2, 6))

# Điền thông tin vào ô user và pass:
txtUser = browser.find_element("id", 'email')
txtUser.send_keys("caodangdanh") # <--- Điền username thật vào đây

txtPass = browser.find_element("id", 'pass')
txtPass.send_keys("testpass")# <--- Điền password thật vào đây

sleep(randint(5, 10))

txtPass.send_keys(Keys.ENTER)
sleep(randint(5, 10))


# Mở URL của post:
browser.get("https://www.facebook.com/Gdtgroup.dn/posts/pfbid0VRxShN6nYshjti5zQm6GfnrD7DsYjV2e6oY1stVLDxZch7ph5goGem9RrGfVXBj3l")
sleep(randint(3, 6))

#Chuyển về tất cả bình luận:

#Click "Bình luận liên quan nhất" hoặc "Phù hợp nhất" để đưa ra các lựa chọn, sau đó chọn "Tất cả bình luận":
while True:
    showcomment_link = browser.find_elements("xpath",'//span[@class="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen x1s688f xi81zsa"]')
    for item in showcomment_link:
        if item.text == 'Bình luận liên quan nhất' or item.text == 'Phù hợp nhất' or item.text == 'Mới nhất' or item.text == 'Gần đây nhất':
            show_type_comment=item
            break
    try:
        show_type_comment.click()
        sleep(randint(3, 6))
        break
    except:
        break


showcomment_type = browser.find_elements("xpath",'//span[@class="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xk50ysn xzsf02u x1yc453h"]')
for item in showcomment_type:
    if item.text == 'Tất cả bình luận':
            typecomment_choose=item
            break
while True:
    try:
        typecomment_choose.click()
        sleep(randint(3, 6))
        break
    except:
        break


#Click xem thêm bình luận. Có thể là ("Xem" thêm "bình luận" trước) hoặc ("Xem" n "bình luận" trước):

while True:
    show_more_comment = browser.find_elements("xpath",'//span[@class="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen x1s688f xi81zsa"]')
    for item in show_more_comment:
        if 'Xem' in item.text and 'bình luận' in item.text:
            show_more_more=item
            break
    else:
        break

    try:
        show_more_more.click()
        sleep(randint(3, 6))
    except:
        break

# 5. Tìm tất cả các comment và ghi ra màn hình (hoặc file):
content_list = []
# -> lấy all thẻ div có thuộc tính role='article':
comment_list = browser.find_elements("xpath",("//div[@role='article']"))
for comment in comment_list:
    contents = comment.find_elements("xpath",("//span[@lang='vi-VN']"))
    for content in contents:
        for a_tag in content.find_elements("xpath", "//a[@class='x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f']"):
            browser.execute_script("arguments[0].remove()", a_tag)
        # Thêm content.text element vào content_list:
        content_list.append(content.text)
    break

# Tạo một dataframe từ content_list:
df = pd.DataFrame(content_list, columns=['Content'])

# Xác định đường dẫn tệp:
file_path = 'file_excel_name.xlsx'

# Kiểm tra xem file đã tồn tại chưa:
if os.path.exists(file_path):
    # Xóa file để điền file mới nếu đã tồn tại:
    os.remove(file_path)
# Viết dataframe vào excel:
df.to_excel(file_path)

sleep(randint(5, 10))

# Đóng browser
browser.close()
