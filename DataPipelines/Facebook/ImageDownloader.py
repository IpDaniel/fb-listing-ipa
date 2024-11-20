import requests
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import html5lib
from time import sleep

class ImageDownloader:
    def __init__(self, driver, username, password, base_folder_path, base_url="https://joinhostu.com", default_action_delay=1):
        self.driver = driver
        self.base_url = base_url
        self.username = username
        self.password = password
        self.base_folder_path = base_folder_path
        self.default_action_delay = default_action_delay

    def login(self):
        self.driver.get(self.base_url + "/login")
        email = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="email"]')))
        email.send_keys(self.username)
        password = self.driver.find_element(By.CSS_SELECTOR, 'input[type="password"]')
        password.send_keys(self.password)
        print("Password sent in image downloader")
        login = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        print("Login button found in image downloader")
        login.click()
        print("Login button clicked in image downloader")
        sleep(self.default_action_delay)
    
    def download_image(self, image_url, filename, folder_name, download_path=None, file_extension="png"):
        """
        Downloads an image from a given URL and saves it to a specified path with a given filename.
        - Download path is the path to the folder where the image will be saved. It does not include the 
        filename or extension.
        - filename is the name of the file to be saved.
        - file_extension is the extension of the file to be saved. It does not include the period.
        """
        if download_path is None:
            download_path = self.base_folder_path

        
        os.makedirs(os.path.dirname(download_path), exist_ok=True)
        
        os.makedirs(os.path.join(download_path, folder_name), exist_ok=True)
        
        full_path = os.path.join(download_path, folder_name, filename + "." + file_extension)

        # Download the image
        response = requests.get(image_url)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Check if file already exists
        if os.path.exists(full_path):
            print(f"File {full_path} already exists, skipping download")
            return

        # Save the image to file
        with open(full_path, 'wb') as f:
            f.write(response.content)

    def download_images(self, image_urls, image_filenames, folder_name, download_path=None):
        if download_path is None:
            download_path = self.base_folder_path
        for image_url, filename in zip(image_urls, image_filenames):
            self.download_image(image_url=image_url, filename=filename, folder_name=folder_name, download_path=download_path)
    
    def get_image_details(self, listing_id):
        try:
            self.driver.get(self.base_url + "/app/listing/" + listing_id)
        except:
            raise RuntimeError(f"Could not find listing {listing_id}")
        sleep(self.default_action_delay)
        webdriver.ActionChains(self.driver).send_keys(webdriver.Keys.ESCAPE).perform()
        sleep(self.default_action_delay / 2)
        webdriver.ActionChains(self.driver).send_keys(webdriver.Keys.ESCAPE).perform()
        sleep(self.default_action_delay / 2)
        image_urls = []
        image_filenames = []
        folder_name = f"{listing_id}_images"
        show_photos_button = self.driver.find_element(By.XPATH, '//button[contains(text(), "Show all photos")]')
        show_photos_button.click()
        sleep(self.default_action_delay)
        iteration = 1
        while (True):
            image = self.driver.find_element(By.CSS_SELECTOR, 'img.max-h-full.max-w-full.object-contain')
            image_src = image.get_attribute('src')
            image_urls.append(image_src)
            image_filenames.append(f"{listing_id}_{iteration}.png")
            try:
                next_button = self.driver.find_element(By.CSS_SELECTOR, 'button.fixed.bottom-0.right-0')
            except:
                print("Could not find next button")
                break
            next_button.click()
            sleep(self.default_action_delay)
            iteration += 1
        return folder_name, image_urls, image_filenames
    
    def retrieve_and_download_images(self, listing_id):
        try:
            folder_name, image_urls, image_filenames = self.get_image_details(listing_id)
        except:
            raise RuntimeError(f"Could not retrieve and download images for listing {listing_id}")
        try:
            self.download_images(image_urls=image_urls, image_filenames=image_filenames, folder_name=folder_name)
        except:
            raise RuntimeError(f"Could not download images for listing {listing_id}")
    
    def download_all_images(self, listing_ids):
        for listing_id in listing_ids:
            try:
                self.retrieve_and_download_images(listing_id)
            except RuntimeError as e:
                print(f"Could not download images for listing {listing_id}: {e}")
                continue
