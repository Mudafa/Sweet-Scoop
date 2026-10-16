import unittest

from base import SweetScoopTestCase


class TestSignupSuccess(SweetScoopTestCase):
    def test_valid_signup_shows_success_and_redirects_to_login(self):
        self.sign_up(self.unique_username())

        status = self.wait_for_status("Registration successful.")
        self.assertIn("status-success", status.get_attribute("class"))

        self.wait_for_url("/login")


if __name__ == "__main__":
    unittest.main()
