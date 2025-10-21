# Projeto Django REST Framework

1. Clonar o repositório:
   ```bash
   git clone https://github.com/tatianefeitosa/busca_api.git
   cd busca_api
   cd busca_api


2. Criar o .env local baseado no .env.example:
    ```bash
    copy .env.example .env   # Windows
    cp .env.example .env     # Mac

Abra o arquivo .env e preencha as variáveis do banco remoto (Supabase) e outras credenciais como SECRET_KEY, DEBUG e ALLOWED_HOSTS.
Consulte o Notion para obter as credenciais do banco remoto.


3. Criar e ativar o ambiente virtual:
    ```bash
    cd ..
    python -m venv venv
    venv\Scripts\activate  # Windows
    source venv/bin/activate  # Mac


4. Instalar as dependências:
    ```bash
    cd busca_api
    pip install -r requirements.txt


5. Inicie o servidor:
    ```bash
    python manage.py runserver

O projeto estará disponível em: http://127.0.0.1:8000/

Para acessar o Swagger: http://127.0.0.1:8000/api/docs/


6. Boas práticas de uso

Não suba seu .env para o GitHub.

Use sempre a mesma branch main para sincronizar atualizações.







