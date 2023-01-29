from numpy import random

from selenium import webdriver
from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys

import time
import configparser
import os
counter = 0
def main():
    config_file = 'config.ini'

    # Create config file if it doesn't exist
    if not os.path.exists(config_file):
        with open(config_file, 'w') as f:
            f.write("[settings]\nstart_value = 5\nserver_id = \nchannel_id = \nbot_username = ")

    # Read config file
    config = configparser.ConfigParser()
    config.read(config_file)

    start_value = config.getint('settings', 'start_value')
    multiplier = config.getfloat('settings', 'multiplier')
    server_id = config.get('settings', 'server_id')
    channel_id = config.get('settings', 'channel_id')
    bot_username = config.get('settings', 'bot_username')
    time.sleep(1)
    # Validate config file
    while not all([start_value, server_id, channel_id, bot_username]):
        print("Config file is not valid. Please enter the required values.")
        start_value = input("Enter the start value (default 3): ") or 3
        multiplier = input("Enter the multiplier (default 2.5): ") or 2.5
        server_id = input("Enter the server id: ")
        channel_id = input("Enter the channel id: ")
        bot_username = input("Enter the bot's username: ")
        config.set('settings', 'start_value', start_value)
        config.set('settings', 'multiplier', multiplier)
        config.set('settings', 'server_id', server_id)
        config.set('settings', 'channel_id', channel_id)
        config.set('settings', 'bot_username', bot_username)
        with open(config_file, 'w') as configfile:
            config.write(configfile)

    # Continue with program
    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=C:\\Users\\lolpv\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

    driver.get("https://discord.com/app")

    # Wait for login

    wait = WebDriverWait(driver, 60)  # timeout after 10 seconds
    results = wait.until(lambda driver: driver.find_element_by_id('app-mount'))

    time.sleep(3)
    driver.get(f"https://discord.com/channels/{server_id}/{channel_id}")
    time.sleep(5)
    input_element = driver.find_element_by_xpath(
        '/html/body/div[1]/div[2]/div/div[1]/div/div[2]/div/div[1]/div/div/div[3]/div[2]/main/form/div/div[1]/div/div[3]/div/div[2]')

    usedmessages = []

    def typeMessage(startv, used, counter, mp):
        time.sleep(0.25)
        elem = input_element
        texts = ["/coin", "heads", str(int(startv))]
        counter += 1
        for text in texts:
            for character in text:
                actions = ActionChains(driver)
                actions.move_to_element(elem)
                actions.send_keys(character)
                actions.perform()
                time.sleep(random.uniform(0.02, 0.08))
            input_element.send_keys(Keys.ENTER)
            time.sleep(0.2)
        time.sleep(0.25)
        input_element.send_keys(Keys.ENTER)
        time.sleep(5)
        for message in reversed(driver.find_elements_by_class_name("messageListItem-ZZ7v6g")):
            if message.get_attribute("id") in used:
                print("used!")
                continue
            if message.find_element_by_class_name("username-h_Y3Us").get_attribute('innerHTML') == bot_username:
                msg = message.find_element_by_css_selector("article").get_attribute('innerHTML')
                if "Heads!" in msg:
                    # win
                    print("Won")
                    startv = config.getint('settings', 'start_value')
                elif "Tails!" in msg:
                    # lose
                    print("Lost")
                    startv *= mp
                used += message.get_attribute("id");
                break
        typeMessage(startv, usedmessages, counter, mp)

    typeMessage(start_value, usedmessages, counter, multiplier)


if __name__ == "__main__":
    main()
