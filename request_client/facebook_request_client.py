from typing import Dict
from selenium import webdriver
import json
import time
import selenium as se
import os
from  pyvirtualdisplay import Display
import sys
from datetime import datetime
from django.conf import settings 
from request_client.models import SearchKeyword
from request_client.serializer import PostCommentsSerializer
import pickle


class RequestClient:
    display = Display(visible=0, size=(800, 800))
    login_url = settings.FB_LOGIN_URL
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    
    options = se.webdriver.ChromeOptions()
    # options.add_argument("--user-data-dir=chrome-data")
    # options.add_argument("--remote-debugging-port=9222")
    # options.add_argument('--headless')
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option("prefs",prefs)

    driver = None   
    driver = se.webdriver.Chrome('/usr/lib/chromium-browser/chromedriver',chrome_options=options)
    
    


    user_id = "praanshugroverescraper1@gmail.com"
    password = "Indy@123"


    def restart_driver(self):
        print('restart_driver')
        try:
            self.driver.close()
        except:    
            self.driver = None
        self.driver = se.webdriver.Chrome('/usr/lib/chromium-browser/chromedriver',chrome_options=self.options)

    def check_session_cookies(self):
        print('check_session_cookies')
        cookies = self.driver.get_cookies()
        # pickle.dump(cookies, open(settings.COOKIE_FILE,"wb"))    
        self.request_cookies = {}
        for cookie in cookies:
            name  = cookie.get('name',None)
            value = cookie.get('value',None)
            self.request_cookies[name] = value

        return True if self.check_login() else self.login_function()
        



    def check_login(self)-> bool:
        print('check_login')
        return True if 'c_user' in self.request_cookies else False


    def get_new_file_name(self):
        print('get_new_file_name')

        screenshot_dir = settings.SCREENSHOT_DIR + self.query_keyword
        os.makedirs(screenshot_dir, exist_ok=True)
        total_files = len(os.listdir(screenshot_dir))
        return screenshot_dir+'/'+ str(total_files)+'.png' 

    def get_comment_screenshot(self):
        print('get_comment_screenshot')
        self.driver.save_screenshot(self.get_new_file_name())

    def get_time_sleep(self,sleep_time:int = 3):
        print('get_time_sleep')
        return time.sleep(sleep_time)


    def toogle_comments_section(self):
        print('toogle_comments_section')
        comment_blocks = self.driver.find_elements_by_xpath('//*[@aria-label="Leave a comment"]')
        for element in comment_blocks:
            try:
                element.click()
                self.get_time_sleep()
                self.get_comment_screenshot()
                self.get_time_sleep(2)
            except:
                continue


    def scroll_page(self):
        print('scroll_page')
        SCROLL_PAUSE_TIME = 3
        self.toogle_comments_section()
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        temp =1
        while temp<3:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            self.get_time_sleep(SCROLL_PAUSE_TIME)
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            self.get_time_sleep(SCROLL_PAUSE_TIME)
            self.toogle_comments_section()

            if new_height == last_height:
                break
            last_height = new_height  
            temp+=1 

 
    def remove_special_char_from_str(self,string:str=None) -> str:
        print('remove_special_char_from_str',string)
        common_str_index = string.rfind('Like')
        string = string[:common_str_index]
        string = " ".join(string.split())
        # str_en = str.encode("ascii", "ignore")
        # str_de = str_en.decode()
        return string 

        


    def save_extracted_comments(self,comments:list) -> Dict:
        print('save_extracted_comments',comments)
        search_keyword = self.query_keyword
        keyword_instance, _ = SearchKeyword.objects.get_or_create(keyword=search_keyword)
        data_set  = {'fk_keyword':keyword_instance.keyword_id}
        
        comments_data = [{'comment':comment,**data_set} for comment in comments]
        instance = PostCommentsSerializer(data=comments_data,many=True)
        
        if instance.is_valid():
            instance.save()
            print('is_valid',comments_data)
            return {'data':instance.data,'saved':True}
        else:
            return {'error':instance.errors,'saved':False}   






    def extract_comments_from_feeds(self):
        print('extract_comments_from_feeds')
        comments = []
        comment_xpath = "//*[contains(@aria-label,'Comment by') or contains(@aria-label,'Reply by')]"
        comment_elements = self.driver.find_elements_by_xpath(comment_xpath)
        print(comment_xpath,comment_xpath)
        for elements in comment_elements:
            # try:
            post_comment = elements.get_attribute('innerText')
            if len(post_comment) > 50:
                comments.append(self.remove_special_char_from_str(post_comment))
            # except:
            #     pass
        return self.save_extracted_comments(comments)
        


    def send_search_query(self,search_keyword:str = ''):
        print('send_search_query')
        self.query_keyword = search_keyword
        query_url =  self.login_url +'search/posts?q={}'.format(search_keyword)
        self.get_time_sleep()
        self.driver.get(query_url)
        self.get_time_sleep(10)
        self.scroll_page()
        
        return self.extract_comments_from_feeds()
        

    # def set_cookies(self):
    #     if os.path.isfile(settings.COOKIE_FILE):
    #         cookies = pickle.load(open(settings.COOKIE_FILE, "rb"))
    #     for cookie in cookies:
    #         self.driver.add_cookie(cookie)

    def start_driver(self):
        print('start_driver')
        # self.display.start()
        
        # self.driver = se.webdriver.Chrome('/usr/lib/chromium-browser/chromedriver',chrome_options=self.options)
        # self.options.add_argument("user-data-dir=chrome-data")
        self.driver.set_page_load_timeout(1800)
        self.driver.get(self.login_url)
        # self.set_cookies()
        
        self.driver.set_window_size(1400,1000)
        self.get_time_sleep()

    
    def main(self,search_keyword):
        print('main')
        
        try:
            self.start_driver()
        except:
            self.restart_driver()
            self.start_driver()


        login_status = self.check_session_cookies()
        if login_status is True:
            return self.send_search_query(search_keyword)
            # return result
            # if 'error' in .keys():
            #     return False
            #     # self.driver.close()
            # else:
            #     return True
            #     # self.driver.close()
                





    def login_function(self):
        print('login_function')
        login_user   = settings.FB_USER_NAME
        login_pass   = settings.FB_PASSWORD
        
        flag=1
        while flag<=2:
            try:
                # self.display.start()
                # self.driver = se.webdriver.Chrome('/usr/lib/chromium-browser/chromedriver',chrome_options=self.options)
                # driver=self.driver
                # driver.set_page_load_timeout(1800)
                # driver.get(self.login_url)
                # driver.set_window_size(1400,1000)

                self.driver.find_element_by_xpath('//*[@id="email"]').send_keys(login_user)
                self.driver.find_element_by_xpath('//*[@id="pass"]').send_keys(login_pass)
                # self.driver.save_screenshot('midday.png')
                self.driver.find_element_by_xpath('//*[@type="submit"]').click()
                self.get_time_sleep()
                # cookies = self.driver.get_cookies()
                # self.cookies, login_status = self.parse_cookies(cookies)
                login_status = self.check_session_cookies()
                if login_status:
                    return login_status
            
            except Exception as e:
                print('--------Fetch page Timeout------',e)
                flag += 1
        if flag==3 :
            return -1
        
        return 0        


