from playwright.async_api import Page

class CartPage:
    def __init__(self, page: Page):
        self.page = page

    async def get_products(self):
        product_elements = await self.page.locator(".cart_item").all()  
        products = []

        for element in product_elements:
            name = await element.locator(".inventory_item_name").text_content()  
            price = await element.locator(".inventory_item_price").text_content()  
            products.append((name.strip(), price.strip()))

        return products
