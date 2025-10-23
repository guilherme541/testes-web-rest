import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.web
@pytest.mark.parametrize("termo_busca", [
    "Python",
    "Selenium",
    "Pytest",
    "API Testing",
    "Automation"
])
def test_busca_google(chrome_driver, termo_busca):
    driver = chrome_driver
    wait = WebDriverWait(driver, 10)

    driver.get("https://www.google.com")

    # Aceitar cookies (se aparecer)
    try:
        aceitar_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Aceitar') or contains(., 'Accept')]"))
        )
        aceitar_btn.click()
        time.sleep(1)
    except:
        pass

    # Caixa de busca pode ser input ou textarea dependendo da variante
    try:
        search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
    except:
        search_box = driver.find_element(By.CSS_SELECTOR, "textarea[name='q'], input[name='q']")

    search_box.clear()
    search_box.send_keys(termo_busca)
    search_box.send_keys(Keys.RETURN)

    # Aguardar resultados
    wait.until(EC.presence_of_element_located((By.ID, "search")))
    time.sleep(2)

    assert termo_busca.lower() in driver.page_source.lower()