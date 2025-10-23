import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://practicetestautomation.com/practice-test-login/"

@pytest.mark.web
def test_login_sucesso(chrome_driver):
    driver = chrome_driver
    driver.get(BASE_URL)

    driver.find_element(By.ID, "username").send_keys("student")
    driver.find_element(By.ID, "password").send_keys("Password123")
    driver.find_element(By.ID, "submit").click()

    # Valida sucesso
    assert "Logged In Successfully" in driver.page_source
    assert "/logged-in-successfully/" in driver.current_url

@pytest.mark.web
def test_login_email_invalido(chrome_driver):
    driver = chrome_driver
    driver.get(BASE_URL)

    driver.find_element(By.ID, "username").send_keys("usuario_invalido")
    driver.find_element(By.ID, "password").send_keys("Password123")
    driver.find_element(By.ID, "submit").click()

    erro = driver.find_element(By.ID, "error")
    assert erro.is_displayed()
    assert "Your username is invalid!" in erro.text

@pytest.mark.web
def test_login_senha_incorreta(chrome_driver):
    driver = chrome_driver
    driver.get(BASE_URL)

    driver.find_element(By.ID, "username").send_keys("student")
    driver.find_element(By.ID, "password").send_keys("errada")
    driver.find_element(By.ID, "submit").click()

    erro = driver.find_element(By.ID, "error")
    assert erro.is_displayed()
    assert "Your password is invalid!" in erro.text

@pytest.mark.web
def test_login_sem_preencher_campos(chrome_driver):
    driver = chrome_driver
    driver.get(BASE_URL)
    driver.find_element(By.ID, "submit").click()

    erro = driver.find_element(By.ID, "error")
    assert erro.is_displayed()
    # A página normalmente mostra mensagem de usuário inválido
    assert "invalid" in erro.text.lower()

@pytest.mark.web
def test_mensagens_erro_adequadas(chrome_driver):
    driver = chrome_driver
    wait = WebDriverWait(driver, 10)
    
    # Usuário incorreto
    driver.get(BASE_URL)
    driver.find_element(By.ID, "username").send_keys("x")
    driver.find_element(By.ID, "password").send_keys("Password123")
    driver.find_element(By.ID, "submit").click()
    
    # Aguarda o texto aparecer no elemento de erro
    wait.until(EC.text_to_be_present_in_element((By.ID, "error"), "Your username is invalid!"))
    assert "Your username is invalid!" in driver.find_element(By.ID, "error").text

    # Senha incorreta
    driver.get(BASE_URL)
    driver.find_element(By.ID, "username").send_keys("student")
    driver.find_element(By.ID, "password").send_keys("x")
    driver.find_element(By.ID, "submit").click()
    
    # Aguarda o texto aparecer no elemento de erro
    wait.until(EC.text_to_be_present_in_element((By.ID, "error"), "Your password is invalid!"))
    assert "Your password is invalid!" in driver.find_element(By.ID, "error").text