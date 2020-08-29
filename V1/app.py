import time
import pymysql
import datetime
from services.shortner_url import id_generator
from flask import Flask, render_template, jsonify, request
from flaskext.mysql import MySQL
# poner version de python 
import conekta

app = Flask(__name__)
database = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '2133010323Gl?'
app.config['MYSQL_DATABASE_DB'] = 'paymentlink'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'

domain_address =  'http://127.0.0.1:3000/'

database.init_app(app)

@app.route('/')
def Index():
    return render_template('payment.html')

@app.route('/payment', methods=['POST'])
def add_paymentInfo():
    if request.method == 'POST':
        order_id = request.form['order_id']
        phone_number = request.form['phone_number']
        payment_amount = request.form['payment_amount']
        payment_concept = request.form['payment_concept']
        business_name = request.form['business_name']
        business_logo_url = request.form['business_logo_url']
        result = "OK"
        link_id = id_generator().url_id(order_id)
        link_url = domain_address+link_id
        creation_date = datetime.datetime.now()
        conn = database.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute('INSERT INTO infopaymentlink (order_id, phone_number, payment_amount, payment_concept, business_name, business_logo_url, result, link_id, link_url, creation_date ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
        (order_id, phone_number, payment_amount, payment_concept, business_name, business_logo_url, result, link_id, link_url, creation_date))
        conn.commit()
        return get_paymentInfo(order_id)

@app.route('/payment/<order_id>', methods = ['POST', 'GET'])
def get_paymentInfo(order_id):
  conn = database.connect()
  cur = conn.cursor(pymysql.cursors.DictCursor)
  cur.execute('SELECT result, link_id, link_url, error_code, error_text  FROM infopaymentlink WHERE order_id = %s', (order_id))
  rows = cur.fetchall()
  cur.close()
  resp = jsonify(rows)
  resp.status_code=200
  return resp

@app.route('/AllInfo', methods = ['POST', 'GET'])
def get_allData():
  conn = database.connect()
  cur = conn.cursor(pymysql.cursors.DictCursor)
  cur.execute('SELECT * FROM infopaymentlink')
  rows = cur.fetchall()
  cur.close()
  resp = jsonify(rows)
  resp.status_code=200
  return resp

@app.route('/PaymentInfo/<link_id>', methods = ['POST', 'GET'])
def get_PaymentInfo(link_id):
  conn = database.connect()
  cur = conn.cursor(pymysql.cursors.DictCursor)
  cur.execute('SELECT * FROM infopaymentlink WHERE link_id = %s', (link_id))
  rows = cur.fetchall()
  cur.close()
  resp = jsonify(rows)
  resp.status_code=200
  return resp

@app.route('/<link_id>', methods = ['POST', 'GET'])
def get_paymentLink(link_id):
  conn = database.connect()
  cur = conn.cursor(pymysql.cursors.DictCursor)
  cur.execute('SELECT phone_number, payment_amount, payment_concept, business_name, business_logo_url FROM infopaymentlink WHERE link_id = %s', (link_id))
  rows = cur.fetchall()
  cur.close()
  print (rows[0])
  return render_template('paymentCard.html', paymentInfo = rows[0])

@app.route('/paidOut/<link_id>', methods=['POST'])
def update_paidOut(link_id):
  if request.method == 'POST':
      second_phone = request.form['second_phone']
      paid_out = 1
      conn = database.connect()
      cur = conn.cursor(pymysql.cursors.DictCursor)
      cur.execute("""
          UPDATE infopaymentlink
          SET second_phone = %s,
              paid_out = %s
          WHERE link_id = %s
      """, (second_phone, paid_out, link_id))
      conn.commit()
      return 'ok'

@app.route('/paymentOrder', methods=["POST"])
def subscription_create():
  conekta.api_key = 'key_ADvMPC2qmR91oC193CFoQA'
  conekta.api_version = "2.0.0"
  conekta.locale = 'es'
   
  try:
    customer = conekta.Customer.create({
      'name': request.form['name'],
      'email': request.form['email'],
      "phone": request.form['phone'],
      'payment_sources': [{
        'type': 'card',
        'token_id': request.form['token_id']
      }]
    })
    orden=order_create(request.form['concept'], request.form['amount'], customer.id)
    return render_template('payment.html', customer_id=customer.id, order_id=orden)

  except conekta.ConektaError as e:
    print(e.message)

def order_create(valor1, valor2, valor3):  
  valor5=100
  valor6=int(valor2)
  valor7=int(valor5)
  valor7 = valor6 * valor7
  # Implementación de una orden.
  conekta.api_key = 'key_ADvMPC2qmR91oC193CFoQA'
  conekta.api_version = "2.0.0"
  conekta.locale = 'es'

  try:
    order = conekta.Order.create({
      "currency": "MXN",
      "line_items": [{
        "name": valor1,
        "unit_price": valor7,
        "quantity": 1
      }],
                
      "customer_info": {
        "customer_id": valor3
      },
      "charges": [{
        "payment_method": {
          "type": "default"
        } 
      }]
    })
  except conekta.ConektaError as e:
    print(e.message)
  return order.id

if __name__ == '__main__':
    app.run(port = 3000, debug = True)