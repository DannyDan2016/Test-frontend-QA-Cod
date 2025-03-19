from playwright.async_api import Page

class CheckoutInformationPage:
    def __init__(self, page: Page):
        self.page = page

    async def fill_information(self, first_name, last_name, postal_code):
        await self.page.locator("#first-name").fill(first_name) 
        await self.page.locator("#last-name").fill(last_name) 
        await self.page.locator("#postal-code").fill(postal_code)  
        await self.page.locator("#continue").click() 
