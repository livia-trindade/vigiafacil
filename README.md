## ⚙️ Como Executar Localmente

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/livia-trindade/vigiafacil.git
   ```

2. **Acesse a pasta do projeto**:
   ```bash
   cd vigiafacil
   ```

3. **Crie e ative um ambiente virtual (Opcional)**:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```


4. **Realize as migrações do banco de dados**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Crie um superusuário**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Execute o servidor**:
   ```bash
   python manage.py runserver
   ```

7. **Acesse no localmente no seu navegador**:
   ```bash
   http://127.0.0.1:8000
   ```
