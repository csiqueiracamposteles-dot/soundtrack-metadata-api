# Soundtrack Metadata API

API REST desenvolvida em **FastAPI** para localizar e consultar metadados de trilhas sonoras de filmes e séries por meio da integração com **Spotify**, **TMDb** e **MusicBrainz**.

A API identifica automaticamente o audiovisual informado, localiza a trilha sonora correspondente e retorna informações como álbum, faixas, ISRC, compositores e links do Spotify.

---

# Funcionalidades

* Pesquisa de trilhas sonoras por título
* Suporte para filmes e séries
* Integração com TMDb para identificação do audiovisual
* Integração com Spotify para localização de álbuns e faixas
* Consulta de ISRC das faixas
* Identificação de compositores via MusicBrainz
* Cache local para otimização das consultas
* Documentação automática com Swagger/OpenAPI

---

# Tecnologias

* Python
* FastAPI
* Spotify Web API
* TMDb API
* MusicBrainz API
* SQLite
* Docker

---

# Como executar

## Clone o repositório

```bash
git clone https://github.com/SEU_USUARIO/soundtrack-metadata-api.git
```

## Instale as dependências

```bash
pip install -r requirements.txt
```

## Configure as variáveis de ambiente

Crie um arquivo `.env` baseado no arquivo `.env.example`.

Exemplo:

```env
SPOTIFY_CLIENT_ID=seu_client_id
SPOTIFY_CLIENT_SECRET=seu_client_secret
TMDB_TOKEN=seu_token_tmdb
```

## Execute a aplicação

```bash
uvicorn app.main:app --reload
```

---

# Documentação

Após iniciar a aplicação, acesse:

```
http://localhost:8000/api/docs
```

---

# Endpoint

## Buscar trilha sonora

### GET

```http
GET /api/soundtrack?titulo=Moana
```

### POST

```http
POST /api/soundtrack
```

```json
{
    "titulo": "Moana"
}
```

---

# Exemplo de resposta

```json
{
    "titulo": "Moana",
    "ano": "2016",
    "tipo": "movie",
    "album": "Moana (Original Motion Picture Soundtrack)",
    "faixas": [
        {
            "musica": "How Far I'll Go",
            "interprete": "Auli'i Cravalho",
            "isrc": "USWD11674632",
            "spotify_link": "https://open.spotify.com/...",
            "autor": "Lin-Manuel Miranda"
        }
    ]
}
```

---

# Estrutura do projeto

```
app/
├── core/
├── routers/
├── services/
├── utils/
└── main.py
```

---

# Licença

Este projeto foi desenvolvido para fins de estudo, demonstração técnica e portfólio.
