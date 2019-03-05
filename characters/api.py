# FLASK DEPENDENCIES
from flask import Flask, Blueprint,request,jsonify,current_app
import json
import requests
import logging
from application import charactersDB as charactersDB
from time import sleep

# SCRAPPER DEPENDENCIES
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# BLUEPRINT AND APP DEFINITION
characters_app = Blueprint('characters_app', __name__)
logger = logging.getLogger(__name__)

# HEADERS FOR SCRAPPER BROWSER
headers = {'User-agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; FSL 7.0.6.01001)'}
headless_mode = True

# SCRAPPER FUNCTION START
@characters_app.route('/characters', methods=['GET'])
def get_characters():

        # DEFINE BROWSER OPTIONS
        chrome_options = webdriver.ChromeOptions()
        if headless_mode:
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--headless')
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36")
        chrome_options.add_argument('window-size=1080x1920')

        # OPEN URL
        basePage = 'https://naruto.fandom.com/wiki/Category:Characters'
        response_data = {}
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get(basePage)
        last_page = False

        # GET LIST OF CHARACTERS 
        char_list = driver.find_elements_by_xpath('//*[@id="mw-content-text"]/div[2]/ul/li/a')

        # WHILE LOOP UNTIL THE 'NEXT' BUTTON IS NOT PRESENT (IN ORDER TO GET ALL PAGES)
        while True:
            # FOR EACH CHARACTER IN THE LIST
            for key in range(len(char_list)):

                # OPEN CHARACTER URL IN NEW TAB
                link = char_list[key].get_attribute('href')
                response_data['source'] = link
                char_list[key].send_keys(Keys.COMMAND + Keys.RETURN)

                # WAIT FOR TAB TO FINISH LOADING
                sleep(2) 
                # SWITCHING TO RECENTLY OPENED TAB 
                driver.switch_to_window(driver.window_handles[1])            

                # GET CHARACTER TITLE
                title = driver.find_element_by_xpath('//h1[@class="page-header__title"]').text
                response_data['title'] = title

                # GET CHARACTER MAIN INFO
                child_elem = driver.find_elements_by_xpath('//*[@id="mw-content-text"]/*')
                flag = 0
                p_count = 0
                section = {}
                p_list = {}
                details = {}
                header = ""

                # FOREACH CHARACTER INFO SECTION
                for child_key in range(len(child_elem)):
                    
                    # AFTER ANALIZING, DISCOVERED A PATTERN IN WHICH THERE'S AN H2 TAG BEFORE A 
                    # PARAGRAPH WHICH CONTAINS THE INFORMATION 

                    # DETECT IF THERE'S A NEW SECTION / PARAGRAPH
                    if child_elem[child_key].tag_name == 'h2' :
                        flag = 1
                        # IF THERE ARE P FOR THIS HEADER, STORE IT WITH THE GIVEN KEY
                        if p_count>0:
                            section[new_key] = p_list
                            p_count = 0
                            p_list = {}
                    elif child_elem[child_key].tag_name == 'p':
                        flag = 0
                    else: 
                        flag = 2

                    # IF THERE IS A PARAGRAPH, STORE IT AND INCREASE THE PARAGRAPH COUNT, ELSE
                    # IF THERE'S A HEADER (H2), STORE THE TEXT TO BE USED AS A KEY TO THE JSON
                    if flag == 0:
                        # FOR FIRST INTRODUCTION PARAGRAPH WITHOUT HEADER
                        if child_key == 1:
                            section['intro'] = child_elem[child_key].text
                        else:
                            p_count = p_count+ 1
                            p_list[str(p_count)] = child_elem[child_key].text  
                    elif flag == 1:
                        new_key = child_elem[child_key].text
                      
                # GET DETAILS TABLE
                table = driver.find_element_by_class_name('infobox')
                # FOR EACH TABLE ROW
                rows = table.find_elements(By.TAG_NAME, "tr")
                for row in rows:
                    # GET ALL ELEMENTS IN ROW
                    all_children = row.find_elements_by_xpath(".//*")
                    
                    # ITERATE THE DETAILS TABLE AND SAVE INFO IN DICTIONARY
                    for c in all_children:
                        if c.get_attribute("class") == "imagecell":
                            a = c.find_elements(By.TAG_NAME, "a")
                            details["image"] = a[0].get_attribute("href")
                        elif c.get_attribute("class") == "mainheader" and "edit" not in c.text:
                            header = c.text
                            if "Collapse" not in header and "Expand" not in header:
                                details[header] = {}
                        elif c.get_attribute("class") == "":
                            if c.tag_name == "th" and "Collapse" not in header and "Expand" not in header:
                                th = c.text
                                details[header][th] = "pending"
                            elif c.tag_name == "td" and "Collapse" not in header and "Expand" not in header:
                                if header in details:
                                    details[header][th] = c.text        
                #print(details)

                # ADD THE INFORMATION SECTION TO THE RESPONSE
                response_data['info'] = section

                # ADD THE DETAILS SECTION TO THE RESPONSE
                response_data['details'] = details

                # CLOSE WINDOWS
                driver.close() 
                driver.switch_to_window(driver.window_handles[0])

                # INSERT THE ELEMENT INTO GIVEN COLECTION
                col = charactersDB.db.characters
                col.update_one({'title': title}, 
                    {'$set': { 'title':title,'info': response_data['info'],'details': response_data['details']}}, upsert=True)

                # DEBUG PURPOSES
                print((response_data['title']))

                # CLEAR RESPONSE DICTIONARY
                response_data = {}
                
            #W HEN FINISHING WITH ACTUAL LIST, IF 'NEXT' BUTTON PRESENT OPEN THE LINK
            if driver.find_element_by_class_name('category-page__pagination-next'):
                next_link = driver.find_element_by_class_name('category-page__pagination-next')
                driver.get(next_link.get_attribute("href"))
                sleep(1)
            
            # GET NEXT PAGE CHARACTERS
            char_list = driver.find_elements_by_xpath('//*[@id="mw-content-text"]/div[1]/ul/li/a')

            # IF 'NEXT' BUTTON IS NOT PRESENT AND THE CHARACTER LIST IS LESS THAN 200 (LAST PAGE) BREAK THE WHILE LOOP
            if len(driver.find_elements_by_class_name('category-page__pagination-next'))==0 and last_page==True:
                driver.close()
                break
                
            # FOR LAST PAGE
            if (len(char_list)<200):
                last_page = True
    
        return jsonify("Success")