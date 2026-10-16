import unittest

from selenium.webdriver.common.by import By

from base import SweetScoopTestCase


class TestPlaceOrder(SweetScoopTestCase):
    def test_placing_order_clears_cart_and_appears_in_history(self):
        self.create_user_and_log_in()
        self.wait_for_flavor_catalog()

        self.add_flavor_to_order("Vanilla Dream")
        self.wait_for_text(By.CSS_SELECTOR, ".order-item", "Vanilla Dream")
        self.add_flavor_to_order("Coffee Buzz")
        self.wait_for_count(By.CSS_SELECTOR, ".order-item", 2)
        self.wait_for_text(By.CSS_SELECTOR, ".order-total", "Total: $10.48")

        self.click(By.CSS_SELECTOR, ".place-order")

        status = self.wait_for_text(
            By.CSS_SELECTOR, ".order-list .page-status", "Order placed successfully."
        )
        self.assertIn("status-success", status.get_attribute("class"))
        self.find(By.CSS_SELECTOR, ".order-empty")

        self.click(By.LINK_TEXT, "Order History")
        self.wait_for_url("/order-history")

        order = self.wait_for_text(By.CSS_SELECTOR, ".history-order h3", "Order #1")
        order = order.find_element(By.XPATH, "..")
        self.assertIn("Total: $10.48", order.text)
        self.assertRegex(order.text, r"Date: \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")

        items = [li.text for li in order.find_elements(By.CSS_SELECTOR, ".history-items li")]
        self.assertEqual(len(items), 2)
        self.assertTrue(items[0].startswith("Vanilla Dream"))
        self.assertIn("Qty: 1", items[0])
        self.assertTrue(items[1].startswith("Coffee Buzz"))


if __name__ == "__main__":
    unittest.main()
