from features.steps.utilities import *
from features.pages.base_page import BasePage


class ExamplePage(BasePage):

    locators = AttrDict(dict(
                                        table=("xpath", "//*[@class='ant-table-content']")
    ))

    def __init__(self, driver):
        BasePage.__init__(self, driver)

    def navigate_to_website(self, url):
        self.open_web(url)

