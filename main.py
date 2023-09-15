from flask import Flask
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers.functions import insert_letters_db, remove_spaces
import datetime
import pytz
import chromedriver_binary
import uuid
import logging

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG) 
stream_handler = logging.StreamHandler()
app.logger.addHandler(stream_handler)


daily_letters = "spellingbee-letters-docker"
this_date = datetime.datetime.now()

doc_id = str(uuid.uuid4())

@app.route('/')
def scraper():
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=options)

        usEastTimezone = pytz.timezone('America/Anchorage')
        current_date = datetime.datetime.now(usEastTimezone)
        formatted_time = current_date.strftime("%Y/%m/%d")
        formatted_date = str(formatted_time).replace("-", "/")

        url ="https://www.nytimes.com/date/crosswords/spelling-bee-forum.html"
        formatted_url = url.replace("date", formatted_date)

        driver.get(formatted_url)
        try: 
            anagram_letters = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR,"article.css-1vxca1d.e1lmdhsb0 section.meteredContent.css-1r7ky0e:nth-child(4) section.interactive-content.interactive-size-medium.css-14l1964 div.css-17ih8de.interactive-body div:nth-child(4) p.content:nth-child(2) > span:nth-child(2)")))
            mandatory_letter = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR,"article.css-1vxca1d.e1lmdhsb0 section.meteredContent.css-1r7ky0e:nth-child(4) section.interactive-content.interactive-size-medium.css-14l1964 div.css-17ih8de.interactive-body div:nth-child(4) p.content:nth-child(2) > span:nth-child(1)")))
            anagram_letters_value = anagram_letters.get_attribute("textContent")
            mandatory_letter_value = mandatory_letter.get_attribute("textContent")

            stripped_anagram = remove_spaces(anagram_letters_value)
            stripped_mandatory = remove_spaces(mandatory_letter_value)

            return {
                "anagram_letters": stripped_anagram,
                "mandatory_letter": stripped_mandatory,  
            }
        except Exception as e:
            print("An error occured while scraping:", str (e))
        finally:
            driver.quit()
    except Exception as e:
        print("An error occureed while initializing the WebDriver:", str(e))
        return None

letter_dictionary = scraper()
anagram,mandatory = letter_dictionary.values()
payload_data = {"date": str(this_date) , "letters": anagram, "mandatory": mandatory}
    
if __name__ == '__main__':
    print("Running the main function", flush=True)
    app.run()
    print("Inserting the letters into the database", flush=True)
    try:
        insert_letters_db(daily_letters, payload_data, doc_id)
    except:
        print("An exception occured", flush=True)
    finally:
        print("The letters have been inserted into the database", flush=True)