# 🐾 Pettzy

**Pettzy** é uma plataforma que conecta tutores de pets a profissionais de cuidado animal — como veterinários domiciliares, banho & tosa, adestradores e dog walkers.  
O objetivo é oferecer **praticidade, segurança e eficiência** no cuidado com os animais de estimação.

---

## ✨ O que já tem pronto

- 🖥️ Site dinâmico com **Flask + Jinja**  
- 📦 **CRUD de Serviços** (cadastrar, editar, excluir, ativar/inativar)  
- 🗂️ **Admin web** para gerenciar serviços: `/admin/services`  
- 🧑‍🍳 **Seed** com serviços de exemplo (Veterinário, Banho & Tosa, Adestramento, Dog Walk)  
- 🔌 **API pública** para listar/detalhar serviços  

> **Próximos passos:** autenticação (proteção do admin), cadastro de profissionais, agendamentos, buscas e filtros.

---

## 🛠️ Tecnologias

**Backend**
- Python 3.11+  
- Flask  
- Flask-SQLAlchemy  
- Flask-Migrate  

**Frontend**
- Jinja (SSR)  
- HTML, CSS, JavaScript  

**Banco**
- SQLite (desenvolvimento)  
- PostgreSQL (produção, opcional)  

---

## 🚀 Como rodar (dev)

```bash
# 1) criar e ativar venv
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 2) instalar dependências
pip install -r requirements.txt

# 3) criar as tabelas
flask --app run.py db upgrade

# 4) popular dados de exemplo
flask --app run.py seed

# 5) executar
python run.py
# http://127.0.0.1:5000/ 


