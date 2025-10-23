"""
Fixtures compartilhadas para todos os testes
"""
import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import requests
import shutil


def tem_chrome_instalado():
    """Verifica se Chrome está instalado"""
    # Windows: procura chrome.exe
    if shutil.which("chrome") or shutil.which("chrome.exe"):
        return True
    # Linux/Mac: procura google-chrome ou chromium
    if shutil.which("google-chrome") or shutil.which("chromium"):
        return True
    # Verifica caminhos comuns do Windows
    common_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    ]
    for path in common_paths:
        if os.path.exists(path):
            return True
    # Verifica variáveis de ambiente
    if os.getenv("CHROME") or os.getenv("GOOGLE_CHROME_BIN"):
        return True
    return False


@pytest.fixture
def chrome_driver():
    """Fixture que retorna uma instância do Chrome WebDriver"""
    if not tem_chrome_instalado():
        pytest.skip("Chrome não está instalado neste ambiente")
    
    options = Options()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-blink-features=AutomationControlled')
    
    # Usa chromedriver local se disponível (evita download)
    driver_path = os.getenv("CHROMEDRIVER")
    if driver_path and os.path.exists(driver_path):
        service = Service(driver_path)
    elif os.path.exists(r"C:\Drivers\chromedriver\chromedriver.exe"):
        service = Service(r"C:\Drivers\chromedriver\chromedriver.exe")
    else:
        # Fallback: tenta baixar via webdriver-manager (precisa de internet)
        service = Service(ChromeDriverManager().install())
    
    driver = webdriver.Chrome(service=service, options=options)
    
    yield driver
    
    driver.quit()


@pytest.fixture
def headless_chrome_driver():
    """Fixture para Chrome em modo headless (sem interface gráfica)"""
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # Usa chromedriver local se disponível
    driver_path = os.getenv("CHROMEDRIVER")
    if driver_path and os.path.exists(driver_path):
        service = Service(driver_path)
    elif os.path.exists(r"C:\Drivers\chromedriver\chromedriver.exe"):
        service = Service(r"C:\Drivers\chromedriver\chromedriver.exe")
    else:
        service = Service(ChromeDriverManager().install())
    
    driver = webdriver.Chrome(service=service, options=options)
    
    yield driver
    
    driver.quit()


@pytest.fixture
def api_base_url():
    """URL base da API de testes"""
    return "https://jsonplaceholder.typicode.com"


@pytest.fixture
def api_session():
    """Sessão HTTP reutilizável para testes de API"""
    session = requests.Session()
    session.headers.update({
        'Content-Type': 'application/json',
        'User-Agent': 'Python-Test-Client/1.0'
    })
    
    yield session
    
    session.close()


@pytest.fixture
def auth_token():
    """
    Fixture que simula obtenção de token de autenticação
    Em produção, faria login real em uma API
    """
    # Simulação - em produção seria uma chamada real
    return "fake-jwt-token-for-testing"


def pytest_addoption(parser):
    """Adiciona opções customizadas ao pytest"""
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Executar testes web em modo headless"
    )


@pytest.fixture
def browser_option(request):
    """Retorna se deve usar modo headless"""
    return request.config.getoption("--headless")