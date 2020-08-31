import time
import json
import pymysql
import datetime
from services.shortner_url import id_generator
from flask import Flask, render_template, jsonify, request
from flaskext.mysql import MySQL
import conekta

app = Flask(__name__)
database = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '2133010323Gl?'
app.config['MYSQL_DATABASE_DB'] = 'paymentlink'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'

database.init_app(app)

domain_address =  'http://127.0.0.1:3000/'

@app.route('/')
def Index():
    return render_template('addInfo.html')

@app.route('/payment', methods=['POST'])
def add_paymentInfo():
    if request.method == 'POST':
        order_id = request.form['order_id']
        phone_number = request.form['phone_number']
        payment_amount = request.form['payment_amount']
        payment_concept = request.form['payment_concept']
        business_name = request.form['business_name']
        business_logo_url = request.form['business_logo_url']
        result = 'OK'
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
  cur.execute('SELECT order_id, paid_out, not_payed, phone_number, payment_amount, payment_concept, business_name, business_logo_url, order_id FROM infopaymentlink WHERE link_id = %s', (link_id))
  rows = cur.fetchall()
  cur.close()
  print (rows[0])
  return render_template('paymentCard.html', paymentInfo = rows[0])


@app.route('/paymentOrder', methods=["POST"])
def subscription_create():
  conekta.api_key = 'key_ADvMPC2qmR91oC193CFoQA'
  conekta.api_version = "2.0.0"
  conekta.locale = 'es'
  payment_processor = 'Conekta'
  token=request.form['token_id']
  exp_month=request.form['exp_month']
  exp_year=request.form['exp_year']
  exp_date= exp_month+'/'+exp_year
  cust_phone = request.form['cust_phone'].replace(" ", "")
  cust_email = request.form['cust_email']
  credit_card=request.form['credit_card']
  i=len(credit_card)-4
  total=len(credit_card)
  client_cc_first_digits=credit_card[0:4]
  client_cc_last_digits=credit_card[i:total] 
  payment_date = datetime.datetime.now()
  order_id=request.form['order_id']
  conn = database.connect()
  cur = conn.cursor(pymysql.cursors.DictCursor)
  cur.execute('UPDATE infopaymentlink SET payment_processor = %s, token = %s, exp_date = %s, not_payed = "False", paid_out = "hidden", cust_phone = %s, cust_email = %s, client_cc_first_digits = %s, client_cc_last_digits = %s, payment_date = %s WHERE order_id = %s',(payment_processor, token, exp_date, cust_phone, cust_email, client_cc_first_digits, client_cc_last_digits, payment_date, order_id))
  conn.commit() 
  try:
    customer = conekta.Customer.create({
      'name': request.form['name'],
      'email': request.form['cust_email'],
      "phone": request.form['cust_phone'],
      'payment_sources': [{
        'type': 'card',
        'token_id': request.form['token_id']
      }]
    })
    orden=order_create(request.form['concept'], request.form['amount'], customer.id, request.form['order_id'])
    return render_template('payment.html', customer_id=customer.id, order_id=orden)

  except conekta.ConektaError as e:
    print(e.message)

def order_create(concept, amount, id, order_id):  
  centesimal=100
  value=int(amount)
  centecimal_value=int(centesimal)
  centecimal_value = value * centecimal_value
  
  conekta.api_key = 'key_ADvMPC2qmR91oC193CFoQA'
  conekta.api_version = "2.0.0"
  conekta.locale = 'es'

  try:
    order = conekta.Order.create({
      "currency": "MXN",
      "line_items": [{
        "name": concept,
        "unit_price": centecimal_value,
        "quantity": 1
      }],
                
      "customer_info": {
        "customer_id": id
      },
      "charges": [{
        "payment_method": {
          "type": "default"
        } 
      }]
    })
    payment_result = {'objec': order.charges[0].object , 'description': order.charges[0].description , 'status': order.charges[0].status , 'amount': str((order.charges[0].amount)/100), 'paid_at': str(order.charges[0].paid_at), 'fee': str(order.charges[0].fee)}
    payment_result_obj = json.dumps(payment_result)
    # payment_result_obj = "object: "+ order.charges[0].object + ", description: "+ order.charges[0].description + ", status: "+ order.charges[0].status + ", amount: " + str((order.charges[0].amount)/100) + ", paid_at: " + str(order.charges[0].paid_at) + ", fee: " + str(order.charges[0].fee)
    order_id = order_id
    conn = database.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute(' UPDATE infopaymentlink SET payment_result_obj = %s WHERE order_id = %s', (payment_result_obj, order_id))
    conn.commit()
    get_paymentInfo(order_id)
  except conekta.ConektaError as e:
    print(e.message)
  return order.id

@app.route('/CCCpayment/<link_id>', methods = ['POST', 'GET'])
def get_paymentCCCInfo(link_id):
  conn = database.connect()
  cur = conn.cursor(pymysql.cursors.DictCursor)
  cur.execute('SELECT order_id, result, payment_processor, payment_result_obj, error_code, error_text, client_cc_first_digits, client_cc_last_digits, cust_email, cust_phone FROM infopaymentlink WHERE link_id = %s', (order_id))
  rows = cur.fetchall()
  cur.close()
  resp = jsonify(rows)
  resp.status_code=200
  return resp

if __name__ == '__main__':
    app.run(port = 3000, debug = True)