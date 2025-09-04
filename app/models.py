from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, default="")
    price = db.Column(db.Float, default=0.0)
    icon = db.Column(db.String(200), default="")
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "icon": self.icon,
            "is_active": self.is_active,
        }

class AboutBlock(db.Model):
    __tablename__ = "about_blocks"

    id = db.Column(db.Integer, primary_key=True)
    # título do bloco (ex.: "Nossa história", "Missão", "Visão", "Valores")
    title = db.Column(db.String(120), nullable=False)

    # texto/descrição (HTML simples permitido)
    body = db.Column(db.Text, default="")

    # opcional: imagem/ícone (arquivo em static/)
    image = db.Column(db.String(200), default="")   # ex.: "pets.png" ou "imgs/pets.png"
    icon  = db.Column(db.String(100), default="")   # ex.: "🐾" ou "icons/paw.png"

    # para agrupar/ordenar se quiser (ex.: "story", "values", "cta", "hero")
    section = db.Column(db.String(40), default="default")

    # ordem de exibição na página
    display_order = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "image": self.image,
            "icon": self.icon,
            "section": self.section,
            "display_order": self.display_order,
        }