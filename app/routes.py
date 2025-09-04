from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from .models import db, Service, AboutBlock

bp = Blueprint("main", __name__)

# ----------------- Helpers -----------------
def _to_float(value, default=0.0):
    """Converte '120,50' ou '120.50' em float."""
    try:
        return float(str(value).replace(",", "."))
    except Exception:
        return default

def _is_checked(name: str) -> bool:
    """Lê checkbox/radio de formulário como booleano."""
    return request.form.get(name) in ("on", "true", "1", "yes")

# ----------------- PÚBLICO -----------------
@bp.route("/")
def index():
    services = Service.query.filter_by(is_active=True).order_by(Service.name).all()
    return render_template("index.html", services=services, page_title="Início")

@bp.route("/servicos")
def servicos():
    services = Service.query.filter_by(is_active=True).order_by(Service.name).all()
    return render_template("servicos.html", services=services, page_title="Serviços")

@bp.route("/agendamentos")
def agendamentos():
    return render_template("agendamentos.html", page_title="Meus agendamentos")

@bp.route("/quem-somos")
def quem_somos():
    blocks = AboutBlock.query.order_by(AboutBlock.display_order, AboutBlock.id).all()
    return render_template("quem_somos.html", blocks=blocks, page_title="Quem somos")

@bp.route("/login")
def login():
    return render_template("login.html", page_title="Entrar")

@bp.route("/cadastro")
def cadastro():
    return render_template("cadastro.html", page_title="Cadastro")

# ----------------- ADMIN WEB (CRUD) -----------------
# Rota legada: jogamos tudo para o dashboard único
@bp.route("/admin/services")
def services_admin():
    return redirect(url_for("main.admin_dashboard"))

@bp.route("/admin/services/new", methods=["GET", "POST"])
def services_new():
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        if not name:
            flash("Nome é obrigatório.", "danger")
            return redirect(url_for("main.services_new"))

        s = Service(
            name=name,
            description=request.form.get("description", "") or "",
            price=_to_float(request.form.get("price", 0)),
            icon=request.form.get("icon", "") or "",
            is_active=_is_checked("is_active"),
        )
        db.session.add(s)
        db.session.commit()
        flash("Serviço cadastrado!", "success")
        return redirect(url_for("main.admin_dashboard"))

    return render_template("admin/service_form.html", service=None, page_title="Novo serviço")

@bp.route("/admin/services/<int:service_id>/edit", methods=["GET", "POST"])
def services_edit(service_id):
    s = Service.query.get_or_404(service_id)
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        if not name:
            flash("Nome é obrigatório.", "danger")
            return redirect(url_for("main.services_edit", service_id=service_id))

        s.name = name
        s.description = request.form.get("description", "") or s.description
        s.price = _to_float(request.form.get("price", s.price))
        s.icon = request.form.get("icon", "") or s.icon
        s.is_active = _is_checked("is_active")
        db.session.commit()
        flash("Serviço atualizado!", "success")
        return redirect(url_for("main.admin_dashboard"))

    return render_template("admin/service_form.html", service=s, page_title="Editar serviço")

@bp.route("/admin/services/<int:service_id>/delete", methods=["POST"])
def services_delete(service_id):
    s = Service.query.get_or_404(service_id)
    db.session.delete(s)
    db.session.commit()
    flash("Serviço excluído.", "info")
    return redirect(url_for("main.admin_dashboard"))

@bp.route("/admin/services/<int:service_id>/toggle", methods=["POST"])
def services_toggle(service_id):
    s = Service.query.get_or_404(service_id)
    s.is_active = not s.is_active
    db.session.commit()
    flash("Status alterado.", "info")
    return redirect(request.referrer or url_for("main.admin_dashboard"))

# ===== ADMIN: QUEM SOMOS =====
# Se não quiser uma página separada, pode remover essa rota;
# Mantive para evitar 404, redirecionando ao dashboard.
@bp.route("/admin/about")
def about_admin():
    return redirect(url_for("main.admin_dashboard"))

@bp.route("/admin/about/new", methods=["GET", "POST"])
def about_new():
    if request.method == "POST":
        title = (request.form.get("title") or "").strip()
        if not title:
            flash("Título é obrigatório.", "danger")
            return redirect(url_for("main.about_new"))

        b = AboutBlock(
            title=title,
            body=request.form.get("body", "") or "",
            image=request.form.get("image", "") or "",
            icon=request.form.get("icon", "") or "",
            section=request.form.get("section", "story") or "story",
            display_order=int(request.form.get("display_order", 0) or 0),
        )
        db.session.add(b)
        db.session.commit()
        flash("Bloco cadastrado!", "success")
        return redirect(url_for("main.admin_dashboard"))

    return render_template("admin/about_form.html", block=None, page_title="Novo bloco — Quem Somos")

@bp.route("/admin/about/<int:block_id>/edit", methods=["GET", "POST"])
def about_edit(block_id):
    b = AboutBlock.query.get_or_404(block_id)
    if request.method == "POST":
        b.title         = request.form.get("title", b.title)
        b.body          = request.form.get("body", b.body)
        b.image         = request.form.get("image", b.image)
        b.icon          = request.form.get("icon", b.icon)
        b.section       = request.form.get("section", b.section)
        b.display_order = int(request.form.get("display_order", b.display_order) or 0)
        db.session.commit()
        flash("Bloco atualizado!", "success")
        return redirect(url_for("main.admin_dashboard"))

    return render_template("admin/about_form.html", block=b, page_title="Editar bloco — Quem Somos")

@bp.route("/admin/about/<int:block_id>/delete", methods=["POST"])
def about_delete(block_id):
    b = AboutBlock.query.get_or_404(block_id)
    db.session.delete(b)
    db.session.commit()
    flash("Bloco excluído.", "info")
    return redirect(url_for("main.admin_dashboard"))

# helper: garante que o bloco existe; se não existir, cria com defaults
def _get_or_create_about(section: str, title_default: str, order: int):
    blk = AboutBlock.query.filter_by(section=section).first()
    if not blk:
        blk = AboutBlock(section=section, title=title_default, body="", display_order=order)
        db.session.add(blk)
        db.session.commit()
    return blk

# página única para editar os 4 blocos principais (opcional)
@bp.route("/admin/about/core", methods=["GET", "POST"])
def about_core():
    story   = _get_or_create_about("story",   "Nossa história", 10)
    mission = _get_or_create_about("mission", "Missão",         20)
    vision  = _get_or_create_about("vision",  "Visão",          30)
    values  = _get_or_create_about("values",  "Valores",        40)

    if request.method == "POST":
        story.title   = request.form.get("story_title", story.title)
        story.body    = request.form.get("story_body", story.body)
        mission.title = request.form.get("mission_title", mission.title)
        mission.body  = request.form.get("mission_body", mission.body)
        vision.title  = request.form.get("vision_title", vision.title)
        vision.body   = request.form.get("vision_body", vision.body)
        values.title  = request.form.get("values_title", values.title)
        values.body   = request.form.get("values_body", values.body)
        db.session.commit()
        flash("Conteúdo atualizado com sucesso!", "success")
        return redirect(url_for("main.about_core"))

    return render_template(
        "admin/about_core.html",
        story=story, mission=mission, vision=vision, values=values,
        page_title="Editar — Quem Somos"
    )

@bp.route("/admin")
@bp.route("/admin/")
@bp.route("/admin/dashboard")
def admin_dashboard():
    services = Service.query.order_by(Service.id.desc()).all()
    blocks = AboutBlock.query.order_by(AboutBlock.display_order, AboutBlock.id.desc()).all()
    return render_template("admin/dashboard.html",
                           services=services, blocks=blocks, page_title="Admin")

# ----------------- API -----------------
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
