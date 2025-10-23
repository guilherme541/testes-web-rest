# Exercícios - Testes Web e REST

## Exercício 1: Teste de Login (Web)

Crie testes automatizados para o formulário de login de um site.

### Cenários a testar:
1. Login com credenciais válidas
2. Login com email inválido
3. Login com senha incorreta
4. Tentativa de login sem preencher campos
5. Verificar mensagens de erro apropriadas

### Site sugerido:
https://practicetestautomation.com/practice-test-login/

### Credenciais de teste:
- Username: student
- Password: Password123

### Estrutura esperada:

    tests/
    └── test_login.py

### Exemplo de teste:

    def test_login_sucesso(chrome_driver):
        driver = chrome_driver
        driver.get("https://practicetestautomation.com/practice-test-login/")
        
        # Preencher formulário
        driver.find_element(By.ID, "username").send_keys("student")
        driver.find_element(By.ID, "password").send_keys("Password123")
        driver.find_element(By.ID, "submit").click()
        
        # Verificar sucesso
        assert "Logged In Successfully" in driver.page_source

## Exercício 2: API de Produtos (REST)

Usando a API https://fakestoreapi.com/, crie testes para as seguintes operações.

### Testes a implementar:
1. Listar todos os produtos
2. Buscar produto por ID
3. Filtrar produtos por categoria
4. Validar schema da resposta
5. Testar limite de produtos retornados

### Estrutura esperada:

    tests/
    └── test_products_api.py

### Exemplo de teste:

    def test_listar_produtos():
        response = requests.get("https://fakestoreapi.com/products")
        assert response.status_code == 200
        assert len(response.json()) > 0
        assert "title" in response.json()[0]

### Validações necessárias:
- Status codes corretos
- Schema dos produtos
- Categorias disponíveis: electronics, jewelery, men's clothing, women's clothing

## Exercício 3: Teste CRUD Completo (REST)

Usando JSONPlaceholder (https://jsonplaceholder.typicode.com/), implemente teste CRUD completo para "todos".

### Endpoint: /todos

### Operações a testar:

    # CREATE
    POST /todos
    {
        "title": "Minha tarefa",
        "completed": false,
        "userId": 1
    }
    
    # READ
    GET /todos/1
    
    # UPDATE
    PATCH /todos/1
    {
        "completed": true
    }
    
    # DELETE
    DELETE /todos/1
    
    # VERIFY
    GET /todos/1  # Deve retornar 404 ou {}

### Estrutura esperada:

    tests/
    └── test_todos_crud.py

### Implementação:
- Use fixtures para criar dados de teste
- Implemente teardown para limpar dados
- Teste casos de erro (ex: criar todo sem título)

## Exercício 4: Page Object Model (Web)

Refatore os testes do Exercício 1 usando Page Object Model.

### Estrutura esperada:

    pages/
    ├── base_page.py
    ├── login_page.py
    └── dashboard_page.py
    tests/
    └── test_login_pom.py

### Classe LoginPage deve ter:
- Locators como atributos da classe
- Métodos: abrir(), preencher_email(), preencher_senha(), clicar_login()
- Método: fazer_login(email, senha) que combina as ações

### Classe DashboardPage deve ter:
- Método: esta_logado() que retorna True/False
- Método: obter_mensagem_boas_vindas()

### Exemplo:

    class LoginPage(BasePage):
        EMAIL_INPUT = (By.ID, "username")
        PASSWORD_INPUT = (By.ID, "password")
        LOGIN_BUTTON = (By.ID, "submit")
        
        def fazer_login(self, username, password):
            self.digitar(self.EMAIL_INPUT, username)
            self.digitar(self.PASSWORD_INPUT, password)
            self.clicar(self.LOGIN_BUTTON)

## Exercício 5: Testes Parametrizados (REST + Web)

Crie testes parametrizados para validar múltiplos cenários de entrada.

### Parte A: Validação de Email (REST)

Cenários de email inválido:

    emails_invalidos = [
        "sem-arroba.com",
        "@sem-usuario.com",
        "sem-dominio@",
        "espacos no meio@teste.com",
        "caracteres!especiais@teste.com",
        "..pontos@teste.com",
        "teste@",
        "@teste.com"
    ]

Implementação com pytest:

    @pytest.mark.parametrize("email_invalido", emails_invalidos)
    def test_validacao_email_api(email_invalido):
        response = requests.post("https://reqres.in/api/register", json={
            "email": email_invalido,
            "password": "senha123"
        })
        assert response.status_code == 400

### Parte B: Validação de Senhas (REST)

Cenários de senha inválida:

    senhas_invalidas = [
        ("123", "muito curta"),
        ("semNumero", "sem número"),
        ("semmaiuscula123", "sem maiúscula"),
        ("12345678", "só números"),
        ("ab", "muito curta")
    ]

Implementação:

    @pytest.mark.parametrize("senha,motivo", senhas_invalidas)
    def test_validacao_senha(senha, motivo):
        response = requests.post("https://reqres.in/api/register", json={
            "email": "test@test.com",
            "password": senha
        })
        assert response.status_code == 400

### Parte C: Busca Parametrizada (Web)

Testar busca com múltiplos termos:

    @pytest.mark.parametrize("termo_busca", [
        "Python",
        "Selenium",
        "Pytest",
        "API Testing",
        "Automation"
    ])
    def test_busca_google(chrome_driver, termo_busca):
        driver = chrome_driver
        driver.get("https://www.google.com")
        
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(termo_busca)
        search_box.submit()
        
        # Aguardar resultados
        time.sleep(2)
        
        assert termo_busca.lower() in driver.page_source.lower()

### Estrutura esperada:

    tests/
    ├── test_validacoes_parametrizadas.py
    └── test_busca_parametrizada.py

## Submissão dos Exercícios

### Estrutura do repositório:

    exercicios-teste-software/
    ├── README.md
    ├── requirements.txt
    ├── pytest.ini
    ├── exercicio01/
    │   └── tests/
    ├── exercicio02/
    │   └── tests/
    ├── exercicio03/
    │   └── tests/
    ├── exercicio04/
    │   ├── tests/
    │   └── pages/
    └── exercicio05/
        └── tests/

### Cada exercício deve conter:
1. Código dos testes
2. README.md com instruções de execução
3. Relatório de execução (HTML ou texto)
4. Print ou log mostrando testes passando

### Arquivo requirements.txt:

    selenium==4.15.2
    webdriver-manager==4.0.1
    requests==2.31.0
    pytest==7.4.3
    pytest-html==4.1.1

### Entrega:
- Repositório Git com código
- Link para o repositório no Moodle da disciplina
- Prazo: padrão

## Recursos de Apoio

### Documentação
- Pytest: https://docs.pytest.org/
- Selenium: https://selenium-python.readthedocs.io/
- Requests: https://requests.readthedocs.io/

### Exemplos de código
- Repositório da disciplina: `aula10-testes-web-rest/exemplos/`
