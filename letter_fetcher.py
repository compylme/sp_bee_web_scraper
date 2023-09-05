from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime

current_date = datetime.date.today()
formatted_date = str(current_date).replace("-", "/")

url ="https://www.nytimes.com/date/crosswords/spelling-bee-forum.html"
formatted_url = url.replace("date", formatted_date)
driver = webdriver.Chrome()

driver.get(formatted_url)



anagram_letters = driver.find_element(By.CSS_SELECTOR,"article.css-1vxca1d.e1lmdhsb0 section.meteredContent.css-1r7ky0e:nth-child(4) section.interactive-content.interactive-size-medium.css-14l1964 div.css-17ih8de.interactive-body div:nth-child(4) p.content:nth-child(2) > span:nth-child(2)")
mandatory_letter = driver.find_element(By.CSS_SELECTOR,"article.css-1vxca1d.e1lmdhsb0 section.meteredContent.css-1r7ky0e:nth-child(4) section.interactive-content.interactive-size-medium.css-14l1964 div.css-17ih8de.interactive-body div:nth-child(4) p.content:nth-child(2) > span:nth-child(1)")
anagram_letters_value = anagram_letters.get_attribute("textContent")
mandatory_letter_value = mandatory_letter.get_attribute("textContent")



print("Value:", str(anagram_letters_value))
print("Mandatory:", str(mandatory_letter_value))
