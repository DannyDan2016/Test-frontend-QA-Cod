from playwright.async_api import Page

class InventoryPage:
    def __init__(self, page: Page):
        self.page = page

    async def add_to_cart(self, product_name: str):
        product_locator = self.page.locator(f".inventory_item:has-text('{product_name}')")
        add_button = product_locator.locator(".btn_inventory")
        await add_button.click() 

    async def get_cart_count(self) -> str:
        count_element = self.page.locator(".shopping_cart_badge")
        return await count_element.text_content()  
