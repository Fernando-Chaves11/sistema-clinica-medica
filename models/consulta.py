from models.paciente import db


class Consulta(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    paciente = db.Column(db.String(100), nullable=False)

    medico = db.Column(db.String(100), nullable=False)

    data = db.Column(db.String(20), nullable=False)

    hora = db.Column(db.String(10), nullable=False)

    observacao = db.Column(db.String(300))