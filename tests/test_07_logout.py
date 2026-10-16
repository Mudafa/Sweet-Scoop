import unittest

from selenium.webdriver.common.by import By

from base import SweetScoopTestCase


class TestLogout(SweetScoopTestCase):
    def test_logout_clears_session_and_blocks_protected_pages(self):
        self.create_user_and_log_in()

        self.click(By.CSS_SELECTOR, "header .auth-button")

        self.wait_for_url("/")
        self.wait_for_text(By.CSS_SELECTOR, "header .auth-button", "Login")
        self.assertIsNone(
            self.driver.execute_script("return localStorage.getItem('sweetScoopAuth');")
        )

        self.open("/flavors")
        self.wait_for_url("/login")


if __name__ == "__main__":
    unittest.main()
