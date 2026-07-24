from flask import Flask, render_template, request, redirect

from config import Config
from models.paciente import Paciente
from models.medico import Medico
from models.consulta import Consulta
from models.paciente import db

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/menu")
def menu():

    total_pacientes = Paciente.query.count()

    total_medicos = Medico.query.count()

    total_consultas = Consulta.query.count()

    return render_template(

        "menu.html",

        total_pacientes=total_pacientes,

        total_medicos=total_medicos,

        total_consultas=total_consultas

    )

@app.route("/pacientes")
def pacientes():

    pesquisa = request.args.get("pesquisa", "")

    if pesquisa:

        lista = Paciente.query.filter(
            Paciente.nome.contains(pesquisa)
        ).all()

    else:

        lista = Paciente.query.all()

    return render_template(
        "pacientes.html",
        pacientes=lista,
        pesquisa=pesquisa
    )

@app.route("/medicos")
def medicos():

    pesquisa = request.args.get("pesquisa", "")

    if pesquisa:

        lista = Medico.query.filter(
            Medico.nome.contains(pesquisa)
        ).all()

    else:

        lista = Medico.query.all()

    return render_template(
        "medicos.html",
        medicos=lista,
        pesquisa=pesquisa
    )

@app.route("/consultas")
def consultas():

    pesquisa = request.args.get("pesquisa", "")
    medico = request.args.get("medico", "")
    data = request.args.get("data", "")

    consulta = Consulta.query

    # Pesquisa por paciente
    if pesquisa:
        consulta = consulta.filter(
            Consulta.paciente.contains(pesquisa)
        )

    # Agenda do médico
    if medico:
        consulta = consulta.filter(
            Consulta.medico == medico
        )

    # Data da agenda
    if data:
        consulta = consulta.filter(
            Consulta.data == data
        )

    lista_consultas = consulta.all()

    lista_pacientes = Paciente.query.all()
    lista_medicos = Medico.query.all()

    return render_template(
        "consultas.html",
        consultas=lista_consultas,
        pacientes=lista_pacientes,
        medicos=lista_medicos,
        pesquisa=pesquisa,
        medico_selecionado=medico,
        data_selecionada=data
    )

@app.route("/salvar_consulta", methods=["POST"])
def salvar_consulta():

    consulta = Consulta(

        paciente=request.form["paciente"],
        medico=request.form["medico"],
        data=request.form["data"],
        hora=request.form["hora"],
        observacao=request.form["observacao"]

    )

    db.session.add(consulta)

    db.session.commit()

    return redirect("/consultas")

@app.route("/editar_consulta/<int:id>")
def editar_consulta(id):

    consulta = Consulta.query.get_or_404(id)

    pacientes = Paciente.query.all()

    medicos = Medico.query.all()

    return render_template(
        "editar_consulta.html",
        consulta=consulta,
        pacientes=pacientes,
        medicos=medicos
    )


@app.route("/atualizar_consulta/<int:id>", methods=["POST"])
def atualizar_consulta(id):

    consulta = Consulta.query.get_or_404(id)

    consulta.paciente = request.form["paciente"]
    consulta.medico = request.form["medico"]
    consulta.data = request.form["data"]
    consulta.hora = request.form["hora"]
    consulta.observacao = request.form["observacao"]

    db.session.commit()

    return redirect("/consultas")


@app.route("/excluir_consulta/<int:id>")
def excluir_consulta(id):

    consulta = Consulta.query.get_or_404(id)

    db.session.delete(consulta)

    db.session.commit()

    return redirect("/consultas")

@app.route("/salvar_medico", methods=["POST"])
def salvar_medico():

    medico = Medico(

        nome=request.form["nome"],
        crm=request.form["crm"],
        especialidade=request.form["especialidade"],
        telefone=request.form["telefone"]

    )

    db.session.add(medico)

    db.session.commit()

    return redirect("/medicos")


@app.route("/editar_medico/<int:id>")
def editar_medico(id):

    medico = Medico.query.get_or_404(id)

    return render_template(
        "editar_medico.html",
        medico=medico
    )


@app.route("/atualizar_medico/<int:id>", methods=["POST"])
def atualizar_medico(id):

    medico = Medico.query.get_or_404(id)

    medico.nome = request.form["nome"]
    medico.crm = request.form["crm"]
    medico.especialidade = request.form["especialidade"]
    medico.telefone = request.form["telefone"]

    db.session.commit()

    return redirect("/medicos")


@app.route("/excluir_medico/<int:id>")
def excluir_medico(id):

    medico = Medico.query.get_or_404(id)

    db.session.delete(medico)

    db.session.commit()

    return redirect("/medicos")

@app.route("/salvar_paciente", methods=["POST"])
def salvar_paciente():

    paciente = Paciente(

        nome=request.form["nome"],

        cpf=request.form["cpf"],

        telefone=request.form["telefone"],

        nascimento=request.form["nascimento"]

    )

    db.session.add(paciente)

    db.session.commit()

    return redirect("/pacientes")

@app.route("/excluir/<int:id>")
def excluir(id):

    paciente = Paciente.query.get_or_404(id)

    db.session.delete(paciente)

    db.session.commit()

    return redirect("/pacientes")

@app.route("/editar/<int:id>")
def editar(id):

    paciente = Paciente.query.get_or_404(id)

    return render_template("editar_paciente.html", paciente=paciente)


@app.route("/atualizar/<int:id>", methods=["POST"])
def atualizar(id):

    paciente = Paciente.query.get_or_404(id)

    paciente.nome = request.form["nome"]
    paciente.cpf = request.form["cpf"]
    paciente.telefone = request.form["telefone"]
    paciente.nascimento = request.form["nascimento"]

    db.session.commit()

    return redirect("/pacientes")

if __name__ == "__main__":
    app.run(debug=True)
