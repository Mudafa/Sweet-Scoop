import unittest

from selenium.webdriver.common.by import By

from base import SweetScoopTestCase


class TestAddToOrder(SweetScoopTestCase):
    def test_adding_flavors_updates_quantity_and_total(self):
        self.create_user_and_log_in()
        self.wait_for_flavor_catalog()
        self.find(By.CSS_SELECTOR, ".order-empty")

        self.add_flavor_to_order("Vanilla Dream")
        item = self.wait_for_text(By.CSS_SELECTOR, ".order-item", "Vanilla Dream")
        self.assertIn("Quantity: 1", item.text)
        self.assertIn("Price: $4.99", item.text)
        self.wait_for_text(By.CSS_SELECTOR, ".order-total", "Total: $4.99")
        self.wait_for_text(By.CSS_SELECTOR, ".order-list .page-status", "Cart updated.")

        self.add_flavor_to_order("Vanilla Dream")
        item = self.wait_for_text(By.CSS_SELECTOR, ".order-item", "Quantity: 2")
        self.assertIn("Price: $9.98", item.text)

        self.add_flavor_to_order("Coffee Buzz")
        self.wait_for_count(By.CSS_SELECTOR, ".order-item", 2)
        self.wait_for_text(By.CSS_SELECTOR, ".order-total", "Total: $15.47")


if __name__ == "__main__":
    unittest.main()
