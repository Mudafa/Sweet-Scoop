import unittest

from selenium.webdriver.common.by import By

from base import SweetScoopTestCase


class TestProtectedRoutes(SweetScoopTestCase):
    def test_flavors_page_redirects_to_login_when_logged_out(self):
        self.open("/flavors")

        self.wait_for_url("/login")
        self.wait_for_text(By.CSS_SELECTOR, ".login-section h2", "Login")

    def test_order_history_redirects_to_login_when_logged_out(self):
        self.open("/order-history")

        self.wait_for_url("/login")
        self.wait_for_text(By.CSS_SELECTOR, ".login-section h2", "Login")


if __name__ == "__main__":
    unittest.main()
