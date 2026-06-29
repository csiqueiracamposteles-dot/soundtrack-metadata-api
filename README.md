#  Music Matching API

API para busca e matching de músicas utilizando Spotify.

---

##  Como rodar

1. Clone o projeto
2. Crie um arquivo `.env`:

SPOTIFY_CLIENT_ID=seu_id
SPOTIFY_CLIENT_SECRET=seu_secret

3. Instale dependências:

pip install -r requirements.txt

4. Rode a API:

uvicorn app.main:app --reload

---

##  Importante

Para rodar o projeto, utilize suas próprias credenciais do Spotify.

---

##  Endpoint

GET /consulta?artista=queen

---

##  JSON (POST)

POST /consulta

{
  "artista": "queen"
}