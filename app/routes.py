from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from .models import db, Service

bp = Blueprint("main", __name__)

# ----------------- PÚBLICO -----------------
@bp.route("/")
def index():
    services = Service.query.filter_by(is_active=True).order_by(Service.name).all()
    # sua index.html usa cards estáticos? beleza; por enquanto só mandamos 'services' caso queira iterar lá
    return render_template("index.html", services=services, page_title="Início")

@bp.route("/servicos")
def servicos():
    services = Service.query.filter_by(is_active=True).order_by(Service.name).all()
    # se quiser usar services_list.html, troque o template abaixo
    return render_template("servicos.html", services=services, page_title="Serviços")

@bp.route("/agendamentos")
def agendamentos():
    return render_template("agendamentos.html", page_title="Meus agendamentos")

@bp.route("/quem-somos")
def quem_somos():
    return render_template("quem_somos.html", page_title="Quem somos")

@bp.route("/login")
def login():
    return render_template("login.html", page_title="Entrar")

@bp.route("/cadastro")
def cadastro():
    return render_template("cadastro.html", page_title="Cadastro")


# ----------------- ADMIN WEB (CRUD) -----------------
@bp.route("/admin/services")
def services_admin():
    services = Service.query.order_by(Service.id.desc()).all()
    return render_template("services_admin.html", services=services, page_title="Gerir serviços")

@bp.route("/admin/services/new", methods=["GET", "POST"])
def services_new():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:
            flash("Nome é obrigatório.", "danger")
            return redirect(url_for("main.services_new"))

        s = Service(
            name=name,
            description=request.form.get("description", ""),
            price=float(request.form.get("price", 0) or 0),
            icon=request.form.get("icon", ""),
            is_active=request.form.get("is_active") == "on"
        )
        db.session.add(s)
        db.session.commit()
        flash("Serviço cadastrado!", "success")
        return redirect(url_for("main.services_admin"))
    return render_template("service_form.html", service=None, page_title="Novo serviço")

@bp.route("/admin/services/<int:service_id>/edit", methods=["GET", "POST"])
def services_edit(service_id):
    s = Service.query.get_or_404(service_id)
    if request.method == "POST":
        s.name = request.form.get("name", s.name)
        s.description = request.form.get("description", s.description)
        s.price = float(request.form.get("price", s.price) or 0)
        s.icon = request.form.get("icon", s.icon)
        s.is_active = request.form.get("is_active") == "on"
        db.session.commit()
        flash("Serviço atualizado!", "success")
        return redirect(url_for("main.services_admin"))
    return render_template("service_form.html", service=s, page_title="Editar serviço")

@bp.route("/admin/services/<int:service_id>/delete", methods=["POST"])
def services_delete(service_id):
    s = Service.query.get_or_404(service_id)
    db.session.delete(s)
    db.session.commit()
    flash("Serviço excluído.", "info")
    return redirect(url_for("main.services_admin"))

@bp.route("/admin/services/<int:service_id>/toggle", methods=["POST"])
def services_toggle(service_id):
    s = Service.query.get_or_404(service_id)
    s.is_active = not s.is_active
    db.session.commit()
    flash("Status alterado.", "info")
    return redirect(url_for("main.services_admin"))

# ----------------- API (para integrar com front) -----------------
@bp.get("/api/services")
def api_services_list():
    only_active = request.args.get("active", "true").lower() == "true"
    q = Service.query
    if only_active:
        q = q.filter_by(is_active=True)
    return jsonify([s.to_dict() for s in q.order_by(Service.name).all()])

@bp.get("/api/services/<int:service_id>")
def api_services_detail(service_id):
    s = Service.query.get_or_404(service_id)
    return jsonify(s.to_dict())
