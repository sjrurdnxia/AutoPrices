import time
from selenium import webdriver

from selenium.webdriver.common.by import By

import xml.etree.ElementTree as ET
from selenium.webdriver.common.keys import Keys
tree = ET.parse(r'C:\Users\funny\Downloads\Booking\hotels.xml')
mytree = tree.getroot()
hotels_data = []

for listing in mytree.findall('listing'):
    name = listing.find('name').text
    address = listing.find(".//component[@name='addr1']").text
    checkin = listing.find(".//component[@name='Checkin']").text
    checkout = listing.find(".//component[@name='Checkout']").text
    adults = int(listing.find(".//component[@name='Adults']").text)

    hotel_info = {
        'name': name,
        'address': address,
        'checkin': checkin,
        'checkout': checkout,
        'adults': adults
    }

    hotels_data.append(hotel_info)

for hotel in hotels_data:
    print("Hotel Name:", hotel['name'])
    print("Address:", hotel['address'])
    print("Check-in Date:", hotel['checkin'])
    print("Check-out Date:", hotel['checkout'])
    print("Number of Adults:", hotel['adults'])
    print("----")

iday = int(checkin[8:])
print(iday)
oday = int(checkout[8:])
print(oday)












# driver = webdriver.Chrome()
# driver.maximize_window()

# test_url = 'https://www.booking.com/hotel/us/bellagio.html?aid=304142&label=gen173nr-1FCAEoggI46AdIM1gEaIkCiAEBmAExuAEXyAEM2AEB6AEB-AECiAIBqAIDuAKIs4-nBsACAdICJDVkMjk0YTgyLTlmZmEtNGI1Yi05NmFjLWJmMDRlOTM3MzZmZtgCBeACAQ&sid=b66f9ff2fe1db0a87c0f945a9cf3908e&dest_id=1704;dest_type=district;dist=0;group_adults=2;group_children=0;hapos=1;hpos=1;no_rooms=1;req_adults=2;req_children=0;room1=A%2CA;sb_price_type=total;sr_order=popularity;srepoch=1692653974;srpvid=5971984b405c00fe;type=total;ucfs=1&#hotelTmpl'
# driver.get(test_url)
# time.sleep(3)

# element = driver.find_element(By.XPATH,"//span[@class='xp__guests__count']")

# adults = int(element.text.split("group_adults")[0])
# print(adults)



