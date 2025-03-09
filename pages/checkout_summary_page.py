from playwright.async_api import Page

class CheckoutSummaryPage:
    def __init__(self, page: Page):
        self.page = page

    async def get_subtotal(self):
        return (await self.page.locator("[data-test='subtotal-label']").text_content()).strip()

    async def get_tax(self):
        return (await self.page.locator("[data-test='tax-label']").text_content()).strip()

    async def get_total(self):
        return (await self.page.locator("[data-test='total-label']").text_content()).strip()

    async def complete_purchase(self):
        await self.page.locator("[data-test='finish']").click()

