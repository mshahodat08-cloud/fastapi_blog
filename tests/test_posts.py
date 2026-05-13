import pytest
from app import schemas

# ─── BARCHA POSTLAR ───────────────────────────
def test_get_all_posts(client, test_posts):
    response = client.get("/posts/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(test_posts)

# ─── BITTA POST ───────────────────────────────
def test_get_post(client, test_posts):
    response = client.get(f"/posts/{test_posts[0].id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_posts[0].id
    assert data["title"] == test_posts[0].title

# ─── MAVJUD BO'LMAGAN POST ────────────────────
def test_get_post_not_found(client):
    response = client.get("/posts/99999")
    assert response.status_code == 404

# ─── POST YARATISH (token bilan) ──────────────
def test_create_post(authorized_client):
    response = authorized_client.post(
        "/posts/",
        json={
            "title": "Yangi post",
            "content": "Yangi kontent", # MODELS dagi kabi 'content'
            "published": True
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Yangi post"
    assert data["content"] == "Yangi kontent"
    assert "id" in data

# ─── POST YARATISH (token YO'Q) ───────────────
def test_create_post_unauthorized(client):
    response = client.post(
        "/posts/",
        json={"title": "Post", "content": "Kontent"}
    )
    assert response.status_code == 401

# ─── DEFAULT PUBLISHED = TRUE ─────────────────
def test_create_post_default_published(authorized_client):
    response = authorized_client.post(
        "/posts/",
        json={"title": "Post", "content": "Kontent"}
    )
    assert response.status_code == 201
    assert response.json()["published"] == True

# ─── POST YANGILASH ───────────────────────────
def test_update_post(authorized_client, test_posts):
    response = authorized_client.put(
        f"/posts/{test_posts[0].id}",
        json={
            "title": "Yangilangan sarlavha",
            "content": "Yangilangan kontent",
            "published": True
        }
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Yangilangan sarlavha"

# ─── BOSHQANING POSTINI YANGILASH ─────────────
def test_update_other_user_post(authorized_client, db):
    from app import models
    from app.utils.hashing import hash_password

    # Ikkinchi user
    other_user = models.User(
        username="other_upd",
        email="other_upd@example.com",
        password=hash_password("password123")
    )
    db.add(other_user)
    db.commit()
    db.refresh(other_user)

    # Ikkinchi user posti
    other_post = models.Post(
        title="Boshqaning posti",
        content="Boshqa kontent", # 'content' ishlatildi!
        owner_id=other_user.id
    )
    db.add(other_post)
    db.commit()

    response = authorized_client.put(
        f"/posts/{other_post.id}",
        json={"title": "Urindim", "content": "Yangilash", "published": True}
    )
    assert response.status_code == 403

# ─── POST O'CHIRISH ───────────────────────────
def test_delete_post(authorized_client, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 204

# ─── O'CHIRILGAN POSTNI TEKSHIRISH ────────────
def test_delete_post_check(authorized_client, test_posts):
    target_id = test_posts[0].id
    authorized_client.delete(f"/posts/{target_id}")
    response = authorized_client.get(f"/posts/{target_id}")
    assert response.status_code == 404

# ─── MAVJUD BO'LMAGAN POSTNI O'CHIRISH ────────
def test_delete_post_not_found(authorized_client):
    response = authorized_client.delete("/posts/99999")
    assert response.status_code == 404

# ─── BOSHQANING POSTINI O'CHIRISH ─────────────
def test_delete_other_user_post(authorized_client, db):
    from app import models
    from app.utils.hashing import hash_password

    other_user = models.User(
        username="other_del",
        email="other_del@example.com",
        password=hash_password("password123")
    )
    db.add(other_user)
    db.commit()
    db.refresh(other_user)

    other_post = models.Post(
        title="Boshqaning posti",
        content="Kontent", # 'content' ishlatildi!
        owner_id=other_user.id
    )
    db.add(other_post)
    db.commit()

    response = authorized_client.delete(f"/posts/{other_post.id}")
    assert response.status_code == 403

# ─── PAGINATION ───────────────────────────────
def test_get_posts_pagination(client, test_posts):
    response = client.get("/posts/?limit=2&skip=0")
    assert response.status_code == 200
    assert len(response.json()) == 2

# ─── QIDIRUV ──────────────────────────────────
def test_get_posts_search(client, test_posts):
    # Test posts ichida "Birinchi" so'zi borligiga ishonch hosil qiling
    response = client.get("/posts/?search=Birinchi")
    assert response.status_code == 200