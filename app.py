from credentials import users
from orders.order import Order, Status, OrdersManager
from orders.places import AddressGenerator
from orders.recommendations import Recommendation
from parser.parser import parse_farmani
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)
orderManager = OrdersManager()
addressGenerator = AddressGenerator()
recommendations = Recommendation()
FARMANI_API = 'https://farmani.ru/search/?q='


# login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users.keys():
            if users[username] == password:
                if username == 'edward':
                    return redirect(url_for("search"))
                if username == 'pavel48':
                    return redirect(url_for("courier"))
    return render_template('login.html')


# search
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form.get('query').lower()
        option = parse_farmani(FARMANI_API+query)
        top_alignment = 47
        for result in option:
            result.append(top_alignment)
            top_alignment += 25
        return render_template('search_results.html', data=option)
    return render_template('search.html')


# payment
@app.route('/payment', methods=['GET', 'POST'])
def pay():
    if request.method == 'GET':
        order = Order(
            -1,
            request.args.get('button_id').split("'")[1],
            request.args.get('button_id').split("'")[3],
            request.args.get('button_id').split("'")[5],
            request.args.get('button_id').split("'")[7],
            Status().get_status_str(),
            addressGenerator.get_place(),
            addressGenerator.get_place()
        )
        orderManager.add_new_order(order)
        print(order.id)
        print(order.drug)
        print(order.country)
        print(order.manufacturer)
        print(order.price)
        print(order.status)
        print(order.address)
        print(order.drug_store)
        print(order.waiting_time)
        return render_template('payment.html', data=order.id)
    if request.method == 'POST':
        return redirect(url_for("status"))


# status
@app.route('/status', methods=['GET', 'POST'])
def status():
    if request.method == 'POST':
        return redirect(url_for("search"))
    if request.method == 'GET':
        order_details = orderManager.get_by_id(orderManager.get_order())
        status = Status()
        status.set_status_by_str(order_details[5])
        status.increment_status()
        order_details[5] = status.get_status_str()
        order_details.append(recommendations.get_variant())
        return render_template('status.html', data=order_details)


# courier
@app.route('/courier', methods=['GET', 'POST'])
def courier():
    if request.method == 'GET':
        return render_template('courier.html')
    if request.method == 'POST':
        order_to_deliver = orderManager.get_by_id(orderManager.get_order())
        print(order_to_deliver)
        data_for_courier = [
            order_to_deliver[0],
            order_to_deliver[6],
            order_to_deliver[7],
            order_to_deliver[8]
        ]
        return render_template('courier_request.html', data=data_for_courier)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
