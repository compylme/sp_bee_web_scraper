from flask import Flask
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers.functions import insert_letters_db, remove_spaces, myTimezones
import chromedriver_binary
import uuid
import logging

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG) 
stream_handler = logging.StreamHandler()
app.logger.addHandler(stream_handler)


daily_letters = "spellingbee-letters-docker"
date = myTimezones.anchorageTime()
myTimestamp = myTimezones.timeStamp()

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

        url ="https://www.nytimes.com/date/crosswords/spelling-bee-forum.html"
        formatted_url = url.replace("date", date)

        driver.get(formatted_url)
        try: 
            anagram_letters = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR,"article.css-1vxca1d.e1lmdhsb0 section.meteredContent.css-1r7ky0e:nth-child(4) section.interactive-content.interactive-size-medium.css-14l1964 div.css-17ih8de.interactive-body div:nth-child(4) p.content:nth-child(2) > span:nth-child(2)")))
            mandatory_letter = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR,"article.css-1vxca1d.e1lmdhsb0 section.meteredContent.css-1r7ky0e:nth-child(4) section.interactive-content.interactive-size-medium.css-14l1964 div.css-17ih8de.interactive-body div:nth-child(4) p.content:nth-child(2) > span:nth-child(1)")))
            anagram_letters_value = anagram_letters.get_attribute("textContent")
            mandatory_letter_value = mandatory_letter.get_attribute("textContent")

            stripped_anagram = remove_spaces(anagram_letters_value)
            stripped_mandatory = remove_spaces(mandatory_letter_value)

            print("The letters have been scraped")

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
    finally:
        driver.quit()

letter_dictionary = scraper()
anagram,mandatory = letter_dictionary.values()
payload_data = {"timestamp": myTimestamp , "letters": anagram, "mandatory": mandatory}
insert_letters_db(daily_letters, payload_data, doc_id)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)