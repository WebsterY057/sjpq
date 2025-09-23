#1/selenium打开浏览器；访问要爬取的页面；获取页面的数据
from selenium import webdriver
import time
from selenium.webdriver.common.by import By

driver =webdriver.Chrome()
driver.get('https://www.baidu.com')

ele = driver.find_element(By.XPATH,'//[@id="kw"]')

ele.send_keys("人大代表")
time.sleep(1)
ele.clear()

driver.maximize_window()
time.sleep(1)

driver.refresh()

time.sleep(5)
driver.quit()
#当request请求无法访问网站，可以考虑使用selenium

#元素的定位和等待
#元素的属性和操作

#iframe切换  