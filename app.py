from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from DataPipelines.Facebook.FacebookSeleniumUploader import FacebookSeleniumUploader, SeleniumSessionBuilder
from DataPipelines.Facebook.ImageDownloader import ImageDownloader
import csv
#selenium_uploader = SeleniumSessionBuilder().set_headless().build()

options = webdriver.ChromeOptions()
# options.add_argument("--headless")

driver = webdriver.Chrome(options=options)
image_downloader = ImageDownloader(driver, "ip.d@northeastern.edu", "D@n1el2004", "C:/Users/arcda/Documents/hostu_listing_images")

image_downloader.login()
# image_downloader.download_image("https://hostu-listings.nyc3.cdn.digitaloceanspaces.com/f9r0cd6g6dzz6mwgm1vrr2tn/vtg3vfxvbdu7h6a7m8favohn", "hostu-logo-1.png", "listing_1")

# print(image_downloader.get_image_details("tjb9rocemrv9xwdkypzdlxrt#8c0d3905-a4e2-4f57-ab39-41b6fafd4c6d"))

# image_downloader.retrieve_and_download_images("tjb9rocemrv9xwdkypzdlxrt#8c0d3905-a4e2-4f57-ab39-41b6fafd4c6d")

listing_ids = []

with open("data/master-excel-11-18-2024.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        listing_ids.append(row["listingId"])

print(listing_ids)

image_downloader.download_all_images(listing_ids)