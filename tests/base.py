"""Shared Selenium WebDriver setup and helpers for the Sweet Scoop test suite."""

import os
import unittest
import uuid

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = os.environ.get("SWEET_SCOOP_URL", "http://localhost:3000").rstrip("/")
HEADLESS = os.environ.get("HEADLESS", "1") != "0"
WAIT_SECONDS = 10
VALID_PASSWORD = "Scoop@1234"


class SweetScoopTestCase(unittest.TestCase):
    """Opens a fresh Chrome window for every test and closes it afterwards."""

    def setUp(self):
        options = webdriver.ChromeOptions()
        if HEADLESS:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1400,1000")
        self.driver = webdriver.Chrome(options=options)
        # React re-renders can replace an element between finding and using it.
        self.wait = WebDriverWait(
            self.driver, WAIT_SECONDS, ignored_exceptions=[StaleElementReferenceException]
        )

    def tearDown(self):
        self.driver.quit()

    # ---------- navigation ----------
    def open(self, path="/"):
        self.driver.get(f"{BASE_URL}{path}")

    def wait_for_url(self, path):
        self.wait.until(EC.url_to_be(f"{BASE_URL}{path}"))

    # ---------- element helpers ----------
    def find(self, by, value):
        return self.wait.until(EC.visibility_of_element_located((by, value)))

    def find_all(self, by, value):
        return self.driver.find_elements(by, value)

    def click(self, by, value):
        def find_and_click(driver):
            element = EC.element_to_be_clickable((by, value))(driver)
            if not element:
                return False
            element.click()
            return True

        self.wait.until(find_and_click)

    def type_into(self, element_id, text):
        field = self.find(By.ID, element_id)
        field.clear()
        field.send_keys(text)

    def wait_for_text(self, by, value, text):
        self.wait.until(EC.text_to_be_present_in_element((by, value), text))
        return self.find(by, value)

    def wait_for_count(self, by, value, count):
        self.wait.until(lambda d: len(d.find_elements(by, value)) == count)
        return self.find_all(by, value)

    def wait_for_status(self, text):
        """Wait for the form status banner (DisplayStatus component) to show text."""
        return self.wait_for_text(By.CSS_SELECTOR, ".status-message", text)

    # ---------- user flows ----------
    @staticmethod
    def unique_username(prefix="tester"):
        return f"{prefix}{uuid.uuid4().hex[:8]}"

    def submit_form(self):
        self.click(By.CSS_SELECTOR, ".login-form button[type='submit']")

    def sign_up(self, username, password=VALID_PASSWORD, email=None, confirm=None):
        self.open("/signup")
        self.type_into("signup-username", username)
        self.type_into("signup-email", email or f"{username}@example.com")
        self.type_into("signup-password", password)
        self.type_into("signup-confirm-password", password if confirm is None else confirm)
        self.submit_form()

    def log_in(self, username, password=VALID_PASSWORD):
        self.open("/login")
        self.type_into("username", username)
        self.type_into("password", password)
        self.submit_form()

    def create_user_and_log_in(self):
        """Register a brand-new user, log in, and wait until /flavors is shown."""
        username = self.unique_username()
        self.sign_up(username)
        self.wait_for_status("Registration successful.")
        self.log_in(username)
        self.wait_for_status("Login successful.")
        self.wait_for_url("/flavors")
        self.wait_for_text(By.CSS_SELECTOR, "header .auth-button", "Logout")
        return username

    def wait_for_flavor_catalog(self):
        return self.wait_for_count(By.CSS_SELECTOR, ".flavor-grid .flavor-card", 10)

    def add_flavor_to_order(self, flavor_name):
        self.click(
            By.XPATH,
            f"//div[contains(@class,'flavor-card')][h3[text()='{flavor_name}']]//button",
        )
