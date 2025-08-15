# CliniOps.AI — Infra + IA para Clínica (MVP)

Plataforma demo, com base de protocolos clínicos, busca semântica simples e sugestões de apoio. **Sem dados sensíveis; usa SQLite** por padrão para facilitar o teste local.

## 📌 Funcionalidades atuais
- **API REST (FastAPI)**:
  - `GET /health` — Verifica se a API está ativa.
  - `POST /protocols` — Cadastra protocolo clínico.
  - `GET /protocols?q=...` — Busca protocolos por termo (similaridade).
  - `POST /ai/suggest` — Sugere protocolos relacionados ao texto informado e fornece lembretes simples baseados em regras.
- **Banco de dados**:
  - SQLite local (`cliniops.db`), criado automaticamente.
  - Tabela `protocols` com embedding simples para busca.
  - Seed inicial com 3 protocolos de exemplo.
- **Painel Web (Streamlit)**:
  - Aba **Buscar Protocolos**: pesquisa e cadastro de novos protocolos.
  - Aba **IA de Suporte**: insere sintomas/contexto e recebe sugestões + lembretes.
- **Código limpo**:
  - Organização por camadas (`api/`, `core/`, `ai/`, `app/`).
  - SQLAlchemy + Pydantic.
  - Embedding mock determinístico (hash → vetor) para rodar leve.

## 🚀 Como executar localmente

### 1. Clonar repositório
```bash
git clone https://github.com/CaikRian/cliniops-ai.git
cd cliniops-ai
```

### 2. Criar ambiente virtual e instalar dependências
```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Rodar a API
```bash
python -m uvicorn src.api.main:app --reload
```
- Acesse http://127.0.0.1:8000/docs para testar.

### 4. Rodar o painel Streamlit
Em outro terminal (com `.venv` ativo):
```bash
streamlit run src/app/dashboard.py
```
- Acesse: http://localhost:8501

## 🛠 Tecnologias utilizadas
- **Python 3.11**
- **FastAPI**
- **Streamlit**
- **SQLAlchemy**
- **Pydantic**
- **NumPy**

## 📄 Licença
MIT — uso livre para fins acadêmicos e profissionais.
