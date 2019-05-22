# 2 route:
# 1. показ страницы (формы)
# 2. обработка формы (POST/GET)
from flask import Flask, render_template, request, redirect, url_for

import db
from domain import Good

app = Flask(__name__)
db_url = 'db.sqlite'


@app.route("/", methods=['GET'])
def index():
    goods = db.get_all(db.open_db(db_url))
    return render_template('index.html', items=goods)


@app.route("/add", methods=['GET'])
def add_form():
    return render_template('add.html')


@app.route("/add", methods=['POST'])
def add():
    name = request.form['name']
    price = int(request.form['price'])
    qty = int(request.form['qty'])
    good = Good(0, name, price, qty)
    db.add(db.open_db(db_url), good)
    return redirect(url_for('index'))


@app.route("/details/<id>", methods=['GET'])
def details_by_id(id):
    good = db.get_by_id(db.open_db(db_url), id)
    return render_template('details.html', item=good)


@app.route("/edit/<id>", methods=['GET'])
def edit_form_by_id(id):
    good = db.get_by_id(db.open_db(db_url), id)
    return render_template('edit.html', item=good)


@app.route("/edit/<id>", methods=['POST'])
def edit_by_id(id):
    name = request.form['name']
    price = int(request.form['price'])
    qty = int(request.form['qty'])
    good = Good(id, name, price, qty)
    db.update(db.open_db(db_url), good)
    return redirect(url_for('details_by_id', id=id))


@app.route("/remove/<id>", methods=['GET'])
def remove_form_by_id(id):
    good = db.get_by_id(db.open_db(db_url), id)
    return render_template('remove.html', item=good)


@app.route("/remove/<id>", methods=['POST'])
def remove_by_id(id):
    db.remove_by_id(db.open_db(db_url), id)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port=8888, debug=True)
