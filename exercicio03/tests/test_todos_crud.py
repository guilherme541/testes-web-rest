"""
Exercício 3: Teste CRUD Completo (REST)
Testes de operações CRUD na API JSONPlaceholder
"""
import requests
import pytest

BASE = "https://jsonplaceholder.typicode.com"

@pytest.fixture
def novo_todo():
    """
    Fixture que cria um novo todo e retorna seus dados.
    Teardown: Como JSONPlaceholder não persiste dados reais,
    não há necessidade de limpeza.
    """
    payload = {"title": "Minha tarefa", "completed": False, "userId": 1}
    r = requests.post(f"{BASE}/todos", json=payload, timeout=20)
    assert r.status_code in (201, 200), f"Falha ao criar todo: {r.status_code}"
    todo = r.json()
    
    yield todo
    
    # Teardown: tentativa de deletar (não persiste no JSONPlaceholder)
    if "id" in todo:
        try:
            requests.delete(f"{BASE}/todos/{todo['id']}", timeout=10)
        except:
            pass  # Ignora erros no teardown


def test_create_todo():
    """CREATE: Testa criação de um novo todo"""
    payload = {
        "title": "Minha tarefa",
        "completed": False,
        "userId": 1
    }
    
    r = requests.post(f"{BASE}/todos", json=payload, timeout=20)
    
    # Valida status code
    assert r.status_code in (201, 200)
    
    # Valida corpo da resposta
    body = r.json()
    assert isinstance(body, dict)
    assert body.get("title") == payload["title"]
    assert body.get("completed") == payload["completed"]
    assert body.get("userId") == payload["userId"]
    assert "id" in body


def test_read_todo():
    """READ: Testa leitura de um todo existente"""
    todo_id = 1
    
    r = requests.get(f"{BASE}/todos/{todo_id}", timeout=20)
    
    # Valida status code
    assert r.status_code == 200
    
    # Valida estrutura da resposta
    body = r.json()
    assert body.get("id") == todo_id
    assert "title" in body
    assert "userId" in body
    assert "completed" in body
    assert isinstance(body["completed"], bool)


def test_update_todo():
    """UPDATE: Testa atualização de um todo com PATCH"""
    todo_id = 1
    payload = {"completed": True}
    
    r = requests.patch(f"{BASE}/todos/{todo_id}", json=payload, timeout=20)
    
    # Valida status code
    assert r.status_code == 200
    
    # Valida que o campo foi atualizado na resposta
    body = r.json()
    assert body.get("completed") is True


def test_delete_todo():
    """DELETE: Testa exclusão de um todo"""
    todo_id = 1
    
    r = requests.delete(f"{BASE}/todos/{todo_id}", timeout=20)
    
    # Valida status code (200 OK ou 204 No Content)
    assert r.status_code in (200, 204)


def test_crud_completo(novo_todo):
    """
    Teste CRUD completo em sequência usando fixture.
    Nota: JSONPlaceholder não persiste dados reais, então
    a verificação final pode não retornar 404.
    """
    todo = novo_todo
    todo_id = todo.get("id")
    
    # CREATE já foi feito pela fixture
    assert todo_id is not None
    assert todo.get("title") == "Minha tarefa"
    
    # READ: Tenta ler o todo criado
    # Nota: JSONPlaceholder pode não retornar o ID criado via POST
    # então usamos um ID conhecido (1) para garantir que o READ funciona
    r_read = requests.get(f"{BASE}/todos/1", timeout=20)
    assert r_read.status_code == 200
    assert "title" in r_read.json()
    
    # UPDATE: Atualiza o todo
    r_patch = requests.patch(
        f"{BASE}/todos/1",
        json={"completed": True},
        timeout=20
    )
    assert r_patch.status_code == 200
    assert r_patch.json().get("completed") is True
    
    # DELETE: Remove o todo
    r_del = requests.delete(f"{BASE}/todos/1", timeout=20)
    assert r_del.status_code in (200, 204)
    
    # VERIFY: Tenta ler novamente
    # Nota: JSONPlaceholder não persiste, então pode retornar 200 ainda
    r_verify = requests.get(f"{BASE}/todos/1", timeout=20)
    # Aceita tanto 404 (ideal) quanto 200 (comportamento do fake API)
    assert r_verify.status_code in (200, 404)


def test_criar_todo_sem_titulo():
    """Teste de erro: criar todo sem título"""
    payload = {"completed": False, "userId": 1}
    
    r = requests.post(f"{BASE}/todos", json=payload, timeout=20)
    
    # JSONPlaceholder é permissivo e aceita mesmo sem título
    assert r.status_code in (201, 200)
    
    body = r.json()
    assert body.get("completed") is False
    assert body.get("userId") == 1
    # Título pode estar ausente ou None
    assert body.get("title") in (None, "")


def test_criar_todo_sem_userid():
    """Teste de erro: criar todo sem userId"""
    payload = {"title": "Tarefa sem usuário", "completed": False}
    
    r = requests.post(f"{BASE}/todos", json=payload, timeout=20)
    
    # JSONPlaceholder aceita mesmo sem userId
    assert r.status_code in (201, 200)


def test_buscar_todo_inexistente():
    """Teste de erro: buscar todo com ID inexistente"""
    todo_id = 999999
    
    r = requests.get(f"{BASE}/todos/{todo_id}", timeout=20)
    
    # Pode retornar 404 ou 200 com objeto vazio
    assert r.status_code in (200, 404)
    
    if r.status_code == 200:
        body = r.json()
        # Se retornar 200, deve ser objeto vazio
        assert body == {} or body.get("id") is None


def test_atualizar_todo_inexistente():
    """Teste de erro: atualizar todo inexistente"""
    todo_id = 999999
    
    r = requests.patch(
        f"{BASE}/todos/{todo_id}",
        json={"completed": True},
        timeout=20
    )
    
    # JSONPlaceholder pode retornar 200 mesmo para IDs inexistentes
    assert r.status_code in (200, 404)


def test_deletar_todo_inexistente():
    """Teste de erro: deletar todo inexistente"""
    todo_id = 999999
    
    r = requests.delete(f"{BASE}/todos/{todo_id}", timeout=20)
    
    # JSONPlaceholder pode retornar 200 mesmo para IDs inexistentes
    assert r.status_code in (200, 204, 404)