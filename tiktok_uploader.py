from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set the path to your ChromeDriver executable
import os

# Set the path to your ChromeDriver executable
chromedriver_path = 'C:\x\chromedriver.exe'

# Set the paths for the video and title files
output_folder = 'output_folder'
titles_folder = 'titles_folder'

# Configure Chrome options to emulate a mobile device
mobile_emulation = {
    'deviceName': 'iPhone X'
}
chrome_options = Options()
chrome_options.add_experimental_option('mobileEmulation', mobile_emulation)

# Initialize the ChromeDriver instance with the specified options
driver = webdriver.Chrome(chromedriver_path, options=chrome_options)

# Open TikTok's mobile web interface in the browser
driver.get('https://m.tiktok.com/')

# Loop through the videos in the output folder
for file_name in os.listdir(output_folder):
    if file_name.endswith('.mp4'):
        # Get the corresponding title and description
        video_number = file_name.split('_')[0].replace('script', '')
        title_file = f"{titles_folder}/{video_number}.txt"
        with open(title_file, 'r') as f:
            title, description = f.read().splitlines()

        # Find and interact with the video upload elements
        upload_button = driver.find_element(By.CSS_SELECTOR, 'button.upload-button')
        upload_button.click()

        title_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input.title-input')))
        title_field.send_keys(title)

        description_field = driver.find_element(By.CSS_SELECTOR, 'textarea.description-textarea')
        description_field.send_keys(description)

        # Simulate file upload by sending the file path to the input element
        file_input = driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
        file_input.send_keys(os.path.join(output_folder, file_name))

        # Wait for the upload to finish
        WebDriverWait(driver, 120).until(EC.url_contains('/upload/success'))

        # Clear the fields for the next upload
        title_field.clear()
        description_field.clear()

# Close the browser
driver.quit()
