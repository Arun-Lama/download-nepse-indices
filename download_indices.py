import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from read_write_google_sheet import read_google_sheet, write_to_google_sheet
from datetime import timedelta
from selenium.webdriver.support.ui import Select



def download_indices(sheet_id):
    # Load existing sheet data to determine scraping range
    data = read_google_sheet(sheet_id)
    data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d', errors='coerce')
    data.sort_values(by='Date', ascending=True, inplace=True)

    if data['Date'].dropna().empty:
        print("[WARNING] No valid dates found in sheet. Defaulting to 30 days back.")
        date_to_start_scraping_from = pd.to_datetime("today") - timedelta(days=30)
    else:
        latest_data_available = data['Date'].dropna().iloc[-1]
        date_to_start_scraping_from = latest_data_available + timedelta(days=1)

    today = pd.to_datetime("today").normalize()
    dates = pd.date_range(start=date_to_start_scraping_from, end=today)
    dates = [d for d in dates if d.isoweekday() not in [5, 6]]

    if not dates:
        print("No dates to scrape — all within weekend range.")
        driver.quit()
        return pd.DataFrame()

    print(f"Downloading indices data from {dates[0].strftime('%Y-%m-%d')} to {dates[-1].strftime('%Y-%m-%d')}")

    sharesansar_sectors = [
        'Nepse Index', 'Banking SubIndex', 'Development Bank Index', 'Finance Index',
        'Hotels And Tourism', 'HydroPower Index', 'Investment', 'Life Insurance',
        'Manufacturing And Processing', 'Microfinance Index', 'Mutual Fund',
        'Non Life Insurance', 'Others Index', 'Trading Index'
    ]

    # Setup Chrome options to run headless and disable images
    options = Options()
    options.add_argument("start-maximized")
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")  # Disable GPU acceleration
    options.add_argument("--no-sandbox")  # Bypass OS security model
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    options.add_argument("window-size=1920,1080")  # Set the window size for consistency
    
    # Disable images
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), Options=Options)
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager(driver_version="137.0.7151.40").install()), options=options)
    driver.get('https://www.sharesansar.com/index-history-data')
    # Set date range
    driver.find_element(By.ID, 'fromDate').clear()
    driver.find_element(By.ID, 'fromDate').send_keys(f"{dates[0].date()}")
    driver.find_element(By.ID, 'toDate').clear()
    driver.find_element(By.ID, 'toDate').send_keys(f"{dates[-1].date()}")

    sectors_df = []

    for each_sector in sharesansar_sectors:
        try:
            # Select sector from dropdown
            driver.find_element(By.ID, "select2-index-container").click()
            driver.find_element(By.CSS_SELECTOR, "input.select2-search__field").send_keys(each_sector)
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".select2-results__option--highlighted"))
            ).click()

            # Submit form
            driver.find_element(By.ID, "btn_indxhis_submit").click()

            # Wait for table to load
            WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.ID, 'myTable_processing')))

            # Set pagination to 50
            dropdown = Select(driver.find_element(By.NAME, 'myTable_length'))
            dropdown.select_by_visible_text('50')
            WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.ID, 'myTable_processing')))

            # Determine number of pages
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            page_controls = soup.find(id='myTable_paginate').find('span')
            total_pages = len(page_controls.find_all('a')) if page_controls else 1

            output_rows = []

            for page in range(total_pages):
                if page > 0:
                    driver.find_element(By.XPATH, '//*[@id="myTable_next"]').click()
                    WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.ID, 'myTable_processing')))

                soup = BeautifulSoup(driver.page_source, 'html.parser')
                for row in soup.find_all('tr')[1:]:
                    columns = row.find_all('td')
                    if columns:
                        output_rows.append([col.text.strip() for col in columns])

            headers = [th.text.strip() for th in soup.find_all('th')]

            if output_rows:
                index_data = pd.DataFrame(output_rows, columns=headers)
                index_data.insert(0, 'Ticker', each_sector)
                index_data['Date'] = pd.to_datetime(index_data['Date'], errors='coerce')
                index_data.set_index('Date', inplace=True)

                cols_to_convert = index_data.columns.difference(['Ticker'])
                index_data[cols_to_convert] = index_data[cols_to_convert].replace(',', '', regex=True).astype(float)

                index_data = index_data.drop(columns=['S.N.', 'Change', 'Per Change (%)'], errors='ignore')
                sectors_df.append(index_data)
                print(each_sector)

        except Exception as e:
            print(f"[ERROR] Skipping sector {each_sector} due to error: {e}")
            continue

    driver.quit()

    if not sectors_df:
        print("Index Data is up to date. Nothing new to download.")
        return pd.DataFrame()

    daily_indices_data = pd.concat(sectors_df).reset_index()
    daily_indices_data['Date'] = pd.to_datetime(daily_indices_data['Date'], errors='coerce')
    daily_indices_data['Date'] = daily_indices_data['Date'].dt.strftime("%Y-%m-%d")
    daily_indices_data = daily_indices_data.sort_values(by = ['Date'], ascending= True)
    return daily_indices_data

indices_history_sheet_id = "1VvJsBXRGZ7sKRhGeHr-DCjnESjiYWsVm-A0ZIYG6en0"

indices_data = download_indices(indices_history_sheet_id)
write_to_google_sheet(indices_data, indices_history_sheet_id, mode= 'append')