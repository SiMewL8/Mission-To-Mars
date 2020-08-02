from splinter import Browser

from bs4 import BeautifulSoup as soupy

import pandas as pd

# Set the executable path and initialize the chrome browser in splinter
browser = Browser('chrome', **{'executable_path':'chromedriver'})

# Visit the mars nasa news site
nasa_url = 'https://mars.nasa.gov/news/'

browser.visit(nasa_url)

# optional delay for loading page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

# Convert the browser html to a soup object and then quit the browser
parse_html = browser.html

news_soup = soupy(parse_html, 'html.parser')

slide_elem = news_soup.select_one('ul.item_list li.slide') # parent element, holds other elements to furhtur filter

slide_elem.find('div', class_='content_title')

# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div',class_='content_title').get_text()

news_title

# Use the parent element to find the paragraph text
news_teaser_sum = slide_elem.find('div',class_='article_teaser_body').get_text()

news_teaser_sum

# ## JPL Space Images Featured Image
 
# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')

full_image_elem.click()

# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)

more_info_elem = browser.links.find_by_partial_text('more info')

more_info_elem.click()

# Parse the resulting html with soup
parse_html = browser.html

full_img_soup = soupy(parse_html, 'html.parser' )

# find the relative image url
latest_image_full = full_img_soup.select_one('figure.lede a img').get("src")

# Use the base url to create an absolute url
latest_imgurl = f"https://www.jpl.nasa.gov{latest_image_full}"

latest_imgurl 


# ## Mars Facts

mars_df = pd.read_html('https://space-facts.com/mars/')[0]

mars_df.columns = ['Description', 'Mars'] # adds column names

mars_df.set_index('Description', inplace=True) # set column index

mars_df

mars_df.to_html()

browser.quit()
