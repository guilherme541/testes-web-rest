
import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

termos_busca = [
    "Python",
    "Selenium",
    "Pytest",
    "API Testing",
    "Automation"
]

@pytest.mark.web
@pytest.mark.parametrize("termo_busca", termos_busca)
def test_busca_google(chrome_driver, termo_busca):
    """
    Testa busca no Google com múltiplos termos.
    Valida que o termo aparece nos resultados.
    """
    driver = chrome_driver
    wait = WebDriverWait(driver, 10)
    
    # Acessa o Google
    driver.get("https://www.google.com")
    
    # Aceita cookies se aparecer (GDPR)
    try:
        aceitar_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Aceitar') or contains(., 'Accept')]"))
        )
        aceitar_btn.click()
        time.sleep(1)
    except:
        pass  # Ignora se não aparecer o banner de cookies
    
    # Localiza a caixa de busca
    try:
        search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
    except:
        # Fallback: tenta outros seletores comuns
        search_box = driver.find_element(By.CSS_SELECTOR, "textarea[name='q'], input[name='q']")
    
    # Digita o termo e envia
    search_box.clear()
    search_box.send_keys(termo_busca)
    search_box.send_keys(Keys.RETURN)
    
    # Aguarda os resultados carregarem
    wait.until(EC.presence_of_element_located((By.ID, "search")))
    time.sleep(1)  # Pequeno delay adicional para estabilidade
    
    # Valida que o termo aparece na página de resultados
    page_source_lower = driver.page_source.lower()
    termo_lower = termo_busca.lower()
    
    assert termo_lower in page_source_lower, \
        f"Termo '{termo_busca}' não encontrado nos resultados da busca"


@pytest.mark.web
@pytest.mark.parametrize("termo,resultado_esperado", [
    ("Python programming", "python"),
    ("Selenium WebDriver", "selenium"),
    ("Pytest framework", "pytest"),
])
def test_busca_google_com_validacao(chrome_driver, termo, resultado_esperado):
    """
    Versão avançada: valida que um termo específico aparece nos resultados.
    """
    driver = chrome_driver
    wait = WebDriverWait(driver, 10)
    
    driver.get("https://www.google.com")
    
    # Aceita cookies
    try:
        aceitar_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Aceitar') or contains(., 'Accept')]"))
        )
        aceitar_btn.click()
        time.sleep(1)
    except:
        pass
    
    # Busca
    try:
        search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
    except:
        search_box = driver.find_element(By.CSS_SELECTOR, "textarea[name='q'], input[name='q']")
    
    search_box.clear()
    search_box.send_keys(termo)
    search_box.send_keys(Keys.RETURN)
    
    # Aguarda resultados
    wait.until(EC.presence_of_element_located((By.ID, "search")))
    time.sleep(1)
    
    # Valida resultado esperado
    assert resultado_esperado.lower() in driver.page_source.lower()


# Teste extra: busca com termo vazio (caso negativo)
@pytest.mark.web
def test_busca_google_termo_vazio(chrome_driver):
    """Testa comportamento ao buscar com termo vazio"""
    driver = chrome_driver
    wait = WebDriverWait(driver, 10)
    
    driver.get("https://www.google.com")
    
    try:
        search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
    except:
        search_box = driver.find_element(By.CSS_SELECTOR, "textarea[name='q'], input[name='q']")
    
    search_box.clear()
    search_box.send_keys(Keys.RETURN)
    
    # Deve permanecer na página inicial ou mostrar mensagem
    time.sleep(1)
    assert "google.com" in driver.current_url