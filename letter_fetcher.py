from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime

def scraper():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)


    current_date = datetime.date.today()
    formatted_date = str(current_date).replace("-", "/")

    url ="https://www.nytimes.com/date/crosswords/spelling-bee-forum.html"
    formatted_url = url.replace("date", formatted_date)
    driver = webdriver.Chrome()

    driver.get(formatted_url)


    try: 
        anagram_letters = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR,"article.css-1vxca1d.e1lmdhsb0 section.meteredContent.css-1r7ky0e:nth-child(4) section.interactive-content.interactive-size-medium.css-14l1964 div.css-17ih8de.interactive-body div:nth-child(4) p.content:nth-child(2) > span:nth-child(2)")))
        mandatory_letter = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR,"article.css-1vxca1d.e1lmdhsb0 section.meteredContent.css-1r7ky0e:nth-child(4) section.interactive-content.interactive-size-medium.css-14l1964 div.css-17ih8de.interactive-body div:nth-child(4) p.content:nth-child(2) > span:nth-child(1)")))
        anagram_letters_value = anagram_letters.get_attribute("textContent")
        mandatory_letter_value = mandatory_letter.get_attribute("textContent")
        
        return {
            "anagram_letters": anagram_letters_value,
            "mandatory_letter": mandatory_letter_value
    }
    finally:
        driver.quit()




def lambda_handler(event, context):
    result = scraper()
    return result


if __name__ == "__main__":
    print(lambda_handler(None, None))