from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import firebase_admin
from firebase_admin import credentials,db

# Function to log in to HackerRank
def login(username, password):
    try:
        driver = webdriver.Chrome()
        driver.get('https://www.hackerrank.com/auth/login')
        username_field = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.NAME, "username"))
        )
        username_field.send_keys(username)
        password_field = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.NAME, "password"))
        )
        password_field.send_keys(password)
        login_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-hr-focus-item="private"]'))
        )
        login_button.click()
        
        
        
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
                    a_tag.get('data-attr10')):

                    username = a_tag.get('data-value')
                    score = a_tag.get('data-attr10')

                    if username not in seen_usernames:
                        usernames_list.append(username)
                        scores_list.append(score)
                        seen_usernames.add(username)
                        
            return usernames_list, scores_list
        
        else:
            print("Failed to fetch page: ",url)


    except Exception as e:
        print("Failed to scrape leaderboard: ",e)


# Function to scrape usernames and scores from 20 pages max
def scrape_all_leaderboard(driver):
    try:
        all_user_scores = {}
        seen_usernames = set()
    
        for page in range(1, 21):
            url = f'https://www.hackerrank.com/leaderboard?filter=follows&filter_on=friends&page={page}&track=algorithms&type=practice'
            usernames, scores = scrape_leaderboard(driver, url, seen_usernames)
        
            for i in range(len(usernames)):
                all_user_scores[usernames[i]] = scores[i]
                
            if len(usernames)<2:
                break
    
        return all_user_scores
    except Exception as e:
        print("Failed to scrape the first 20 page data",e)


        
        
#Function to update data in Firebase        
def firebase_upload(leaderboard_data):
    try:
        credential=credentials.Certificate('credentials.json') #Replace the file name with your Firebase credential file
        firebase_admin.initialize_app(credential,{'databaseURL':'https://certain-root-333610-default-rtdb.asia-southeast1.firebasedatabase.app/'})
        ref=db.reference('/')
        ref.set({})
        
        rank=1
        for username,score in leaderboard_data.items():
            ref.child('Leaderboard').child(str(rank)).set({'Username':username,'score':score})
            rank+=1
        print("Firebase database has updated")
        
        
    except Exception as e:
        print("Failed to upload data to Firebase",e)
    

# Credentials
username = ''
password = ''

driver = login(username, password)

if driver:
    all_user_scores = scrape_all_leaderboard(driver)
    
    if all_user_scores:
        sorted_user_scores = {k: v for k, v in sorted(all_user_scores.items(), key=lambda item: float(item[1]), reverse=True)}
        print("Usernames and Scores from the leaderboard:")
        for username, score in sorted_user_scores.items():
            print(f"Username: {username}, Score: {score}")
        firebase_upload(sorted_user_scores)


    driver.quit()
