from selenium.webdriver.common.by import By
from .base_page import BasePage

class LoginPage(BasePage):
    URL = "https://practicetestautomation.com/practice-test-login/"

    EMAIL_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "submit")
    ERROR_MESSAGE = (By.ID, "error")

    def abrir(self):
        super().abrir(self.URL)

    def preencher_email(self, email):
        self.digitar(self.EMAIL_INPUT, email)

    def preencher_senha(self, senha):
        self.digitar(self.PASSWORD_INPUT, senha)

    def clicar_login(self):
        self.clicar(self.LOGIN_BUTTON)

    def fazer_login(self, email, senha):
        self.preencher_email(email)
        self.preencher_senha(senha)
        self.clicar_login()