from flask import Flask
from flask_migrate import Migrate
from .models import db

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    migrate.init_app(app, db)

    # rotas
    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    # comando de seed para popular rápido
    @app.cli.command("seed")
    def seed():
        from .models import Service
        with app.app_context():
            if Service.query.count() == 0:
                db.session.add_all([
                    Service(name="Veterinário", description="Atendimento domiciliar e preventivo.", price=150.0, icon="consulta.png", is_active=True),
                    Service(name="Banho & Tosa", description="Banho, secagem e tosa higiênica.", price=80.0, icon="banho.png", is_active=True),
                    Service(name="Adestramento", description="Aulas básicas de obediência.", price=120.0, icon="adestramento.png", is_active=True),
                    Service(name="Dog Walk", description="Passeios de 30 minutos.", price=50.0, icon="passeio.png", is_active=True),
                ])
                db.session.commit()
                print("Seed concluído.")
            else:
                print("Já existem serviços na base.")
    return app
