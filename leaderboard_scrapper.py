import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to log in to HackerRank
def login(username, password):
    try:
        driver = webdriver.Chrome()
        driver.get('https://www.hackerrank.com/auth/login')
        username_field = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, "input-1"))
        )
        username_field.send_keys(username)
        password_field = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, "input-2"))
        )
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)
        WebDriverWait(driver, 20).until(
            EC.url_contains("hackerrank.com/dashboard")
        )
        print("Login successful.")
        return driver

    except Exception as e:
        print("Login failed:", e)
        return None

# Function to scrape usernames and scores from a given page URL
def scrape_leaderboard(driver, url, seen_usernames):
    try:
        driver.get(url)
        
        if "leaderboard" in driver.current_url:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            all_a_tags = soup.find_all('a')
            
            usernames_list = []
            scores_list = []
            
            for a_tag in all_a_tags:
                if (
                    a_tag.get('data-value') and
                    a_tag.get('data-attr10')
                ):
                    username = a_tag.get('data-value')
                    score = a_tag.get('data-attr10')
                    
                    if username not in seen_usernames:
                        usernames_list.append(username)
                        scores_list.append(score)
                        seen_usernames.add(username)
            
            return usernames_list, scores_list
        
        else:
            print(f"Failed to fetch page: {url}")
            return [], []

    except Exception as e:
        print(f"Failed to scrape leaderboard: {e}")
        return [], []

# Function to scrape usernames and scores from 10 pages
def scrape_all_leaderboard(driver):
    all_user_scores = {}
    seen_usernames = set()
    
    for page in range(1, 11):
        url = f'https://www.hackerrank.com/leaderboard?filter=follows&filter_on=friends&page={page}&track=algorithms&type=practice'
        usernames, scores = scrape_leaderboard(driver, url, seen_usernames)
        
        for i in range(len(usernames)):
            all_user_scores[usernames[i]] = scores[i]
    
    return all_user_scores

def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def main():
    username = ''
    password = ''
    
    driver = login(username, password)
    
    if driver:
        all_user_scores = scrape_all_leaderboard(driver)
        
        if all_user_scores:
            sorted_user_scores = {k: v for k, v in sorted(all_user_scores.items(), key=lambda item: item[1], reverse=True)}
            
            print("Sorted Usernames and Scores from the leaderboard:")
            for username, score in sorted_user_scores.items():
                print(f"Username: {username}, Score: {score}")
            save_to_json(sorted_user_scores, 'leaderboard_data.json')
            print("Data saved to leaderboard_data.json")
        else:
            print("No data found on the leaderboard.")
        driver.quit()

if __name__ == "__main__":
    main()
