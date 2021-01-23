from flask import Flask, render_template, request, redirect, url_for
import json
import os
import random

app = Flask(__name__)
database = {}
with open('customers.json') as fp:
    database = json.load(fp)
print(database)


def find_customer_by_id(customer_id):
    customer = None
    for each_customer in database:
        if each_customer['id'] == int(customer_id):
            customer = each_customer
    return customer


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
    can_send = request.form.get('can_send')
# generate a random number as customer ID but usually we
# will get database to generate for us. (industry standard)
    customer_id = random.randint(1, 1000000) + 5

    new_customer = {}
    new_customer['id'] = customer_id
    new_customer['first_name'] = first_name
    new_customer['last_name'] = last_name
    new_customer['email'] = email
    new_customer['send_marketing_material'] = can_send == "on"

    database.append(new_customer)

    with open('customers.json', 'w') as fp:
        json.dump(database, fp)

    return redirect(url_for('show_customers'))


@app.route('/customers/<customer_id>/edit')
def show_edit_customer(customer_id):
    # customer_id will refer to the id of customer
    # that we want to edit
    # hence it is important for all customer
    # to have a unique identifier
    # 1. retrieve customer we want to edit
    customer_to_edit = find_customer_by_id(customer_id)

    # if customer exist, show form to edit
    if customer_to_edit:
        return render_template('edit_customer.template.html',
                               customer=customer_to_edit)
    else:
        return "Customer Not Found!"


@app.route('/customers/<customer_id>/edit', methods=["POST"])
def process_edit_customer(customer_id):
    print(request.form)
    customer = find_customer_by_id(customer_id)
    if customer:
        # extract out the values from the form
        customer['first_name'] = request.form.get('first_name')
        customer['last_name'] = request.form.get('last_name')
        customer['email'] = request.form.get('email')
        customer['send_marketing_material'] = request.form.get(
            'can_send') == 'on'

        with open('customers.json', 'w') as fp:
            json.dump(database, fp)
        return redirect(url_for('show_customers'))

    else:
        return "Customer Does Not Exist!"


@app.route('/customers/<customer_id>/delete')
def show_delete_customer(customer_id):
    customer = find_customer_by_id(customer_id)
    if customer:
        return render_template('show_delete_customer.template.html',
                               customer=customer)
    else:
        return "Customer Not Found!"


@app.route('/customers/<customer_id>/delete', methods=["POST"])
def process_delete_customer(customer_id):
    customer_to_delete = find_customer_by_id(customer_id)
    database.remove(customer_to_delete)

    with open('customers.json', 'w') as fp:
        json.dump(database, fp)

    return redirect(url_for('show_customers'))


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=8080,
            debug=True)
