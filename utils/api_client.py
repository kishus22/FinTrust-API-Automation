from utils.logger import logger
from playwright.sync_api import sync_playwright


class APIClient:
    def __init__(self, base_url):
        self.playwright = sync_playwright().start()
        self.request = self.playwright.request.new_context(base_url=base_url)

    def post(self, endpoint, data=None, headers=None):
        return self.request.post(endpoint, data=data, headers=headers)

    def get(self, endpoint, headers=None):
        return self.request.get(endpoint, headers=headers)

    def patch(self, endpoint, data=None, headers=None):
        return self.request.patch(endpoint, data=data, headers=headers)

    def close(self):
        self.playwright.stop()