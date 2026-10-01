from playwright.sync_api import Page


class Menu:
    """Menú lateral de las páginas autenticadas.

    El ``data-test="open-menu"`` es una imagen tapada por el botón real, así que se abre y
    se cierra por su rol accesible (``button`` con nombre "Open Menu" / "Close Menu").
    """

    def __init__(self, page: Page) -> None:
        self.open_button = page.get_by_role("button", name="Open Menu")
        self.close_button = page.get_by_role("button", name="Close Menu")
        self.all_items_link = page.get_by_test_id("inventory-sidebar-link")
        self.logout_link = page.get_by_test_id("logout-sidebar-link")
        self.reset_app_state_link = page.get_by_test_id("reset-sidebar-link")

    def open(self) -> None:
        self.open_button.click()

    def close(self) -> None:
        self.close_button.click()

    def logout(self) -> None:
        self.open()
        self.logout_link.click()

    def reset_app_state(self) -> None:
        self.open()
        self.reset_app_state_link.click()
