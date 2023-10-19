import os
import json
import abc

import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

from crawl.base import BaseCrawler


class NaverCrawler(BaseCrawler):
    def __init__(self, channel_name: str = 'NAVER'):
        super().__init__()
        self.get_config(channel_name)

    def login(self):
        wait = WebDriverWait(self.driver, 5)  # 최초 로딩 최장 5초 대기

        log_in_btn = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "btn.btn-login"))
        )

        log_in_btn.click()
        self.driver.implicitly_wait(1)
        self.driver.refresh()

        log_in_types = self.driver.find_elements(
            By.CSS_SELECTOR, "li[class ^= 'Login_type_item']"
        )
        naver_id_log_in = log_in_types[1]
        naver_id_log_in.click()

        # 팝업창 로그인
        self.driver.switch_to.window(self.driver.window_handles[-1])
        log_in_btn = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "btn_login"))
        )
        id_pw_rows = self.driver.find_elements(By.CLASS_NAME, "input_row")
        self.authentication(id_pw_rows[0], id_pw_rows[1])  # avoid captcha

        self.driver.implicitly_wait(1)
        log_in_btn.click()  # click 시 captcha 와 2단계 인증 발생 가능

    def authentication(self, id_element, pw_element):
        # using key instead of send_key
        # ref: https://ai-creator.tistory.com/125
        tmp = pyperclip.paste()

        pyperclip.copy(self.info["id"])
        ele_id = id_element.find_element(By.ID, "id")
        ele_id.click()
        ele_id.send_keys(Keys.CONTROL, "v")

        pyperclip.copy(self.info["pw"])
        ele_pw = pw_element.find_element(By.ID, "pw")
        ele_pw.click()
        ele_pw.send_keys(Keys.CONTROL, "v")

        pyperclip.copy(tmp)

    def modal_dispose(self, delay: int = 1):
        try:
            modal_header = self.driver.find_element(By.CLASS_NAME, "modal-header")
            close_btn = modal_header.find_element(By.CLASS_NAME, "close")
            close_btn.click()
            self.driver.implicitly_wait(delay)
        except:
            pass

    def run(self):
        self.driver.get(self.info["url"])

        # 개인 계정 로그인
        # TODO:사업자 계정 받으면 수정 (2차 인증 해제되어야 함)
        self.login()

        # 모달창 닫기
        self.driver.switch_to.window(self.driver.window_handles[0])
        while "modal-open" in self.driver.find_element(
            By.TAG_NAME, "body"
        ).get_attribute("class"):
            self.driver.implicitly_wait(0.5)
            self.modal_dispose()

        self.driver.implicitly_wait(3)

        manager = self.driver.find_element(By.XPATH, "//*[contains(text(), '판매관리')]")
        manager.click()
        logistic = manager.find_element(By.XPATH, "//*[contains(text(), '배송현황 관리')]")
        confirm = manager.find_element(By.XPATH, "//*[contains(text(), '구매확정 내역')]")

        # 배송현황 관리 탭에서 목록 가져오기
        logistic.click()
        search_btn = self.driver.find_element(
            By.CLASS_NAME, "button_area"
        ).find_elements(By.TAG_NAME, "button")[-1]
        search_btn.click()
        self.driver.implicitly_wait(3)

        # 구매확정 내역에서 목록 가져오기
        logistic.click()
        search_btn = self.driver.find_element(
            By.CLASS_NAME, "button_area"
        ).find_elements(By.TAG_NAME, "button")[-1]
        search_btn.click()
        self.driver.implicitly_wait(3)

