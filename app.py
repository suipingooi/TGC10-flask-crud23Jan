from flask import Flask, render_template, request, redirect, url_for
import json
import os
import random

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


@app.route('/customers/add')
def show_add_customers():
    return render_template('add_customer.template.html')


@app.route('/customers/add', methods=['POST'])
def process_add_customer():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    agree = request.form.get('can_send')
# generate a random number as customer ID but usually we
# will get database to generate for us. (industry standard)
    customer_id = random.randint(1, 10000) + 5

    new_customer = {}
    new_customer['id'] = customer_id
    new_customer['first_name'] = first_name
    new_customer['last_name'] = last_name
    new_customer['email'] = email
    new_customer['send_marketing_material'] = agree == "on"
   
    database.append(new_customer)
    return "data received"


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host='localhost',
            port=8080,
            debug=True)
