from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to log in to HackerRank
def login(username, password):
    driver = webdriver.Chrome()
    driver.get('https://www.hackerrank.com/auth/login')
    try:
        username_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "input-1"))
        )
        username_field.send_keys(username)
        password_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "input-2"))
        )
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)
        WebDriverWait(driver, 10).until(
            EC.url_contains("hackerrank.com/dashboard")
        )
        print("Login successful.")

    except Exception as e:
        print("Login failed:", e)

    return driver

# Function to scrape usernames and scores from the leaderboard
def scrape_leaderboard(username, password):
    # Login to HackerRank with other Fn
    driver = login(username, password)
    driver.get('https://www.hackerrank.com/leaderboard?filter=follows&filter_on=friends&page=1&track=algorithms&type=practice')
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".leaderboard-list-item"))
        )
        rows = driver.find_elements_by_css_selector('.leaderboard-list-item')
        for row in rows:
            username = row.find_element_by_css_selector('.leaderboard-list-item-handle').text
            score = row.find_element_by_css_selector('.leaderboard-list-item-score').text
            print(f"Username: {username}, Score: {score}")
    except Exception as e:
        print("Failed to scrape leaderboard:", e)
    driver.quit()

#my credential, u can use it to complete hackerrank problems for me :)
username = 'snikilpaul@gmail.com'
password = 'password123'
scrape_leaderboard(username, password)
