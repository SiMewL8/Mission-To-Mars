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
    
    # pylint: disable=unbalanced-tuple-unpacking
    # news_title, news_teaser_sum, news_date = mars_news(browser)
    news_title, news_teaser_sum = mars_news(browser)  

    # Runs all separate scraping functions and stores results in a dictionary
    mars_total_data = {
        "news_title" : news_title,
        "news_paragraph_summary" : news_teaser_sum,
        # "news_latest_date" : news_date,
        # "news_latest_link" : latest_art_link,
        "featured_image" : featured_image(browser),
        "facts" : mars_facts(),
        "img_and_url": get_url(browser),
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

        # news_date = slide_elem.find('div',class_='list_date').get_text()

        # latest_art_link = f"https://mars.nasa.gov{slide_elem.select_one('ul li a').get('href')}"

        # Use the parent element to find the paragraph text
        news_teaser_sum = slide_elem.find('div',class_='article_teaser_body').get_text()

    except AttributeError:

        return None, None

    # return news_title, news_teaser_sum, news_date, latest_art_link

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
    return mars_df.to_html(classes= "table")



# --------------------------------------------------------------------------------------------------------------------------------
#                                       Mars Hemispheres
# --------------------------------------------------------------------------------------------------------------------------------

def get_url(browser):

    hemis_search_list = ['Cerberus Hemisphere Enhanced',
                     'Schiaparelli Hemisphere Enhanced',
                     'Syrtis Major Hemisphere Enhanced',
                     'Valles Marineris Hemisphere Enhanced']

    names_n_url = []

    Hemisphere = "Hemisphere"

    Urlid = "URL"

    for x in range(len(hemis_search_list)):
    
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

        browser.visit(url)
    
        try:

            browser.is_element_present_by_text((f'{hemis_search_list[x]}'), wait_time=2)
    
            hemi_click = browser.links.find_by_partial_text(f'{hemis_search_list[x]}')
    
            hemi_click.click()
    
            parse_html = browser.html

            hemi_parse_html = soupy(parse_html, 'html.parser' )
        
            hemi_img_url = hemi_parse_html.select_one('ul li a').get("href")
        
            names_n_url.append({Hemisphere:hemis_search_list[x],Urlid:hemi_img_url})

        except IndexError:

            return f"Search result not found"

        except AttributeError:

            return None

    # df_hemi_urls = pd.DataFrame.from_dict(names_n_url, orient='columns')

    # df_hemi_urls.set_index('Hemisphere', inplace=True)
    
    # df_hemi_urls['URL']=str(df_hemi_urls['URL'])  

    # pd.set_option('display.max_colwidth', -1)

    return names_n_url



if __name__ == "__main__":

    # if running as script, print scraped data

    print(scrape_all())