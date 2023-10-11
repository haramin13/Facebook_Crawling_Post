from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import sys
import os
from time import sleep
import datetime
import utils
import random

CHROMEDRIVER_PATH = 'chromedriver.exe'

class CollectPosts():
    """Collector of recent FaceBook posts.
           Note: We bypass the FaceBook-Graph-API by using a 
           selenium FireFox instance! 
           This is against the FB guide lines and thus not allowed.

           USE THIS FOR EDUCATIONAL PURPOSES ONLY. DO NOT ACTAULLY RUN IT.
    """

    def __init__(self, ids=["oxfess"], file="posts", depth=5, delay=random.randint(5,10)):
        self.ids = ids
        self.out_file = file
        self.depth = depth + 1
        self.delay = delay
        chrome_options = Options()
        # browser instance
        # chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('disable-infobars')
        chrome_options.add_argument('--disable-gpu') if os.name == 'nt' else None  # Windows workaround
        chrome_options.add_argument("--verbose")
        chrome_options.add_argument("--no-default-browser-check")
        chrome_options.add_argument("--ignore-ssl-errors")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--disable-feature=IsolateOrigins,site-per-process")
        chrome_options.add_argument("--no-first-run")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-translate")
        chrome_options.add_argument("--ignore-certificate-error-spki-list")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--disable-blink-features=AutomationControllered")
        chrome_options.add_experimental_option('useAutomationExtension', False)
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument("--start-maximized")  # open Browser in maximized mode
        chrome_options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        chrome_options.add_argument('disable-infobars')
        self.browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=chrome_options)
        # self.browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH)

    def collect_page(self, page):
        t_start = datetime.datetime.now()
        utils.create_csv(page)
        # navigate to page
        self.browser.get(
            'https://www.facebook.com/' + page)

        sleep(10)
        wait = WebDriverWait(self.browser, 20)
        action = ActionChains(self.browser)
        # wait.until(EC.element_to_be_clickable(By.XPATH, "//div[@aria-label='Close chat']")).click()
        # close_chat.click()

        t_posts = []

        for scroll in range(self.depth):
            if scroll % 10 == 0:
                print("Scroll times: ", scroll)
            links = self.browser.find_elements(By.XPATH, "//div[text()='See more']")
            for link in links:
                try:
                    action.move_to_element(link).perform()
                    wait.until(EC.element_to_be_clickable(link)).click()
                except:
                    continue

            posts = self.browser.find_elements(By.XPATH, "//div[@data-ad-preview='message']")
            for post in posts:
                t_posts.append(post.text)

            sleep(15)

            # Scroll down to bottom
            self.browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            # self.browser.execute_script(
            #     "arguments[0].scrollIntoView();", posts[-1])

            # Wait to load page
            sleep(10)

        links = self.browser.find_elements(By.XPATH, "//div[text()='See more']")
        for link in links:
            try:
                action.move_to_element(link).perform()
                wait.until(EC.element_to_be_clickable(link)).click()
            except:
                continue
        
        posts = self.browser.find_elements(By.XPATH, "//div[@data-ad-preview='message']")
        for post in posts:
            t_posts.append(post.text)

        idx = 1
        for post in t_posts:
            if (post != "") and ("See more" not in post):
                analysis=[idx]

                # Creating post text entry
                status = utils.strip(post)
                analysis.append(status)
                # print(post)

                # Write row to csv
                utils.write_to_csv(page, analysis)
                # Write raw data to txt
                utils.write_to_txt(page, post, idx)
                idx = idx + 1

        t_end = datetime.datetime.now()
        log_info = "Total posts scraped from " + page + " are: " + str(idx - 1) + "\nPosts are start scraped at: " + str(t_start) + " and finish at: " + str(t_end) + '\n' + '*'*30 + '\n'
        print(log_info)
        utils.write_log_file(log_info)


    def collect(self, typ):
        if typ == "pages":
            utils.create_log_file()
            for iden in self.ids:
                self.collect_page(iden)
        self.browser.close()

    def safe_find_element_by_id(self, elem_id):
        try:
            return self.browser.find_element(By.ID, elem_id)
        except NoSuchElementException:
            return None

    def login(self, email, password):
        try:

            self.browser.get("https://www.facebook.com")
            self.browser.maximize_window()

            # filling the form
            self.browser.find_element(By.ID, "email").send_keys(email)
            self.browser.find_element(By.ID, "pass").send_keys(password)

            # time.sleep(self.delay)

            # sys.exit()

            # clicking on login button
            self.browser.find_element(By.NAME, 'login').click()

            sleep(self.delay)
            
            # sys.exit()

        except Exception as e:
            print("There was some error while logging in.")
            print(sys.exc_info()[0])
            exit()

    def checkLiveClone(self):
        try:
            self.browser.get("https://www.facebook.com/")
            sleep(2)
            self.browser.get("https://www.facebook.com/")
            sleep(1)
            elementLive = self.browser.find_elements(By.XPATH, '//a[contains(@href, "/messages/")]')
            if (len(elementLive) > 0):
                return True

            return False
        except:
            print("Check Live Fail")


    def convertToCookie(self, cookie):
        try:
            new_cookie = ["c_user=", "xs="]
            cookie_arr = cookie.split(";")
            for i in cookie_arr:
                if i.__contains__('c_user='):
                    new_cookie[0] = new_cookie[0] + (i.strip() + ";").split("c_user=")[1]
                if i.__contains__('xs='):
                    new_cookie[1] = new_cookie[1] + (i.strip() + ";").split("xs=")[1]
                    if (len(new_cookie[1].split("|"))):
                        new_cookie[1] = new_cookie[1].split("|")[0]
                    if (";" not in new_cookie[1]):
                        new_cookie[1] = new_cookie[1] + ";"

            conv = new_cookie[0] + " " + new_cookie[1]
            if (conv.split(" ")[0] == "c_user="):
                return
            else:
                return conv
        except:
            print("Error Convert Cookie")


    def checkLiveCookie(self, cookie):
        try:
            self.browser.get('https://www.facebook.com/')
            self.browser.maximize_window()
            sleep(1)
            self.browser.get('https://www.facebook.com/')
            sleep(2)
            self.loginFacebookByCookie(cookie)

            return self.checkLiveClone()
        except:
            print("check live fail")


    def loginFacebookByCookie(self, cookie):
        try:
            cookie = self.convertToCookie(cookie)
            print(cookie)
            if (cookie != None):
                script = 'javascript:void(function(){ function setCookie(t) { var list = t.split("; "); console.log(list); for (var i = list.length - 1; i >= 0; i--) { var cname = list[i].split("=")[0]; var cvalue = list[i].split("=")[1]; var d = new Date(); d.setTime(d.getTime() + (7*24*60*60*1000)); var expires = ";domain=.facebook.com;expires="+ d.toUTCString(); document.cookie = cname + "=" + cvalue + "; " + expires; } } function hex2a(hex) { var str = ""; for (var i = 0; i < hex.length; i += 2) { var v = parseInt(hex.substr(i, 2), 16); if (v) str += String.fromCharCode(v); } return str; } setCookie("' + cookie + '"); location.href = "https://www.facebook.com"; })();'
                self.browser.execute_script(script)
                sleep(5)
        except:
            print("loi login")