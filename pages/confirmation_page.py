from playwright.async_api import Page

class ConfirmationPage:
    def __init__(self, page: Page):
        self.page = page

    async def is_confirmation_displayed(self) -> bool:
        confirmation_text = await self.page.locator(".complete-header").text_content()
        return confirmation_text.strip() == "Thank you for your order!"  # ✅ Se usa `.strip()` por si hay espacios extras
