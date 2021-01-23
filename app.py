from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
database = {}
with open('customers.json') as fp:
    database = json.load(fp)
print(database)


@app.route('/')
def home():
    return render_template('home.template.html')


@app.route('/customers')
def show_customers():
    return render_template('customers.template.html',
                           customers=database)


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host='localhost',
            port=8080,
            debug=True)
