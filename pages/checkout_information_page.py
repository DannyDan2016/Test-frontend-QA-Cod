from playwright.sync_api import Page

from pages.base_page import BasePage


class CheckoutInformationPage(BasePage):
    path = "/checkout-step-one.html"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        # En el checkout los data-test van en camelCase (los id son first-name, etc.)
        self.first_name = page.get_by_test_id("firstName")
        self.last_name = page.get_by_test_id("lastName")
        self.postal_code = page.get_by_test_id("postalCode")
        self.continue_button = page.get_by_test_id("continue")

    def fill_information(self, first_name: str, last_name: str, postal_code: str) -> None:
        self.first_name.fill(first_name)
        self.last_name.fill(last_name)
        self.postal_code.fill(postal_code)
        self.continue_button.click()
