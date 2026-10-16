import unittest

from selenium.webdriver.common.by import By

from base import SweetScoopTestCase


class TestHomepageContent(SweetScoopTestCase):
    def test_homepage_shows_header_featured_flavors_reviews_and_footer(self):
        self.open("/")

        title = self.find(By.CSS_SELECTOR, "header h1")
        self.assertEqual(title.text, "Sweet Scoop Ice Cream Shop")
        self.assertTrue(self.find(By.CSS_SELECTOR, "header img").is_displayed())

        nav_links = [link.text for link in self.find_all(By.CSS_SELECTOR, ".navbar a")]
        self.assertEqual(nav_links, ["Home", "Flavors", "Order History", "Signup"])

        self.find(By.XPATH, "//h2[text()='About Sweet Scoop Ice Cream']")

        featured = self.wait_for_count(By.CSS_SELECTOR, ".flavorgrid .flavor-card", 3)
        for card in featured:
            self.assertNotEqual(card.find_element(By.TAG_NAME, "h3").text, "")
            self.assertIn("Price:", card.text)

        reviews = self.wait_for_count(By.CSS_SELECTOR, ".review-card", 2)
        for review in reviews:
            self.assertIn("\u2605", review.text)

        self.assertEqual(
            self.find_all(By.CSS_SELECTOR, ".status-message"),
            [],
            "Homepage fell back to built-in data, so the backend is not reachable.",
        )

        footer = self.find(By.TAG_NAME, "footer")
        self.assertIn("Sweet Scoop Ice Cream Shop. All rights reserved.", footer.text)


if __name__ == "__main__":
    unittest.main()
