from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait

class IMDB:
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.wait = WebDriverWait(self.driver, 20)

    def boot(self):
        """
        This method will open the Chrome web-browser with the URL passed.
        """
        self.driver.get(self.url)
        self.driver.maximize_window()
        self.wait.until(EC.url_to_be(self.url))

    def quit(self):
        """
        To quit the WebDriver session.
        """
        self.driver.quit()

    def FindElementByXpath(self, xpath):
        """
        Find an element by XPath.
        """
        return self.driver.find_element(by=By.XPATH, value=xpath)

    def FillTheData(self):
        """
        Fill the data in the IMDb search form.
        """
        try:
            self.boot()

            # click the name filter and then enter the name
            self.FindElementByXpath('//*[@id="nameTextAccordion"]').click()
            self.wait.until(EC.presence_of_element_located(
                (By.NAME, 'name-text-input'))).send_keys("Tom Hanks")

            # click the Birthday filter and enter the birthday
            self.FindElementByXpath('//*[@id="birthdayAccordion"]').click()
            self.wait.until(EC.presence_of_element_located(
                (By.NAME, 'birthday-input'))).send_keys("07-09")

            # click on the awards and recognition and then click - Best Actor-Winning.
            self.FindElementByXpath('//*[@id="awardsAccordion"]').click()
            self.wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="accordion-item-awardsAccordion"]/div/section/button[4]'))).click()

            # Wait for the "See Results" button to be clickable
            self.wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="__next"]/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/div[1]/button'))).click()

        except NoSuchElementException as e:
            print(f"The elements are not intractable as {e}")

    def searchresultUrl(self):
        """
        load the search results and get the current url of the web page

        """
        try:
            self.wait.until(EC.url_changes(self.url))
            search_url = self.driver.current_url
            print("Search Results URL:", search_url)
            return search_url
        except:
            print("The results are not loaded")
        finally:
            print("Details entered and search results are viewed")


if __name__ == "__main__":
    obj = IMDB("https://www.imdb.com/search/name/")
    obj.FillTheData()
    obj.searchresultUrl()
    obj.quit()


'''
    Output : 
    Current URL: https://www.imdb.com/search/name/?name=Tom%20Hanks&birth_monthday=07-09&groups=oscar_best_actor_winners
    Details entered and search results are viewed
'''
