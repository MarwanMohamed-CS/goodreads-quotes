from operator import contains
from xdrlib import ConversionError
from bs4 import BeautifulSoup
from click import MissingParameter
from gtts import gTTS
import requests
import os
from re import search


class Scraper():
    def __init__(self, link='') -> None:
        self.link = link
        self.page = None

    def contains_page_num(self, link):
        '''
        returns true if it contains a page and False if not
        '''
        regx = search('page=\d', link)
        match = regx.group()
        if match:
            return True
        else:
            return False

    def scrape_website(self, link='', page_num=0):
        '''
        returns a page object that contains the quotes and their informaiton
        '''

        if not link:
            if self.link:
                link = self.link
            else:
                raise MissingParameter('No link is provided.')

        page_num = str(page_num)
        link = link + '?page=' + page_num
        webpage = requests.get(link)
        quotes = []
        soup = BeautifulSoup(webpage.text, "html.parser")
        quoteText = soup.select('.quoteText')  # Get the tag and it's class
        # quoteText = soup.find_all('div', attrs={'class':'quoteText'}) #Get the tag and it's class
        for i in quoteText:
            # Get the text of the current quote, but only the sentence before a new line
            quote = i.text.strip().split('\n')[0]
            author = i.find(
                'span', attrs={'class': 'authorOrTitle'}).text.strip()
            book_name = ''
            try:
                book_name = i.find(
                    'a', attrs={'class': 'authorOrTitle'}).text.strip()
            except:
                pass
            quotes.append(Quote(quote, author, book_name))
        self.page = Page(quotes, int(page_num))
        return self.page


class Page():
    def __init__(self, quotes, page_num) -> None:
        self.quotes = quotes
        self.page_num = page_num

    def format(self):
        '''
        format the quotes into one string, a.k.a a page of quotes.
        '''
        return ''.join([quote.format() for quote in self.quotes])

    def __str__(self) -> str:
        return self.format()

    def convert_to_mp3(self, audio_file_name='text.mp3', text_lang='en', accent='co.uk', Fast=True):
        '''
        converts the text passed to audio
        '''
        speech = gTTS(self.format(), lang=text_lang, tld=accent, slow=not Fast)
        speech.save(audio_file_name)
        return audio_file_name




class Quote():
    '''
    mainly used to take quotes parameters for it to be used in the format function
    '''

    def __init__(self, quote, author_name, book_name) -> None:
        self.quote = quote
        self.author_name = author_name
        self.book_name = book_name

    def format(self):
        '''formats quotes object for the audio to prounounce '''
        return f'{self.quote}\n{self.author_name}{" " + self.book_name if self.book_name else ""}.\n'  # note that the end point is to pause when reading
        # voice stops at stop points not lines.


link = input('Link: ')
scraper = Scraper(link)
print('scarping quotes..')
page = scraper.scrape_website()
print('converting to mp3..')
rel_path = page.convert_to_mp3()
print('starting file..')
os.system('start {}'.format(rel_path))
