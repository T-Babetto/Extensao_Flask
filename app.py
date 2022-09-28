from http import client
from flask import Flask, Response, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import json

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cliente.sqlite3'

db = SQLAlchemy(app)


class Cliente(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50))
    email = db.Column(db.String(100))

    def __init__(self, nome, email):
        self.nome = nome
        self.email = email


@app.route('/')
def index():
    cliente = Cliente.query.all()
    return render_template('index.html', cliente=cliente)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        clientes = Cliente(request.form['nome'], request.form['email'])
        db.session.add(cliente)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/edit/<int:id>', methods=['GET, POST'])
def edit(id):
    clientes = Cliente.query.get(id)
    if request.method == 'POST':
        clientes.nome = request.form['nome']
        clientes.email = request.form['email']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', clientes=clientes)


@app.route('/delete/<int:id>')
def delete(id):
    clientes = Cliente.query.get(id)
    db.session.delete(clientes)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
