
import pytest
import requests

BASE_URL = "https://reqres.in/api"

# Parte A: Cenários de email inválido
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

@pytest.mark.parametrize("email_invalido", emails_invalidos)
def test_validacao_email_api(email_invalido):
    """
    Testa que emails inválidos retornam erro 400 na API de registro.
    Nota: reqres.in pode ser permissivo; ajuste conforme comportamento real.
    """
    response = requests.post(
        f"{BASE_URL}/register",
        json={"email": email_invalido, "password": "senha123"},
        timeout=20
    )
    
    # Valida que retorna erro (400 ou 4xx)
    # Nota: reqres.in pode retornar 400 com mensagem "Missing email or username"
    assert response.status_code >= 400, f"Email '{email_invalido}' deveria ser rejeitado"


# Parte B: Cenários de senha inválida
senhas_invalidas = [
    ("123", "muito curta"),
    ("semNumero", "sem número"),
    ("semmaiuscula123", "sem maiúscula"),
    ("12345678", "só números"),
    ("ab", "muito curta")
]

@pytest.mark.parametrize("senha,motivo", senhas_invalidas)
def test_validacao_senha(senha, motivo):
    """
    Testa que senhas inválidas retornam erro 400 na API de registro.
    O parâmetro 'motivo' serve para documentar o cenário no relatório.
    """
    response = requests.post(
        f"{BASE_URL}/register",
        json={"email": "test@test.com", "password": senha},
        timeout=20
    )
    
    # Valida que retorna erro (400 ou 4xx)
    # Nota: reqres.in pode não validar complexidade de senha; ajuste conforme API real
    assert response.status_code >= 400, f"Senha '{senha}' ({motivo}) deveria ser rejeitada"


# Testes extras: combinações de email e senha inválidos
@pytest.mark.parametrize("email,senha", [
    ("invalido.com", "123"),
    ("@teste.com", "abc"),
    ("teste@", "12345678"),
])
def test_validacao_email_e_senha_invalidos(email, senha):
    """Testa combinações de email e senha inválidos"""
    response = requests.post(
        f"{BASE_URL}/register",
        json={"email": email, "password": senha},
        timeout=20
    )
    assert response.status_code >= 400


# Teste com dados válidos (controle positivo)
def test_registro_valido():
    """
    Teste de controle: registro com dados válidos.
    Nota: reqres.in exige emails específicos para sucesso (ex: eve.holt@reqres.in)
    """
    response = requests.post(
        f"{BASE_URL}/register",
        json={"email": "eve.holt@reqres.in", "password": "pistol"},
        timeout=20
    )
    
    # Deve retornar 200 ou 201 com token
    assert response.status_code in (200, 201)
    body = response.json()
    assert "token" in body or "id" in body