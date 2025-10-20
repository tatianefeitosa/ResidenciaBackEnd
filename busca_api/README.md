# Projeto Django REST Framework

## Como rodar o projeto localmente

1. Clone o repositório:
   ```bash
   git clone https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git
   cd NOME_DO_REPOSITORIO

2. Crie um ambiente virtual:
    ```bash
    python -m venv venv
    venv\Scripts\activate  # Windows
    source venv/bin/activate  # Linux/Mac

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt

4. Crie o arquivo .env baseado no .env.example:
    ```bash
    cp .env.example .env  # Linux/Mac
    copy .env.example .env # Windows

5. Preencha as variáveis do .env com os valores corretos (SECRET_KEY, banco de dados, JWT).

6. Rode as migrações e inicie o servidor:
    ```bash
    python manage.py migrate
    python manage.py runserver




