import telebot
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import time
import random
import pyautogui
import datetime
import threading

token = "token"
lock = False

telegram_bot = telebot.TeleBot(token)

class Bot():
    en_use = 0

    brovse = None

    day = 0

    starting_process_day = datetime.datetime.now().today().day

    sleep_time_train = 0
    wt_train = 0

    sleep_time_work = 0
    wt_work = 0

    start_day = datetime.datetime.now().today().day
    start_month = datetime.datetime.now().today().month

    def __init__(self, brovse):
        self.brovse = brovse

    def login(self, email, password):
        try:
            time.sleep(1)
            self.brovse.get("https://rivalregions.com/")
            time.sleep(5)

            input_email = self.brovse.find_element(By.NAME, "mail")
            input_email.clear()
            input_email.send_keys(email)
            time.sleep(2)

            input_password = self.brovse.find_element(By.NAME, "p")
            input_password.clear()
            input_password.send_keys(password)
            time.sleep(3)
            input_password.send_keys(Keys.ENTER)

            time.sleep(2)
        except:
            return "Error!!"
        # brovse.close()
        # brovse.quit()

    def select_job(self):
        try:
            self.get_menu_button("https://rivalregions.com/#work")

            find_factory = self.brovse.find_element(By.XPATH, "/html/body/div[6]/div[1]/div[5]/div[2]")
            time.sleep(0.5)
            find_factory.click()
            time.sleep(3)

            factory_list = self.brovse.find_element(By.ID, "list_tbody")
            time.sleep(0.5)
            factorys = factory_list.find_elements(By.TAG_NAME, "tr")
            for factory in factorys:
                time.sleep(1)
                salary = int(factory.text.split("%")[0].split(" ")[-1])
                if salary == 100:
                    factory.find_elements(By.TAG_NAME, "td")[-1].click()
                    break
            time.sleep(2)
        except:
            return

    def worked(self):
        try:
            time.sleep(5)

            if self.en_use == 10:
                self.en_use = 0

                storage = self.brovse.find_element(By.XPATH, "/html/body/div[5]/div[2]/div[6]")
                storage.click()
                time.sleep(2)

                buy_enegry = self.brovse.find_element(By.XPATH, "/html/body/div[6]/div[1]/div[11]/div[3]")
                buy_enegry.click()
                time.sleep(3)

                input_energy_value = self.brovse.find_element(By.XPATH, "/html/body/div[6]/div[1]/div[1]/div[2]/div[3]/input")
                input_energy_value.clear()
                input_energy_value.send_keys(2000)
                time.sleep(1)

                produce = self.brovse.find_element(By.XPATH, "/html/body/div[6]/div[1]/div[1]/div[2]/div[4]/div")
                produce.click()
                time.sleep(2)

            time.sleep(1)

            factory = self.brovse.find_element(By.XPATH, "/html/body/div[6]/div[1]/div[6]/div[2]/div[2]/div[3]/div[1]")
            factory.click()
            time.sleep(1.5)
            pyautogui.press('enter')
            time.sleep(2)

            close_work_panel = self.brovse.find_element(By.XPATH, "/html/body/div[3]/div/div[1]")
            close_work_panel.click()

            self.en_use += 1

            return 600, time.time()
        except:
            return 0, 0

    def select_energy(self):
        try:
            self.get_menu_button("https://rivalregions.com/#work")

            sel_ener = self.brovse.find_element(By.XPATH, "/html/body/div[6]/div[1]/div[6]/div[2]/div[2]/div[2]/div[2]/div/div/div")
            sel_ener.click()
            time.sleep(3)

            energy_list = self.brovse.find_element(By.XPATH, "/html/body/div[6]/div[1]/div[6]/div[2]/div[2]/div[2]/div[2]/div/ul")
            time.sleep(1)

            full_energy = energy_list.find_elements(By.TAG_NAME, "li")[-1]
            full_energy.click()
            time.sleep(2)
        except:
            return "Error!!!"

    def xpath_exith(self, xpath):
        try:
            self.brovse.find_element(By.XPATH, xpath)
            exist = True
        except:
            exist = False
        return exist

    def training(self):
        try:
            self.get_menu_button("https://rivalregions.com/#overview")

            ran_perk = random.randint(1, 3)

            if ran_perk == 1:
                wait_time, days = self.click_train_button("/html/body/div[6]/div[1]/div[9]/div[2]/div[4]")
            elif ran_perk == 2:
                wait_time, days = self.click_train_button("/html/body/div[6]/div[1]/div[9]/div[2]/div[5]")
            elif ran_perk == 3:
                wait_time, days = self.click_train_button("/html/body/div[6]/div[1]/div[9]/div[2]/div[6]")
            else:
                return 0.0, 0, 0, 0

            if days == None:
                return wait_time, time.time(), datetime.datetime.now().today().day, datetime.datetime.now().today().month
            else:
                return wait_time, time.time(), days, datetime.datetime.now().today().month
        except:
            return 0.0, 0, 0, 0

    def click_train_button(self, perk_xpath):
        try:
            perk = self.brovse.find_element(By.XPATH, perk_xpath)
            time.sleep(0.3)
            perk.click()
            time.sleep(1)

            train = self.brovse.find_element(By.XPATH, "/html/body/div[6]/div[1]/div[9]/div[1]/div[2]/div[2]/div/div[1]")
            time.sleep(0.3)
            trainning_time = train.find_element(By.CLASS_NAME, "perk_4").text.split(",")[-1]

            hour_min_second = trainning_time.split(":")
            second = 0

            days = None

            for _, el in enumerate(hour_min_second):
                if len(hour_min_second) == 3:
                    if _ == 0:
                        if "д" in el:
                            el = el.replace("д", "")
                            el = el.split(" ")
                            days = el[0]
                            second += int(el[1]) * 3600
                        else:
                            second += int(el[1]) * 3600
                    elif _ == 1:
                        second += int(el) * 60
                    else:
                        second += int(el)
                else:
                    if _ == 0:
                        second += int(el) * 60
                    else:
                        second += int(el)

            time.sleep(0.5)
            train.click()
            time.sleep(0.3)

            return second, days
        except:
            return "Error!!!"

    def send_likes(self, url, liky, login_email, login_password):
        try:
            self.login(login_email, login_password)
            self.get_menu_button(url)

            if liky:
                plus = self.brovse.find_element(By.XPATH, "/html/body/div[6]/div[1]/div[1]/div[5]/h1/span[3]")
                plus.click()
            else:
                minus = self.brovse.find_element(By.XPATH, "/html/body/div[6]/div[1]/div[1]/div[5]/h1/span[1]")
                minus.click()
            time.sleep(2)

            self.brovse.close()
            self.brovse.quit()
        except:
            self.brovse.close()
            self.brovse.quit()

    def get_menu_button(self, url):
        time.sleep(3)
        self.brovse.get(url.replace("#", ""))
        time.sleep(5)
        self.brovse.get(url)
        time.sleep(3)

    def main(self,  email, password):
        self.login(email, password)

        self.select_job()
        while True:
            if time.time() - self.wt_work >= self.sleep_time_work:
                self.select_energy()

                energy_hub = "/html/body/div[5]/div[1]/div[1]/div[5]"
                if self.xpath_exith(energy_hub):
                    energy = self.brovse.find_element(By.XPATH, energy_hub)
                    if "block" in energy.get_attribute("style"):
                        energy.click()
                        time.sleep(1)
                self.sleep_time_work, self.wt_work = self.worked()
            elif datetime.datetime.now().today().month > self.start_month or datetime.datetime.now().today().month == self.start_month and datetime.datetime.now().today().day > self.start_day or datetime.datetime.now().today().month == self.start_month and datetime.datetime.now().today().day == self.start_day and time.time() - self.wt_train >= self.sleep_time_train:
                self.sleep_time_train, self.wt_train, start_day, self.start_month = self.training()
            elif self.day >= 7:
                self.day = 0

                self.get_menu_button("https://rivalregions.com/#slide/profile/2001487437")

                if self.xpath_exith("/html/body/div[3]/div/div[3]/div[7]"):
                    self.send_donate()
            elif self.starting_process_day < datetime.datetime.now().today().day:
                self.day += 1
                self.starting_process_day += 1

    def send_donate(self):
        time.sleep(2)
        my_money = self.brovse.find_element(By.XPATH, "/html/body/div[5]/div[1]/div[1]/div[4]/span[1]/span")
        my_money = my_money.text.split(".")

        moneys = ""

        for el in my_money:
            moneys += el

        time.sleep(3)

        my_acount = self.brovse.find_element(By.XPATH, "/html/body/div[3]/div/div[3]/div/div/div/table/tbody/tr[1]")
        my_acount.click()
        time.sleep(3)

        donate = self.brovse.find_element(By.XPATH, "/html/body/div[3]/div/div[3]/div[7]")
        donate.click()
        time.sleep(3)

        money = self.brovse.find_element(By.XPATH, "/html/body/div[3]/div/div[3]/div[3]/div[2]")
        money.click()
        time.sleep(3)

        donate_money = self.brovse.find_element(By.XPATH, "/html/body/div[3]/div/div[3]/div[1]/div/div[1]/div[2]/input")
        donate_money.clear()
        time.sleep(1)
        donate_money.send_keys(int(moneys) * 70 // 100)
        time.sleep(2)

        send = self.brovse.find_element(By.XPATH, "/html/body/div[3]/div/div[3]/div[1]/div/div[2]/div")
        send.click()
        time.sleep(2)

with open("Bots.txt", "r") as file:
    bots = file.read().split("\n")

for el in bots:
    bot_config = el.split(",")

    user_agent = UserAgent().chrome
    options = Options()
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--headless")

    bot = Bot(webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options))

    threading.Thread(target=bot.main, args=(bot_config[0].strip(), bot_config[1].strip())).start()

@telegram_bot.message_handler(commands=['start'])
def welkome(message):
    telegram_bot.send_message(message.chat.id, "Hello!!Please enter password:")

@telegram_bot.message_handler(commands=['sendlikes'])
def send_reaction(message):
    global lock
    if lock:
        config_url = message.text.split(" ")[1]
        print(config_url)
        plus_minus = message.text.split(" ")[2]
        print(plus_minus)
        if plus_minus == "plus":
            plus_minus = True
        else:
            plus_minus = False
        reaction_number = int(message.text.split(" ")[3])

        with open("Bots.txt", "r") as file:
            bots = file.read().split("\n")
        bots = bots[:reaction_number]

        for el in bots:
            bot_config = el.split(",")
            user_agent = UserAgent().chrome
            options = Options()
            options.add_argument(f"user-agent={user_agent}")
            options.add_argument("--headless")

            bot = Bot(webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options))

            threading.Thread(target=bot.send_likes, args=(config_url, plus_minus, bot_config[0].strip(), bot_config[1].strip())).start()
    else:
        telegram_bot.send_message(message.chat.id, "Enter password:")

@telegram_bot.message_handler(commands=['addbot'])
def add_bot(message):
    AddBot = message.text.split(" ")
    with open("Bots.txt", "a") as file:
        file.write(f"\n{AddBot[1]} {AddBot[2]}")

    with open("Bots.txt", "r") as file:
        bots = file.read().split("\n")

    telegram_bot.send_message(message.chat.id, "Bot was add")

    bot_config =  bots[-1].split(",")
    user_agent = UserAgent().chrome
    options = Options()
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--headless")

    bot = Bot(webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options))

    threading.Thread(target=bot.main, args=(bot_config[0].strip(), bot_config[1].strip())).start()

@telegram_bot.message_handler(content_types=['text'])
def check_password(message):
    if message.text == "12345678":
        global lock
        lock = True
        telegram_bot.send_message(message.chat.id, "Sucseful")
    else:
        telegram_bot.send_message(message.chat.id, "Ceck your password")
telegram_bot.polling(none_stop=True)
