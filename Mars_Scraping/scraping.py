# --------------------------------------------------------------------------------------------------------------------------------
#                                       Imports and Executables 
# --------------------------------------------------------------------------------------------------------------------------------
from splinter import Browser

from bs4 import BeautifulSoup as soupy

import pandas as pd

import datetime as dt




# --------------------------------------------------------------------------------------------------------------------------------
#                                       Gathered Data 
# --------------------------------------------------------------------------------------------------------------------------------

def scrape_all():

    # Set the executable path and initialize the chrome browser in splinter
    browser = Browser('chrome', **{'executable_path':'chromedriver'}, headless=True)
    # headless = True, doesnt show automated script in action
    
    news_title, news_teaser_sum = mars_news(browser) 

    # Runs all separate scraping functions and stores results in a dictionary
    mars_total_data = {
        "news_title" : news_title,
        "news_paragraph_summary" : news_teaser_sum,
        "featured_image" : featured_image(browser),
        "facts" : mars_facts(),
        "last_modified" : dt.datetime.now()}

    browser.quit()

    return mars_total_data


# --------------------------------------------------------------------------------------------------------------------------------
#                                       News Title and Paragraph
# --------------------------------------------------------------------------------------------------------------------------------

def mars_news(browser):
# defined outside of the function, basically a catalyst to get the function started, like a grandfather variable
# browser function already defined outside  

    # Visit the mars nasa news site
    nasa_url = 'https://mars.nasa.gov/news/'

    browser.visit(nasa_url)

    # optional delay for loading page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    parse_html = browser.html

    news_soup = soupy(parse_html, 'html.parser')

   
    try:
    # add error handling, espescially for AttributeErros with try/except
    # if error, code will keep running, except it will stop when its AttributeError with none returned
        
        slide_elem = news_soup.select_one('ul.item_list li.slide') # parent element, holds other elements to furthur filter

        # Use the parent element to find the first a tag and save it as `news_title`
        news_title = slide_elem.find('div',class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_teaser_sum = slide_elem.find('div',class_='article_teaser_body').get_text()

    except AttributeError:

        return None, None

    return news_title, news_teaser_sum

# --------------------------------------------------------------------------------------------------------------------------------
#                                       JPL Featured Space Image
# --------------------------------------------------------------------------------------------------------------------------------

# Visit URL
def featured_image(browser):

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

    try:

        # find the relative image url
        latest_image_full = full_img_soup.select_one('figure.lede a img').get("src")

    except AttributeError:

        return None

    # Use the base url to create an absolute url
    latest_imgurl = f"https://www.jpl.nasa.gov{latest_image_full}"

    return latest_imgurl 

# --------------------------------------------------------------------------------------------------------------------------------
#                                       Mars Fact Table
# --------------------------------------------------------------------------------------------------------------------------------

def mars_facts():

    try:
        
        mars_df = pd.read_html('https://space-facts.com/mars/')[0]

    except BaseException:
    # covers all exception errors 

        return None

    # Assign columns and set index of dataframe
    mars_df.columns = ['Description', 'Mars'] # adds column names

    mars_df.set_index('Description', inplace=True) # set column index

    # Convert dataframe into HTML format, add bootstrap
    return mars_df.to_html(classes= "table table-striped")


if __name__ == "__main__":

    # if running as script, print scraped data

    print(scrape_all())