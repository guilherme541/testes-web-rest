import pytest
from exercicio04.pages.login_page import LoginPage
from exercicio04.pages.dashboard_page import DashboardPage

@pytest.mark.web
def test_login_pom_sucesso(chrome_driver):
    login = LoginPage(chrome_driver)
    login.abrir()
    login.fazer_login("student", "Password123")

    dash = DashboardPage(chrome_driver)
    assert dash.esta_logado()

@pytest.mark.web
def test_login_pom_erro(chrome_driver):
    login = LoginPage(chrome_driver)
    login.abrir()
    login.fazer_login("student", "errada")

    assert "invalid" in chrome_driver.page_source.lower()