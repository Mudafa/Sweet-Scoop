import unittest

from selenium.webdriver.common.by import By

from base import SweetScoopTestCase


class TestLoginSuccess(SweetScoopTestCase):
    def test_valid_login_redirects_to_flavors_and_shows_logout(self):
        username = self.unique_username()
        self.sign_up(username)
        self.wait_for_status("Registration successful.")

        self.log_in(username)

        status = self.wait_for_status("Login successful.")
        self.assertIn("status-success", status.get_attribute("class"))

        self.wait_for_url("/flavors")
        self.wait_for_text(By.CSS_SELECTOR, "header .auth-button", "Logout")

        stored = self.driver.execute_script(
            "return JSON.parse(localStorage.getItem('sweetScoopAuth'));"
        )
        self.assertEqual(stored["username"], username)
        self.assertIsInstance(stored["userId"], int)


if __name__ == "__main__":
    unittest.main()
