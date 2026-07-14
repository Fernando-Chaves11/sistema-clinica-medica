from models.paciente import db


class Medico(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(100), nullable=False)

    crm = db.Column(db.String(20), nullable=False)

    especialidade = db.Column(db.String(100), nullable=False)

    telefone = db.Column(db.String(20))