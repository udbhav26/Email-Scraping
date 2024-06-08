import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Function to read search phrases from a file
def read_phrases(filename):
    phrases = []
    if os.path.isfile(filename):
        with open(filename, 'r') as file:
            phrases = file.readlines()
    return [phrase.strip() for phrase in phrases]

# Function to write search phrases to a file
def write_phrases(filename, phrases):
    with open(filename, 'a') as file:
        for phrase in phrases:
            file.write(phrase + '\n')

# Function to perform headless scraping
def headless_scrape(phrases, output_filename, max_pages=6):
    # Initialize already_searched_phrases as an empty list
    already_searched_phrases = []
    
    # Configure headless Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=chrome_options)
    
    # List to store URLs
    urls = []
    
    # Words to skip in URLs
    skip_words = ['google', 'youtube', 'quora', 'maps']
    
    # Function to filter out unwanted URLs
    def filter_urls(url):
        for word in skip_words:
            if word in url:
                return False
        return True
    
    # Loop through each search phrase
    for phrase in phrases:
        # Loop through multiple pages
        for page in range(1, max_pages + 1):
            # Generate Google search URL for the current page
            search_url = f"https://www.google.com/search?q={phrase.replace(' ', '+')}&start={(page - 1) * 10}"
            
            # Open Google search in headless browser
            driver.get(search_url)
            
            # Parse the HTML of search results
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            # Find all search result elements
            search_results = soup.find_all('a', href=True)
            
            # Extract URLs from search results
            for result in search_results:
                href = result['href']
                # Exclude unwanted URLs
                if href.startswith('http') and filter_urls(href):
                    urls.append(href)
        
        # Move the searched phrase to already_searched_phrases file
        already_searched_phrases.append(phrase)
        phrases.remove(phrase)
        write_phrases('already_searched_phrases.txt', already_searched_phrases)
        write_phrases('phrases.txt', phrases)
    
    # Close the browser
    driver.quit()
    
    # Write URLs to the output file (append mode)
    with open(output_filename, 'a') as file:
        for url in urls:
            file.write(url + '\n')


# Main function
def main():
    phrases = read_phrases('phrases.txt')
    already_searched_phrases = read_phrases('already_searched_phrases.txt')
    headless_scrape(phrases, 'output_urls.txt', max_pages=15)
    print("URLs scraped successfully!")

if __name__ == "__main__":
    main()




