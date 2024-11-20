from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import html5lib
from time import sleep
from ..Base.Uploader import Uploader

class FacebookSeleniumUploader(Uploader):
    def __init__(self, home_url, email, password, driver, formatted_data, default_action_delay=1):
        self.email = email
        self.password = password
        self.driver = driver
        self.default_action_delay = default_action_delay
        self.home_url = home_url if home_url is not None else "https://www.facebook.com"
        if self.home_url != "https://www.facebook.com":
            raise RuntimeError("Home URL is usually supposed to be https://www.facebook.com")
        super().__init__(formatted_data)

    def login(self):
        """Logs into Facebook"""
        self.driver.get(self.home_url)
        email = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'email')))
        email.send_keys(self.email)
        password = self.driver.find_element('id', 'pass')
        password.send_keys(self.password)
        login = self.driver.find_element('name', 'login')
        login.click()
        sleep(3)

    def post_to_group(self, group_id, post_data, text_only=False):
        """Posts formatted data to a single Facebook group"""
        occurences = []
        try:
            # Navigate to group
            self.driver.get(f"https://www.facebook.com/groups/{group_id}")
            sleep(self.default_action_delay)

            # raise NotImplementedError("check here if the group is private and the user has not joined it")
            # raise NotImplementedError("check here if the user has been banned from the group")

            if text_only:
                # Find the "Write something..." button to create a text-only post
                try:
                    write_something = WebDriverWait(self.driver, self.default_action_delay).until(
                        EC.element_to_be_clickable((By.XPATH, "//*[text()='Write something...']"))
                    )
                    write_something.click()
                except Exception as e:
                    print(f"Error clicking 'Write something' button: {str(e)}")
                    occurences.append(f"error clicking 'Write something' button: {str(e)}")
                    raise e
                
                # Find and clear the text input, and input the post text
                try:
                    text_input = WebDriverWait(self.driver, self.default_action_delay).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, '.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x9f619.xzsf02u.xmper1u.xngnso2.xo1l8bm.x5yr21d.x1qb5hxa.x1a2a7pz.x1iorvi4.x4uap5.xwib8y2.xkhd6sd.xh8yej3.xha3pab'))
                    )
                    text_input.clear()
                    text_input.send_keys(post_data['text'])
                except Exception as e:
                    print(f"Error finding or interacting with text input: {str(e)}")
                    occurences.append(f"error finding or interacting with text input: {str(e)}")
                    raise e
                sleep(self.default_action_delay)

                # Find and click the "Post" button
                try:
                    post_button = WebDriverWait(self.driver, self.default_action_delay).until(
                        EC.element_to_be_clickable((By.XPATH, "//*[text()='Post']"))
                    )
                    post_button.click()
                except Exception as e:
                    print(f"Error clicking post button: {str(e)}")
                    occurences.append(f"error clicking post button: {str(e)}")
                    raise e
                sleep(self.default_action_delay)

                # raise NotImplementedError("Make sure to check here if the post was successful, or if it has to get approved")
            
                occurences.append(f"posted write-only post {post_data['text']}")
                return True, occurences
            
            # Find and click "Photo/video" button
            try:
                photo_video_button = WebDriverWait(self.driver, self.default_action_delay).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[text()='Photo/video']"))
                )
                photo_video_button.click()
            except Exception as e:
                print(f"Error clicking 'Photo/video' button: {str(e)}")
                occurences.append(f"error clicking 'Photo/video' button: {str(e)}")
                raise e
            sleep(self.default_action_delay)
            raise NotImplementedError("add the logic to upload the image")
        
            # Find and click the text input and input the post text
            try:
                text_input = WebDriverWait(self.driver, self.default_action_delay).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x9f619.xzsf02u.xmper1u.xo1l8bm.x5yr21d.x1a2a7pz.x1iorvi4.x4uap5.xwib8y2.xkhd6sd.xh8yej3.xha3pab.x6prxxf.xvq8zen'))
                )
                text_input.clear()
                text_input.send_keys(post_data['text'])
            except Exception as e:
                print(f"Error finding text input: {str(e)}")
                occurences.append(f"error finding text input: {str(e)}")
                raise e
            sleep(self.default_action_delay)

            # Find and click the "Post" button
            try:
                post_button = WebDriverWait(self.driver, self.default_action_delay).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "div[aria-label='Post']"))
                )
                post_button.click()
            except Exception as e:
                print(f"Error clicking post button: {str(e)}")
                occurences.append(f"error clicking post button: {str(e)}")
                raise e
            sleep(self.default_action_delay)

            raise NotImplementedError("Make sure to check here if the post was successful, or if it has to get approved")

            occurences.append(f"posted post {post_data['text']}")
            return True, occurences
            
        except TimeoutException as e:
            print(f"Timeout posting to group {group_id}: {str(e)}")
            return False, occurences
            
        except Exception as e:
            print(f"Error posting to group {group_id}: {str(e)}")
            return False, occurences

    def parse_data_for_post(self, data):
        """Formats data into a Facebook post"""
        raise NotImplementedError("This method may not be needed")

    def post_to_groups(self, group_ids, data):
        """Posts formatted data to multiple Facebook groups"""
        results = {}
        for group_id in group_ids:
            success, occurences = self.post_to_group(group_id, data)
            results[group_id] = success
            sleep(self.default_action_delay)
        return results

    def post_to_school_groups(self, school_name, group_data, data):
        """Posts to groups associated with a school name"""
        raise NotImplementedError("This method needs to have more known structure to be implemented")

    def close(self):
        self.driver.quit()

   

class SeleniumSessionBuilder:
    def __init__(self):
        self.headless = False
        self.driver = None
        self.default_action_delay = 1
        self.disable_notifications = True
        self.home_url = "https://www.facebook.com"
        self.formatted_data = None

    def set_formatted_data(self, formatted_data):
        self.formatted_data = formatted_data
        return self
        
    def set_headless(self):
        self.headless = True
        return self
    
    def unset_headless(self):
        self.headless = False
        return self
        
    def set_default_action_delay(self, delay):
        self.default_action_delay = delay
        return self
        
    def set_notifications(self, enabled):
        self.disable_notifications = not enabled
        return self
    
    def unset_notifications(self):
        self.disable_notifications = False
        return self
        
    def set_home_url(self, url):
        self.home_url = url
        return self
    
    def build(self):
        if self.formatted_data is None:
            raise ValueError("Formatted data not set")

        options = webdriver.ChromeOptions()
        
        if self.headless:
            options.add_argument('--headless')
            
        if self.disable_notifications:
            options.add_argument('--disable-notifications')
            
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(self.home_url)
        
        return FacebookSeleniumUploader(self.driver, self.formatted_data, self.default_action_delay)
