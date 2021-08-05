from typing import Dict
from typing_extensions import Literal
from selenium import webdriver
import time
import selenium as se
import os
from pyvirtualdisplay import Display
from django.conf import settings
# from request_client.models import SearchKeyword
# from request_client.serializer import PostCommentsSerializer
from .extractors import PageExtractors
from .serializer_functions import SerializerFunctions
import logging
log = logging.getLogger(__name__)

class RequestClient:
    '''
    Selenium based request client for collecting post comments
    Set user and password in project settings
    '''

    display = Display(visible=0, size=(800, 800))

    login_url = settings.FB_LOGIN_URL

    options = se.webdriver.ChromeOptions()

    prefs = {"profile.default_content_setting_values.notifications": 2}
    options.add_experimental_option("prefs", prefs)
    DEBUG = settings.DEBUG
    if DEBUG is False:
        display.start()
    driver = se.webdriver.Chrome(settings.DRIVER_PATH, chrome_options=options)

    
        # options.add_argument("--user-data-dir=chrome-data")
        # options.add_argument("--remote-debugging-port=9222")
        # options.add_argument('--headless')
        # options.add_argument('--no-sandbox')
        # options.add_argument('--disable-dev-shm-usage')

    def start_driver(self) -> None:
        '''
        Initiate the search with query keyword
        '''
        if self.DEBUG:
            log.debug('start_driver')

        self.driver.set_page_load_timeout(1800)
        self.driver.get(self.login_url)
        self.driver.set_window_size(1400, 1000)
        self.get_time_sleep()

    def restart_driver(self) -> None:
        '''
        Create a fresh instance of webdriver in case previous fails to connect
        '''
        if self.DEBUG:
            log.debug('restart_driver')
        try:
            self.driver.close()
        except:
            self.driver = None
        self.driver = se.webdriver.Chrome(settings.DRIVER_PATH,
                                          chrome_options=self.options)

    def check_session_cookies(self) -> (Literal[True, -1, 0]):
        '''
        Check for successfull authentication and verify generated session cookies
        '''
        if self.DEBUG:
            log.debug('check_session_cookies')

        cookies = self.driver.get_cookies()
        # pickle.dump(cookies, open(settings.COOKIE_FILE,"wb"))
        self.request_cookies = {}
        for cookie in cookies:
            name = cookie.get('name', None)
            value = cookie.get('value', None)
            self.request_cookies[name] = value

        return True if self.check_login() else self.login_function()

    def check_login(self) -> bool:
        '''
        Verify unique key in cookies to validate cookies
        '''
        if self.DEBUG:
            log.debug('check_login')
        return True if 'c_user' in self.request_cookies else False

    def get_new_file_name(self) -> str:
        '''
        Generate new file name for saving screenshot for query keyword
        '''
        if self.DEBUG:
            log.debug('get_new_file_name')

        screenshot_dir = settings.SCREENSHOT_DIR + self.query_keyword
        os.makedirs(screenshot_dir, exist_ok=True)
        total_files = len(os.listdir(screenshot_dir))
        return str(screenshot_dir + '/' + str(total_files) + '.png')

    def get_comment_screenshot(self) -> None:
        '''
        Take screenshots while scrolling through the posts
        '''
        if self.DEBUG:
            log.debug('get_comment_screenshot')
        self.driver.save_screenshot(self.get_new_file_name())

    def get_time_sleep(self, sleep_time: int = 3) -> None:
        '''
        Get explicit time wait to allow DOM to update completely
        '''
        if self.DEBUG:
            log.debug('get_time_sleep')
        return time.sleep(sleep_time)

    def toogle_comments_section(self) -> None:
        '''
        Toggle comment footers in feed object to load post comments
        '''
        if self.DEBUG:
            log.debug('toogle_comments_section')
        comment_blocks = self.driver.find_elements_by_xpath(
            PageExtractors.comments_block)

        for element in comment_blocks:
            try:
                element.click()
                self.get_time_sleep()
                self.get_comment_screenshot()
                self.get_time_sleep(2)
            except:
                continue

    def scroll_page(self) -> None:
        '''
        Execute scripts for scrolling through feeds and loading new feeds
        '''
        if self.DEBUG:
            log.debug('scroll_page')

        SCROLL_PAUSE_TIME = 3
        self.toogle_comments_section()
        last_height = self.driver.execute_script(PageExtractors.body_height)
        temp = 1
        while temp < 3:

            self.driver.execute_script(PageExtractors.scroll_body)
            self.get_time_sleep(SCROLL_PAUSE_TIME)

            new_height = self.driver.execute_script(PageExtractors.body_height)

            self.get_time_sleep(SCROLL_PAUSE_TIME)
            self.toogle_comments_section()

            if new_height == last_height:
                break
            last_height = new_height
            temp += 1

    def remove_special_char_from_str(self, string: str = None) -> str:
        '''
        Remove common strings from comments and remove non-ASCII characters
        '''

        if self.DEBUG:
            log.debug('remove_special_char_from_str', string)

        common_str_index = string.rfind('Like')
        string = string[:common_str_index]
        string = " ".join(string.split())
        return string

    # def save_extracted_comments(self, comments: list) -> Dict:
    #     '''
    #     Serialize the collected post comments PostComment models
    #     '''
    #   if self.DEBUG:  
    #   log.debug('save_extracted_comments', comments)
    #     search_keyword = self.query_keyword
    #     keyword_instance, _ = SearchKeyword.objects.get_or_create(
    #         keyword=search_keyword)
    #     data_set = {'fk_keyword': keyword_instance.keyword_id}

    #     comments_data = [{
    #         'comment': comment,
    #         **data_set
    #     } for comment in comments]
    #     instance = PostCommentsSerializer(data=comments_data, many=True)

    #     if instance.is_valid():
    #         instance.save()
    #   if self.DEBUG:      
    #   log.debug('is_valid', comments_data)
    #         return {'data': instance.data, 'saved': True}
    #     else:
    #         return {'error': instance.errors, 'saved': False}

    def extract_comments_from_feeds(self) -> Dict:
        '''
        Extract Comment text from comment html elements
        '''
        if self.DEBUG:
            log.debug('extract_comments_from_feeds')
        comments = []

        comment_elements = self.driver.find_elements_by_xpath(
            PageExtractors.comment_xpath)
        # if self.DEBUG:
        #   log.debug(comment_xpath,comment_xpath)

        for elements in comment_elements:
            # try:
            post_comment = elements.get_attribute('innerText')
            if len(post_comment) > 50:
                comments.append(
                    self.remove_special_char_from_str(post_comment))
            # except:
            #     pass
        return SerializerFunctions().save_extracted_comments(
            comments, self.query_keyword)

    def send_search_query(self, search_keyword: str = '') -> Dict:
        '''
        Send request for retrieving search results using keyword
        '''
        if self.DEBUG:
            log.debug('send_search_query')
        self.query_keyword = search_keyword
        query_url = self.login_url + 'search/posts?q={}'.format(search_keyword)

        self.get_time_sleep()
        self.driver.get(query_url)
        self.get_time_sleep(10)
        self.scroll_page()

        return self.extract_comments_from_feeds()

    def login_function(self) -> Literal[True, -1, 0]:
        '''
        Login to Facebook and create fresh instance of cookies
        '''
        if self.DEBUG:
            log.debug('login_function')
        login_user = settings.FB_USER_NAME
        login_pass = settings.FB_PASSWORD
        flag = 1
        while flag <= 2:
            try:
                self.driver.find_element_by_xpath(
                    PageExtractors.email_selector).send_keys(login_user)
                self.driver.find_element_by_xpath(
                    PageExtractors.passwd_selector).send_keys(login_pass)
                self.driver.find_element_by_xpath(
                    PageExtractors.submit_selector).click()
                self.get_time_sleep()

                login_status = self.check_session_cookies()
                if login_status:
                    return login_status

            except Exception as e:
                if self.DEBUG:
                    log.debug('--------Fetch page Timeout------', e)
                flag += 1
        if flag == 3:
            return -1

        return 0

    def main(self, search_keyword):
        '''
        Controller for checking the status of driver and sending request with keyword
        '''
        if self.DEBUG:
            log.debug('main')

        try:
            self.start_driver()
        except:
            self.restart_driver()
            self.start_driver()

        login_status = self.check_session_cookies()
        if login_status is True:
            return self.send_search_query(search_keyword)
