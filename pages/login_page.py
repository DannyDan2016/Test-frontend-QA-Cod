from playwright.async_api import Page

class LoginPage:
    def __init__(self, page: Page):
        self.page = page

    async def login(self, username: str, password: str):
        await self.page.locator("#user-name").fill(username)
        await self.page.locator("#password").fill(password)
        await self.page.locator("#login-button").click()
