import requests
import pyttsx3
from bs4 import BeautifulSoup
from click import MissingParameter
from gtts import gTTS
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
            quote = str(i).replace('<br>', '.')
            quote = self.remove_tags(quote)
            
            quotes.append(Quote(quote))
        self.page = Page(quotes, int(page_num))
        return self.page

    def remove_tags(self, html):
        '''
        removes html tags from str and returns str pure 
        '''
    # parse html content
        soup = BeautifulSoup(html, "html.parser")

        for data in soup(['style', 'script']):
            # Remove tags
            data.decompose()

        # return data by retrieving the tag content
        return ' '.join(soup.stripped_strings)


class Page():
    '''
    class for a goodreads page. contains quotes and functions to extract and use them. 
    '''

    def __init__(self, quotes, page_num) -> None:
        self.quotes = quotes

    def __str__(self) -> str:
        return self.format()
        self.page_num = page_num

    def say(self):
        '''
        says the text in the page using male voice
        '''
        text = self.format()
        input(text)
        
        converter = pyttsx3.init()
        # Sets speed percent
        # Can be more than 100
        converter.setProperty('rate', 150)
        converter.setProperty('volume', 1.200
                              )
        # Queue the entered text
        # There will be a pause between
        converter.say(text)
        converter.runAndWait()

    def format(self):
        '''
        format the quotes into one string, a.k.a a page of quotes.
        '''
        return '\n'.join([quote.format() for quote in self.quotes])

    def convert_to_mp3(self, audio_file_name='text.mp3', text_lang='en', accent='co.uk', Fast=True):
        '''
        converts the text passed to audio
        '''
        input(self.format())
        speech = gTTS(self.format(), lang=text_lang, tld=accent, slow=not Fast)
        speech.save(audio_file_name)
        return audio_file_name


class Quote():
    '''
    mainly used to take quotes parameters for it to be used in the format function
    '''

    def __init__(self, quote) -> None:
        self.quote = quote

    def format(self):
        '''formats quotes object for the audio to prounounce '''
        return f'{self.quote}.'  # note that the end point is to pause when reading
        # voice stops at stop points not lines.


link = input('Link: ')
scraper = Scraper(link)
print('scarping quotes..')
page = scraper.scrape_website()
print('reading quotes..')
page.say()
# print('converting to mp3..')
# rel_path = page.convert_to_mp3()
# print('starting file..')https://www.goodreads.com/author/quotes/875661.Rumi
