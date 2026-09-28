# FastAPI - REST API com Python (Backend Completo)

Este é o projeto desenvolvido durante o curso de **FastAPI** da [Hashtag Programação](https://www.youtube.com/watch?v=BtIy2aD8k_w). O objetivo deste projeto é construir uma API RESTful completa, abordando desde a estruturação inicial até a integração com banco de dados e autenticação.

## 🚀 Tecnologias Utilizadas

O projeto utiliza as seguintes bibliotecas e ferramentas do ecossistema Python:

*   **[FastAPI](https://fastapi.tiangolo.com/):** Framework web moderno e rápido para construção de APIs com Python.
*   **[Uvicorn](https://www.uvicorn.org/):** Servidor ASGI super rápido, utilizado para rodar a aplicação.
*   **[SQLAlchemy](https://www.sqlalchemy.org/):** ORM (Object Relational Mapper) para comunicação e integração com o banco de dados.
*   **[Passlib](https://passlib.readthedocs.io/):** Biblioteca para hashing de senhas utilizando `bcrypt`.
*   **[Python-Jose](https://python-jose.readthedocs.io/):** Implementação de tokens JWT com suporte a `cryptography` para autenticação.
*   **python-dotenv:** Para gerenciamento de variáveis de ambiente de forma segura.
*   **python-multipart:** Para suporte ao processamento de formulários na API.

## ⚙️ Estrutura do Projeto

Baseado nas aulas, o escopo de desenvolvimento cobre:
1. Apresentação e configuração do ambiente.
2. Estruturação do arquivo principal (`main.py`) e configurações iniciais do FastAPI.
3. Criação de Rotas e Endpoints para processamento de requisições.
4. Integração com Banco de Dados e configuração do ORM.
5. Criação de Modelos de Dados (Data Models).
6. Autenticação e Segurança da API.

## 💻 Como Executar o Projeto Localmente

Siga o passo a passo abaixo para rodar a API no seu computador.

### 1. Clonar ou baixar o projeto
```bash
# Clone o repositório ou navegue até a pasta do projeto
cd seu-repositorio
```

### 2. Criar e ativar um ambiente virtual (Recomendado)
```bash
# No Windows
python -m venv venv
venv\Scripts\activate

# No Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar as dependências
Instale todos os pacotes necessários utilizando o `pip`. 

*(Nota para usuários de Linux/macOS utilizando ZSH: é importante utilizar aspas nos pacotes com colchetes para evitar erros no terminal, conforme o comando abaixo).*

```bash
pip install fastapi uvicorn sqlalchemy "passlib[bcrypt]" "python-jose[cryptography]" python-dotenv python-multipart
```

### 4. Rodar o Servidor
Com todas as dependências instaladas, inicie o servidor com o Uvicorn:

```bash
uvicorn main:app --reload
```
*O parâmetro `--reload` faz com que o servidor reinicie automaticamente sempre que uma mudança for salva no código (útil para o desenvolvimento).*

### 5. Acessar a Documentação Automática
Acesse o navegador para ver a documentação interativa gerada automaticamente pelo FastAPI:
*   **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
*   **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---
*Projeto desenvolvido para fins de estudo com base no curso da Hashtag Programação.*