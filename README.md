<div align="center">

# 📚 EVOLUÇÃO FLASK

### API de gerenciamento de livros — organize, acompanhe e favorite suas leituras

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Alembic](https://img.shields.io/badge/Flask--Migrate-Alembic-6BA81E?style=for-the-badge)
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow?style=for-the-badge)

[📖 Sobre](#-sobre-o-projeto) •
[✨ Funcionalidades](#-funcionalidades) •
[🗃️ Modelo de dados](#️-modelo-de-dados) •
[🚀 Como executar](#-como-executar) •
[📂 Estrutura](#-estrutura-do-projeto) •
[🗺️ Roadmap](#️-roadmap)

</div>

---

## 📖 Sobre o projeto

O **EVOLUÇÃO FLASK** é uma aplicação back-end construída com **Flask** para gerenciar uma biblioteca pessoal de livros. A ideia é ter um lugar único onde você cadastra seus livros e acompanha o que está **lendo**, o que já **finalizou** e quais são seus **favoritos**.

Os dados ficam em um banco **PostgreSQL**, acessado via **SQLAlchemy (ORM)**, e a evolução da estrutura do banco é controlada com **Flask-Migrate / Alembic**. As respostas da API são pensadas para sair em **JSON**.

> 🌱 O projeto está em fase inicial: a base (configuração, banco e modelo `Book`) já está montada e os endpoints estão sendo construídos.

---

## ✨ Funcionalidades

| | Funcionalidade | Situação |
|---|---|---|
| 🔍 | Consultar livros | 🛠️ Planejado |
| ➕ | Cadastrar livros | 🛠️ Planejado |
| ✏️ | Editar / atualizar livros | 🛠️ Planejado |
| 🗑️ | Deletar livros | 🛠️ Planejado |
| ⭐ | Favoritar livros | 🛠️ Planejado |
| 📖 | Marcar livros em leitura | 🛠️ Planejado |
| ✅ | Marcar livros finalizados | 🛠️ Planejado |
| 🧱 | Modelo `Book` com UUID e status de leitura | ✔️ Estruturado |
| 🔌 | Configuração do banco com SQLAlchemy | ✔️ Estruturado |

---

## 🗃️ Modelo de dados

Entidade **`book`**:

| Campo | Tipo | Obrigatório | Descrição |
|---|---|:---:|---|
| 🔑 `id` | `UUID` | ✔️ | Chave primária, gerada automaticamente |
| 📕 `title` | `String(255)` | ✔️ | Título do livro |
| ✍️ `author` | `String(255)` | ✔️ | Autor(a) do livro |
| 📝 `description` | `Text` | ✔️ | Descrição / sinopse |
| ⭐ `is_favorite` | `Boolean` | ✔️ | Se é favorito (padrão: `False`) |
| 📖 `is_reading` | `Boolean` | ✔️ | Se está em leitura (padrão: `False`) |
| ✅ `is_finished` | `Boolean` | ✔️ | Se já foi finalizado (padrão: `False`) |

O método `as_dict()` converte o objeto `Book` em um dicionário Python (com o `id` convertido para texto), pronto para ser serializado em **JSON** na resposta HTTP.

```json
{
  "id": "3f2b8c1e-5a47-4d1f-9c0a-7e6d2b9a1f10",
  "title": "Título do livro",
  "author": "Nome do autor",
  "description": "Sinopse do livro",
  "is_favorite": false,
  "is_reading": true,
  "is_finished": false
}
```

---

## 🔄 Fluxo da aplicação

```mermaid
flowchart LR
    A[👤 Cliente] -->|requisição HTTP| B[⚙️ Flask - app.py]
    B --> C[🧱 Modelo Book]
    C --> D[🔌 SQLAlchemy - db.py]
    D --> E[(🐘 PostgreSQL)]
    E --> D
    D --> C
    C -->|as_dict| B
    B -->|resposta JSON| A
```

---

## 🛠️ Tecnologias

| Tecnologia | Uso |
|---|---|
| 🐍 **Python** | Linguagem principal |
| 🌶️ **Flask** | Framework web |
| 🧩 **Flask-SQLAlchemy / SQLAlchemy** | ORM para acesso ao banco |
| 🐘 **PostgreSQL** (`psycopg`) | Banco de dados |
| 🔄 **Flask-Migrate / Alembic** | Controle de migrações do banco |
| 🔐 **python-dotenv** | Variáveis de ambiente via arquivo `.env` |

---

## 🚀 Como executar

### Pré-requisitos

- [Python 3.10+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)
- [PostgreSQL](https://www.postgresql.org/download/) com um banco criado para o projeto

### Passo a passo

```bash
# 1️⃣ Clone o repositório
git clone https://github.com/julianabcor/EVOLUCAO-FLASK.git
cd EVOLUCAO-FLASK

# 2️⃣ Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# 3️⃣ Instale as dependências
pip install -r requirements.txt
```

### 🔐 Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com a URL de conexão do seu banco PostgreSQL:

```env
database=postgresql+psycopg://usuario:senha@localhost:5432/nome_do_banco
```

> 🔒 O `.env` já está no `.gitignore`, então suas credenciais não vão para o GitHub.

---

## 📂 Estrutura do projeto

```
📦 EVOLUCAO-FLASK
 ┣ 📂 models
 ┃ ┣ 📜 __init__.py
 ┃ ┗ 📜 book.py          # Modelo Book (entidade do banco)
 ┣ 📜 app.py             # Aplicação Flask e endpoints
 ┣ 📜 db.py              # Instância do SQLAlchemy (ORM)
 ┣ 📜 migrations.py      # Controle das alterações estruturais do banco
 ┣ 📜 requirements.txt   # Dependências do projeto
 ┣ 📜 .gitignore
 ┗ 📜 README.md
```

---

## 🗺️ Roadmap

- [x] Estrutura inicial do projeto com Flask
- [x] Instância do SQLAlchemy (`db.py`)
- [x] Modelo `Book` com UUID e status de leitura
- [x] Método `as_dict()` para serialização em JSON
- [ ] Finalizar a configuração da aplicação e conexão com o banco
- [ ] Configurar migrações com Flask-Migrate
- [ ] Endpoint para **consultar** livros
- [ ] Endpoint para **cadastrar** livros
- [ ] Endpoint para **editar / atualizar** livros
- [ ] Endpoint para **deletar** livros
- [ ] Endpoint para **favoritar** livros
- [ ] Listagem de livros **em leitura**
- [ ] Listagem de livros **finalizados**
- [ ] Deploy online

---

## 🤝 Contribuindo

Contribuições são bem-vindas!

1. Faça um fork do projeto
2. Crie uma branch: `git checkout -b minha-feature`
3. Commit: `git commit -m "Adiciona minha feature"`
4. Push: `git push origin minha-feature`
5. Abra um Pull Request

---

## 👩‍💻 Autora

<div align="center">

Feito com 💜 por **Juliana**

[![GitHub](https://img.shields.io/badge/GitHub-julianabcor-181717?style=for-the-badge&logo=github)](https://github.com/julianabcor)

⭐ Se gostou do projeto, deixe uma estrela!

</div>
