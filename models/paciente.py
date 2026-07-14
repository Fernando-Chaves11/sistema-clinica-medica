from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Paciente(db.Model):

    __tablename__ = "pacientes"

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(100), nullable=False)

    cpf = db.Column(db.String(14), unique=True, nullable=False)

    telefone = db.Column(db.String(20))

    nascimento = db.Column(db.String(10))