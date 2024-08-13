import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def get_company_info_selenium(driver, url):
    data = {
        'company_name': "",
        'email': "",
        'website': "",
        'turnover': "",
        'employees': "",
        'town': ""
    }
    
    driver.get(url)
    # Close the cookie consent pop-up if it appears
    try:
        WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        ).click()
    except TimeoutException:
        pass

    # Extract the company name
    try:
        data['company_name'] = driver.find_element(By.CLASS_NAME, 'Profile__Name').text
    except NoSuchElementException:
        pass
    
    # Attempt to extract the email
    try:
        email_element = driver.find_element(By.CLASS_NAME, 'listing-email')
        data['email'] = email_element.get_attribute('href').replace('mailto:', '')
    except NoSuchElementException:
        pass

    # Attempt to extract the website URL
    try:
        website_element = driver.find_element(By.CLASS_NAME, 'listing-website-url')
        data['website'] = website_element.get_attribute('href')
    except NoSuchElementException:
        pass

    # Attempt to extract the town
    try:
        town_element = driver.find_element(By.XPATH, "//dt[contains(text(), 'Kotipaikka')]/following-sibling::dd/a")
        data['town'] = town_element.text
    except NoSuchElementException:
        pass

    # Wait for the upper bar chart to load and extract the last turnover value
    try:
        turnover_chart = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CLASS_NAME, "Financials__TurnoverChart"))
        )
        turnover_bars = turnover_chart.find_elements(By.CSS_SELECTOR, '.BarChart__Column')
        data['turnover'] = turnover_bars[-1].find_element(By.CSS_SELECTOR, '.BarChart__BarLabel').text
    except (NoSuchElementException, TimeoutException):
        pass

    # Extract number of employees
    try:
        employees_text = driver.find_element(By.XPATH, "//dt[contains(text(), 'Toimipaikan henkilöstöluokka')]/following-sibling::dd").text
        data['employees'] = employees_text.split('Lähde:')[0].strip()
    except NoSuchElementException:
        pass

    return data

# Set up the WebDriver for Firefox using Service
service = Service('C:\\Users\\...\\...\\...\\geckodriver.exe') #path must be edited
driver = webdriver.Firefox(service=service)

# List of URLs to process
urls = [
'',
    # ... other URLs
]

# This will hold all the company information
all_company_info = []

try:
    for url in urls:
        all_company_info.append(get_company_info_selenium(driver, url))
finally:
    driver.quit()

# Convert the list of dictionaries to a pandas DataFrame
df = pd.DataFrame(all_company_info)

# Check if DataFrame is not empty before saving to Excel
if not df.empty:
    # Define the path to save the Excel file on the desktop
    excel_path = #'example path'

    # Save the DataFrame to an Excel file on the desktop
    df.to_excel(excel_path, index=False)
    print(f"The Excel file was created successfully at {excel_path}.")
else:
    print("The DataFrame is empty. No Excel file was created.")
