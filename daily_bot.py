from os import system
from datetime import datetime as dt
import threading
from time import sleep
from selenium import webdriver, common
import configparser

StartUrl = str("https://www.snai.it/giochi/")

# configuration file (toml)
class BotConfiguration:
    Username = ""
    Password = ""
    Browser = ""

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.toml')
        self.Username = config['login']['username'].removeprefix('"').removesuffix('"')
        self.Password = config['login']['password'].removeprefix('"').removesuffix('"')
        self.Browser = config['system']['browser'].removeprefix('"').removesuffix('"')
    
    def getUsername(self):
        return self.Username

    def getPassword(self):
        return self.Password

    def getBrowser(self):
        return self.Browser

BotConfig = BotConfiguration()

# 
# Thread for the firefox driver
#
def RunFirefoxDriver():
    system("./geckodriver")

# 
# Thread for the chrome driver
#
def RunChromeDriver():
    system("./chromedriver")

#
# Function to spin
#
def Spin(driver: webdriver.Remote):
    print("Spinning")
    # click on the spin button
    driver.find_element("id", "contenitore_area_leva").click()
    sleep(10)

#
# Function to check if the daily spin is available
#
def CheckIFDailySpinAvaible(driver: webdriver.Remote):
    print("Checking if daily spin is available")

    # GOL.daily_spin.vince = 0 if i will not win
    if driver.execute_script("return GOL.daily_spin.vince") == 1:
        print("You will win")
    else:
        print("You will not win") 

    # TODO: check if the daily spin is available

    return True

# 
# Function to check if login was successful
#
def CheckLogin(driver: webdriver.Remote):
    if driver.current_url == "https://www.snai.it/user/login/error?destination=giochi":
        print("Login failed, probably wrong username or password")
        driver.quit()
        exit()
    else:
        print("Login successful")

#
# Function to login to the website and access the "daily" page
#
def AccessDailySpin(driver: webdriver.Remote):
    driver.get(StartUrl)
    # login
    driver.find_element("id", "accedi-button").click()

    # set edit-name
    name = driver.find_element("id", "edit-name")
    js = "arguments[0].value = '" + BotConfig.getUsername() + "';"
    driver.execute_script(js, name)
    # set edit-pass
    passwd = driver.find_element("id", "edit-pass")
    js = "arguments[0].value = '" + BotConfig.getPassword() + "';"
    driver.execute_script(js, passwd)
    # click on the login button
    login = driver.find_element("id", "edit-submit--2")
    js = "arguments[0].click();"
    driver.execute_script(js, login)
    # wait programatically 10 seconds
    sleep(10)

    # check if login succeeded
    CheckLogin(driver)

    # play the game
    driver.execute_script("openGamePopup(1516, 'giocaonline', 1024, 700, 0, 1, 'R2lhbGxvIC0gREFJTFkgU1BJTioqKmdpb2NoaSAtIEdpb2NoaU1haW5QYWdlKioqREFJTFlTUElOIC0gREFJTFlTUElOIC0gZ2lvY28=');")
    sleep(10)

if BotConfig.getBrowser() == "Chrome":
    capabilities = webdriver.DesiredCapabilities.CHROME
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

    # start chromedriver (another thread)
    x = threading.Thread(target=RunChromeDriver)
    x.start()
elif BotConfig.getBrowser() == "Firefox":
    capabilities = webdriver.DesiredCapabilities.FIREFOX
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')

    # start geckodriver (another thread)
    x = threading.Thread(target=RunFirefoxDriver)
    x.start()
else:
    print("Browser not supported")
    exit(1)

sleep(5)

first_time = True

while True:
    date_time = dt.now()
    # format as 24hrs
    date_time_str = date_time.strftime("%H:%M:%S")

    # check if a day has passed
    if (date_time.hour == 0 and date_time.minute == 0 and date_time.second >= 0) or (first_time == True):
        driver = webdriver.Remote(command_executor='http://127.0.0.1:4444', desired_capabilities=capabilities, options=options)
        
        first_time = False
        
        driver.get(StartUrl)
        AccessDailySpin(driver)

        # after that a new window will be opened with the game
        # we need to switch to that window
        found = False
        for handle in driver.window_handles:
            driver.switch_to.window(handle)
            if driver.current_url.startswith("https://www.snai.it/play/games/1516"):
                found = True

                # TODO: Mute the game

                break
            
        if found == False:
            print("Could not find the game window, aborting")
            exit(1)

        if CheckIFDailySpinAvaible(driver):
            print("Daily spin is available")

            Spin(driver)

        sleep(10) # wait 10 seconds before closing the window (spin time)

        # close the windows
        driver.quit()

