from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import xml.etree.ElementTree as ET
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from lxml import etree
class HotelScraper:
    WINDOW_SIZE = "1200,900"
    BASE_URL = "https://www.booking.com"
    
    def __init__(self, xml_data):
        self.xml_data = xml_data
        self.popup_closed = False
        self.date_already = False
        self.alert_found = False
        self.entered_people = False
    def _setup_driver(self):
        opts = Options()
        opts.add_argument('--headless=new')
        driver = webdriver.Chrome(opts)
        return driver
    
    def _parse_xml(self):
        root = ET.fromstring(self.xml_data)
        
        for listing in root.findall('listing'):
            name = listing.find('name').text
            checkin = listing.find('component[@name="Checkin"]').text
            checkout = listing.find('component[@name="Checkout"]').text
            adults = listing.find('component[@name="Adults"]').text
            yield name, checkin, checkout, adults
    
    def get_prices(self):
        driver = self._setup_driver()
        
        for hotel, checkin, checkout, adults in self._parse_xml():
            # Navigate to Booking.com
            driver.get(self.BASE_URL)
            time.sleep(5)
            if not self.popup_closed:
                try: 
                    close_popup = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Dismiss sign-in info.']")
                    close_popup.click()
                    self.popup_closed = True
                except:
                    pass
            # Fill the search bar with the hotel name
            search_input = driver.find_element(By.ID,':re:')
            search_input.send_keys(hotel)
            if not self.entered_people:
                    people = driver.find_element(By.XPATH,"//button[normalize-space()='2 adults · 0 children · 1 room']")
                    people.click()
                    if int(adults)>2:
                        click_times = int(adults)-2
                    else:
                        click_times=0
                    next_arrow = driver.find_element(By.XPATH,"//div[@data-capla-component-boundary='b-index-lp-web-mfe/SearchBoxDesktopHorizontal']//form//*[name()='svg']")
                    for i in range(click_times):
                        next_arrow.click()
                    self.entered_people = True
                
        # search_input.send_keys(Keys.ENTER)
            time.sleep(5)
            if not self.date_already:
                try:
                    date = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="date-display-field-end"]')
                    date.click()
                    time.sleep(2)
            
                    next_button = driver.find_element(By.CSS_SELECTOR,
                                            "button[class='a83ed08757 c21c56c305 f38b6daa18 d691166b09 f671049264 deab83296e f4552b6561 dc72a8413c f073249358']")
                    next_button.click()

                    inday = int(checkin.split('-')[-1])  # Extracting day from '2023-10-10' format
                    oday = int(checkout.split('-')[-1])
            
                    formatted_inday = f"{inday:02d}"
                    formatted_oday = f"{oday:02d}"
            
            
                    date_element_xpath = f"//span[contains(@aria-label, '{formatted_inday} October 2023')]"
                    date_element_xpatho = f"//span[contains(@aria-label, '{formatted_oday} October 2023')]"

                    checkin_date = driver.find_element(By.XPATH, date_element_xpath)
                    checkout_date = driver.find_element(By.XPATH, date_element_xpatho)

                    checkin_date.click()
                    checkout_date.click()
                    self.date_already=True
                    time.sleep(3)
                except:
                    pass
            search_input.send_keys(Keys.ENTER)
            time.sleep(5)
        # Extract data using BeautifulSoup

            if hotel=='Bellagio Las Vegas':
                try:
                    first_result = driver.find_element(By.XPATH,"//div[normalize-space()='Bellagio']")
                except:
                    print("Not Found")
                    continue
            
            elif hotel=='ARIA Resort And Casino':
                first_result = driver.find_element(By.XPATH,"//div[normalize-space()='ARIA Resort & Casino']")
            elif hotel =='Red Rock Casino, Resort and Spa':
                try:
                    first_result = driver.find_element(By.XPATH,"//div[normalize-space()='Red Rock Casino, Resort and Spa']")
                except:
                    print('Not Found')
                    continue
                
            elif hotel=='Trump International Hotel Las Vegas':
                first_result = driver.find_element(By.XPATH,"//div[normalize-space()='Trump International Hotel Las Vegas']")
        
            
            elif hotel=='NoMad Las Vegas':
                first_result = driver.find_element(By.XPATH,"//div[normalize-space()='NoMad Las Vegas']")
            elif hotel=='NoMad Las Vegas':
                first_result = driver.find_element(By.XPATH,"//div[normalize-space()='NoMad Las Vegas']")
            elif hotel =='The Venetian Resort Las Vegas':
                first_result = driver.find_element(By.XPATH,"//div[normalize-space()='The Venetian® Resort Las Vegas']")
            elif hotel =='Waldorf Astoria Las Vegas': 
                wait = WebDriverWait(driver, 10)
                first_result = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[normalize-space()='Waldorf Astoria Las Vegas']")))
        
            first_result.click()
            time.sleep(5)
            if not self.alert_found:
                try: 
                    driver.find_element(By.XPATH,"//span[@class='bui-alert__title']")
                    print('Not Available')
                    self.alert_found = True
                    continue
                except:
                    pass
            driver.switch_to.window(driver.window_handles[-1])
            soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        
        
        
            room_elements = soup.find_all('span', class_='hprt-roomtype-icon-link')[:3]
            price_elements = [elem for elem in soup.find_all('span', class_='bui-u-sr-only') if '$' in elem.text]

        # Ensure that the room and price lists have the same length
            min_length = min(len(room_elements), len(price_elements))

            rooms_and_prices = list(zip(
                [room.get_text(strip=True) for room in room_elements[:min_length]],
                [price.get_text(strip=True) for price in price_elements[:min_length]]
                ))

            print(f"Hotel: {hotel}")
            for room, price in rooms_and_prices:
                print(f"Room Type: {room}, {price}")
            print('-' * 50)
            
            driver.get(self.BASE_URL)
            time.sleep(5)
        print('Done')

if __name__ == "__main__":
    xml_data = """<?xml version="1.0" encoding="UTF-8"?>
<listing>
    <listing>
        <name>Bellagio Las Vegas</name>
        <component name="addr1">3600 Las Vegas Blvd S, Las VegasNevada 89109, Las Vegas, 89109, USA</component>
        <component name="Checkin">2023-10-10</component>
        <component name="Checkout">2023-10-14</component>
        <component name="Adults">4</component>
        <country>US</country>
    </listing>
    <listing>
        <name>ARIA Resort And Casino</name>
        <component name="addr1">3730 Las Vegas Blvd South, Las Vegas</component>
        <component name="Checkin">2023-10-10</component>
        <component name="Checkout">2023-10-14</component>
        <component name="Adults">2</component>
        <country>US</country>
    </listing>
    
    <listing>
        <name>Red Rock Casino, Resort and Spa</name>
        <component name="addr1">11011 W Charleston Blvd, Las Vegas</component>
        <component name="Checkin">2023-10-10</component>
        <component name="Checkout">2023-10-14</component>
        <component name="Adults">2</component>
        <country>US</country>
    </listing>
    
    <listing>
        <name>Trump International Hotel Las Vegas</name>
        <component name="addr1">2000 Fashion Show Drive, Las Vegas</component>
        <component name="Checkin">2023-10-10</component>
        <component name="Checkout">2023-10-14</component>
        <component name="Adults">2</component>
    </listing>
    
    <listing>
        <name>NoMad Las Vegas</name>
        <component name="addr1">3772 S Las Vegas Blvd, Las Vegas</component>
        <component name="Checkin">2023-10-10</component>
        <component name="Checkout">2023-10-14</component>
        <component name="Adults">2</component>
    </listing>
    
    <listing>
        <name>The Venetian Resort Las Vegas</name>
        <component name="addr1">3355 Las Vegas Blvd S, Las Vegas</component>
        <component name="Checkin">2023-10-10</component>
        <component name="Checkout">2023-10-14</component>
        <component name="Adults">2</component>
    </listing>
    
    <listing>
        <name>Waldorf Astoria Las Vegas</name>
        <component name="addr1">3752 Las Vegas Blvd S, Las Vegas</component>
        <component name="Checkin">2023-10-10</component>
        <component name="Checkout">2023-10-14</component>
        <component name="Adults">2</component>
    </listing>
</listing>"""
    scraper = HotelScraper(xml_data)
    scraper.get_prices()