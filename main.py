from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def login(username, password):
    driver = webdriver.Chrome()
    driver.get('https://www.hackerrank.com/auth/login')
    try:
        username_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "input-1")))
        username_field.send_keys(username)
        password_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "input-2")))
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)
        WebDriverWait(driver, 10).until(EC.url_contains("hackerrank.com/dashboard"))
        print("Login successful.")
    except Exception as e:
        print("Login failed:", e)
    return driver

def scrape_leaderboard(username, password):
    driver = login(username, password)
    driver.get('https://www.hackerrank.com/leaderboard?filter=follows&filter_on=friends&page=1&track=algorithms&type=practice')
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "general-table-wrapper")))
        leaderboard_html = driver.page_source
        soup = BeautifulSoup(leaderboard_html, 'html.parser')
        general_table = soup.find('div', class_='general-table')
        leaderboard_items = general_table.find_all('div', class_='table-row-wrapper')
        
        for item in leaderboard_items:
            username = item.find('a', {'username': True})['username']
            score = item.find('a', {'username': True})['data-attr10']
            print(f"Username: {username}, Score: {score}")
    except Exception as e:
        print("Failed to scrape leaderboard:", e)
    
    driver.quit()

username = 'snikilpaul@gmail.com'
password = 'password@123'
scrape_leaderboard(username, password)
