from bs4 import BeautifulSoup
from gtts import gTTS
from matplotlib.pyplot import text
import pandas as pd
import requests
import urllib.request
import time
import os


class Quote():
    def __init__(self, quote, author_name, book_name) -> None:
        self.quote = quote
        self.author_name = author_name
        self.book_name = book_name

    def format(self):
        '''formats quotes object for audio to prounounce '''
        return f'{self.quote}\n{self.author_name}{" " + self.book_name if self.book_name else ""}.\n' # note that the end point is to pause when reading 
		# voice stops at stop points not lines 


def text_to_voice(text, text_lang='en', accent='co.uk', audio_file_name='text.mp3', Fast = True):
    speech = gTTS(text, lang=text_lang, tld=accent, slow= not Fast)
    # speech = gTTS(text = text, lang = language, slow = False)
    speech.save(audio_file_name)


def scrape_website(URL, page_number=''):
    page_num = str(page_number)  # Convert the page number to a string
    URL = URL + \
        page_num  # append the page number to complete the URL
    webpage = requests.get(URL)  # Make a request to the website

    # Create lists to store the scraped data
    authors = []
    quotes = []
    # Parse the text from the website
    soup = BeautifulSoup(webpage.text, "html.parser")
    quoteText = soup.select('.quoteText')  # Get the tag and it's class
    # quoteText = soup.find_all('div', attrs={'class':'quoteText'}) #Get the tag and it's class
    for i in quoteText:
        # Get the text of the current quote, but only the sentence before a new line
        quote = i.text.strip().split('\n')[0]
        author = i.find('span', attrs={'class': 'authorOrTitle'}).text.strip()
        book_name = ''
        try:
            book_name = i.find(
                'a', attrs={'class': 'authorOrTitle'}).text.strip()
        except:
            pass
        quotes.append(Quote(quote, author, book_name))
    return quotes


link = input('Link: ')
if not link:
    link = 'https://www.goodreads.com/author/quotes/3137322.Fyodor_Dostoevsky'

quotes = scrape_website(link)

quotes_text = ''.join(quotes)
text_to_voice(quotes_text)
os.system('start text.mp3')
