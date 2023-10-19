import abc
from abc import abstractmethod

import pyperclip
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from utils import gen_agent, read_json


class BaseCrawler(abc.ABC):
    def __init__(self):
        self.driver, self.opt, self.channel_info = None, None, None
        self.init_driver()
        self.get_config()

    def init_driver(self, headless: bool = False) -> None:
        self.opt = webdriver.ChromeOptions()
        if headless:
            self.opt.add_argument("--headless")
        self.opt.add_argument("--no-sandbox")
        self.opt.add_argument("--disable-dev-shm-usage")
        self.opt.add_argument("user-agent=" + gen_agent())
        self.driver = webdriver.Chrome(options=self.opt)

    def get_config(self, channel_name: str) -> None:
        self.channel_info = read_json('./config/url_info.json')[channel_name]

    def dispose(self):
        self.driver.quit()

    @abstractmethod
    def login(self):
        return

    @abstractmethod
    def find_login_elements(self):
        id_element, pw_element, confirm_btn = None, None, None
        return id_element, pw_element, confirm_btn

    @abstractmethod
    def goto_manage_tab(self):
        return

    @abstractmethod
    def parse_data(self):
        return

    @abstractmethod
    def insert_data_to_db(self):
        return

    def authentication(self, id_dict: dict, pw_dict: dict) -> None:
        """
        Input user id & pw using clipboard instead of send_keys to avoid captcha.
        :param id_dict: dictionary of id element & user id
        :param pw_dict: dictionary of pw element & user pw
        :return: None
        """

        assert set(id_dict.keys()) == set(pw_dict.keys()) == {'element', 'value'}

        original_clipboard = pyperclip.paste()

        pyperclip.copy(id_dict['value'])
        id_dict['element'].click()
        id_dict['element'].send_keys(Keys.CONTROL, "v")

        pyperclip.copy(pw_dict['value'])
        pw_dict['element'].click()
        pw_dict['element'].send_keys(Keys.CONTROL, "v")

        pyperclip.copy(original_clipboard)

    @abstractmethod
    def run(self, base_url: str):
        self.driver.get(base_url)

        id, pw, ok = self.find_login_elements()

        self.authentication(
            id_dict={'element': id, 'value': self.channel_info['id']},
            pw_dict={'element': id, 'value': self.channel_info['pw']}
        )

        self.goto_manage_tab()
        self.parse_data()
        self.insert_data_to_db()
