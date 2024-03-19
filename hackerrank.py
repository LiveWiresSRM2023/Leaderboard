from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

id = "thalakratos5@gmail.com"
password = "Zeusfatherkratos"

options = webdriver.ChromeOptions()
options.add_experimental_option("detach",True)

driver = webdriver.Chrome(options=options)

url = "https://www.hackerrank.com/auth/login"

driver.get(url)

driver.find_element(By.ID,'input-1').send_keys(id)
driver.find_element(By.ID,'input-2').send_keys(password)
driver.find_element(By.CSS_SELECTOR,"button[data-analytics='LoginPassword'] span.ui-text").click()
sleep(2)

driver.get("https://www.hackerrank.com/leaderboard?page=1&track=algorithms&type=practice")

leaderboard_full = driver.find_element(By.CLASS_NAME,"general-table")
print(leaderboard_full.text)





