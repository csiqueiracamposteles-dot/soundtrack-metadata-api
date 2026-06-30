# 🎬 Soundtrack Metadata API

API REST desenvolvida em **FastAPI** para localizar e consultar metadados de trilhas sonoras de filmes e séries por meio da integração com múltiplos serviços públicos.

A aplicação identifica automaticamente o audiovisual informado, localiza o álbum oficial da trilha sonora e retorna informações estruturadas sobre faixas, intérpretes, compositores, códigos ISRC e links para o Spotify.

Além da API, este repositório inclui um **pipeline completo de processamento em lote**, demonstrando como consumir a API em aplicações reais de enriquecimento e validação de dados.

---

# 🚀 Funcionalidades

- Pesquisa de trilhas sonoras por título de filmes e séries
- Identificação automática do audiovisual utilizando TMDb
- Localização do álbum oficial no Spotify
- Extração das faixas da trilha sonora
- Consulta de códigos ISRC
- Identificação de compositores utilizando MusicBrainz
- Cache local utilizando SQLite
- Retry automático para chamadas às APIs externas
- Documentação automática com Swagger/OpenAPI
- Exemplo completo de processamento em lote

---

# 🛠 Tecnologias

- Python 3.12
- FastAPI
- Requests
- Pydantic
- RapidFuzz
- SQLite
- Docker
- Spotify Web API
- TMDb API
- MusicBrainz API

---

# 🏗 Arquitetura

```text
                        Client
                           │
                           ▼
                    FastAPI REST API
                           │
                    SQLite Cache
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
     Spotify API       TMDb API      MusicBrainz API
```

---

# 📁 Estrutura do Projeto

```text
soundtrack-metadata-api/
│
├── app/
│   ├── core/
│   ├── routers/
│   ├── services/
│   ├── utils/
│   └── main.py
│
├── examples/
│   └── soundtrack-matching-pipeline/
│       ├── data/
│       ├── pipeline/
│       ├── run_pipeline.py
│       └── README.md
│
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

---

# ⚙️ Como executar

## 1. Clone o repositório

```bash
git clone https://github.com/SEU_USUARIO/soundtrack-metadata-api.git
```

## 2. Instale as dependências

```bash
pip install -r requirements.txt
```

## 3. Configure as variáveis de ambiente

Crie um arquivo `.env` baseado em `.env.example`.

Exemplo:

```env
SPOTIFY_CLIENT_ID=seu_client_id
SPOTIFY_CLIENT_SECRET=seu_client_secret
TMDB_TOKEN=seu_tmdb_token
```

## 4. Execute a aplicação

```bash
uvicorn app.main:app --reload
```

---

# 📖 Documentação

Após iniciar a aplicação:

Swagger

```text
http://localhost:8000/api/docs
```

OpenAPI

```text
http://localhost:8000/api/openapi.json
```

Health Check

```text
http://localhost:8000/healthz
```

---

# 🔎 Exemplos de utilização

## Consulta via GET

```http
GET /api/soundtrack?titulo=Moana
```

---

## Consulta via POST

```http
POST /api/soundtrack
```

```json
{
    "titulo": "Moana"
}
```

---

# 📦 Exemplo de resposta

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

# 📚 Exemplo incluído no repositório

Este projeto inclui um exemplo completo de utilização da API localizado em:

```text
examples/
└── soundtrack-matching-pipeline/
```

O exemplo demonstra um fluxo completo de processamento em lote utilizando a API.

Fluxo:

```text
movies.csv
        │
        ▼
Carregamento dos títulos
        │
        ▼
Soundtrack Metadata API
        │
        ▼
Spotify
TMDb
MusicBrainz
        │
        ▼
Enriquecimento dos metadados
        │
        ▼
Matching utilizando RapidFuzz
        │
        ▼
Relatório Final
```

O pipeline gera automaticamente:

```text
enriched_tracks.csv
matched_tracks.csv
soundtrack_report.csv
```

Para executar o exemplo:

```bash
cd examples/soundtrack-matching-pipeline

python run_pipeline.py
```

---

# 💡 Objetivo do Projeto

Este projeto foi desenvolvido para demonstrar a construção de APIs REST utilizando FastAPI, integração entre múltiplas APIs públicas, técnicas de enriquecimento de metadados musicais e organização de aplicações em camadas.

O exemplo incluído no repositório demonstra como reutilizar a API em um pipeline de processamento de dados, aplicando algoritmos de similaridade e geração de relatórios.

