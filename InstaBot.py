from selenium import webdriver
import BotEngine

chromedriver_path = r'PATH_TO_CHROMEDRIVE_EXECUTABLE'
webdriver = webdriver.Chrome(executable_path=chromedriver_path)

BotEngine.init(webdriver)
BotEngine.update(webdriver)

webdriver.close()
