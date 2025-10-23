import requests
from jsonschema import validate

BASE = "https://fakestoreapi.com"

PRODUCT_SCHEMA = {
    "type": "object",
    "required": ["id", "title", "price", "description", "category", "image"],
    "properties": {
        "id": {"type": "number"},
        "title": {"type": "string"},
        "price": {"type": "number"},
        "description": {"type": "string"},
        "category": {"type": "string"},
        "image": {"type": "string"},
        "rating": {
            "type": "object",
            "required": ["rate", "count"],
            "properties": {
                "rate": {"type": "number"},
                "count": {"type": "number"}
            }
        }
    }
}

def test_listar_produtos():
    r = requests.get(f"{BASE}/products", timeout=20)
    assert r.status_code == 200
    itens = r.json()
    assert isinstance(itens, list) and len(itens) > 0
    validate(instance=itens[0], schema=PRODUCT_SCHEMA)

def test_buscar_produto_por_id():
    r_all = requests.get(f"{BASE}/products", timeout=20)
    first_id = r_all.json()[0]["id"]

    r = requests.get(f"{BASE}/products/{first_id}", timeout=20)
    assert r.status_code == 200
    validate(instance=r.json(), schema=PRODUCT_SCHEMA)

def test_filtrar_por_categoria():
    categorias_validas = {"electronics", "jewelery", "men's clothing", "women's clothing"}
    r = requests.get(f"{BASE}/products/categories", timeout=20)
    assert r.status_code == 200
    cats = set(r.json())
    assert categorias_validas.issubset(cats)

    # pegar uma categoria e conferir listagem
    cat = "electronics"
    r2 = requests.get(f"{BASE}/products/category/{cat}", timeout=20)
    assert r2.status_code == 200
    for p in r2.json():
        assert p["category"] == cat

def test_limite_de_produtos():
    r = requests.get(f"{BASE}/products", params={"limit": 5}, timeout=20)
    assert r.status_code == 200
    assert len(r.json()) == 5