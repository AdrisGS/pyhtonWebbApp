# import ssl
import time
import pymysql
import datetime
from services.linkShortener import tiny_url
from flask import Flask, render_template, jsonify, request
from flaskext.mysql import MySQL
# from functools import wraps

# context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
# context.load_cert_chain('server.crt', 'server.key')

app = Flask(__name__)
database = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '2133010323Gl?'
app.config['MYSQL_DATABASE_DB'] = 'paymentlink'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'

database.init_app(app)

# # The actual decorator function
# def require_appkey(view_function):
#     @wraps(view_function)
#     # the new, post-decoration function. Note *args and **kwargs here.
#     def decorated_function(*args, **kwargs):
#         with open('api.key', 'r') as apikey:
#             key=apikey.read().replace('\n', '')
#         #if request.args.get('key') and request.args.get('key') == key:
#         if request.headers.get('x-api-key') and request.headers.get('x-api-key') == key:
#             return view_function(*args, **kwargs)
#         else:
#             abort(401)
#     return decorated_function

@app.route('/')
def Index():
    return render_template('addInfo.html')

@app.route('/payment', methods=['POST'])
# @require_appkey
def add_paymentInfo():
    if request.method == 'POST':
        order_id = request.form['order_id']
        phone_number = request.form['phone_number']
        payment_amount = request.form['payment_amount']
        payment_concept = request.form['payment_concept']
        business_name = request.form['business_name']
        business_logo_url = request.form['business_logo_url']
        result = "OK"
        long_url = 'http://127.0.0.1:3000/cccPayment/'+order_id
        link_url = tiny_url(long_url)
        creation_date = datetime.datetime.now()
        conn = database.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute('INSERT INTO infopaymentlink (order_id, phone_number, payment_amount, payment_concept, business_name, business_logo_url, result, long_url, link_url, creation_date ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s )',
        (order_id, phone_number, payment_amount, payment_concept, business_name, business_logo_url, result, long_url, link_url, creation_date))
        conn.commit()
        return 'Hecho'
        # resp = jsonify(rows)
        # resp.status_code=200
        # return resp

@app.route('/paymentJSON', methods=['POST'])
# @require_appkey
def add_paymentInfoJSON():
    if request.method == 'POST':
        order_id = request.args.get('order_id', '')
        phone_number = request.args.get('phone_number', '')
        payment_amount = request.args.get('payment_amount', '')
        payment_concept = request.args.get('payment_concept', '')
        business_name = request.args.get('business_name', '')
        business_logo_url = request.args.get('business_logo_url', '')
        result = "OK"
        long_url = 'http://127.0.0.1:3000/cccPayment/'+order_id
        link_url = tiny_url(long_url)
        creation_date = datetime.datetime.now()
        conn = database.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute('INSERT INTO infopaymentlink (order_id, phone_number, payment_amount, payment_concept, business_name, business_logo_url, result, long_url, link_url, creation_date ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s )',
        (order_id, phone_number, payment_amount, payment_concept, business_name, business_logo_url, result, long_url, link_url, creation_date))
        conn.commit()
        return 'Hecho'

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

@app.route('/getallInfo', methods = ['POST', 'GET'])
def get_allData():
  conn = database.connect()
  cur = conn.cursor(pymysql.cursors.DictCursor)
  cur.execute('SELECT * FROM infopaymentlink')
  rows = cur.fetchall()
  cur.close()
  resp = jsonify(rows)
  resp.status_code=200
  return resp


@app.route('/cccPayment/<order_id>', methods = ['POST', 'GET'])
def get_paymentLink(order_id):
  conn = database.connect()
  cur = conn.cursor(pymysql.cursors.DictCursor)
  cur.execute('SELECT phone_number, payment_amount, payment_concept, business_name, business_logo_url FROM infopaymentlink WHERE order_id = %s', (order_id))
  rows = cur.fetchall()
  cur.close()
  print (rows[0])
  return render_template('paymentCard.html', paymentInfo = rows[0])

@app.route('/paymentComplete', methods=['POST', 'GET'])
# @require_appkey
def add_paymentInfoAndJsonOutput():
    if request.method == 'POST':
        order_id = request.form['order_id']
        phone_number = request.form['phone_number']
        payment_amount = request.form['payment_amount']
        payment_concept = request.form['payment_concept']
        business_name = request.form['business_name']
        business_logo_url = request.form['business_logo_url']
        result = "OK"
        long_url = 'http://127.0.0.1:3000/cccPayment/'+order_id
        link_url = tiny_url(long_url)
        creation_date = datetime.datetime.now()
        conn = database.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute('INSERT INTO infopaymentlink (order_id, phone_number, payment_amount, payment_concept, business_name, business_logo_url, result, long_url, link_url, creation_date ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s )',
        (order_id, phone_number, payment_amount, payment_concept, business_name, business_logo_url, result, long_url, link_url, creation_date))
        conn.commit()
        cur.execute('SELECT result, link_id, link_url, error_code, error_text  FROM infopaymentlink WHERE order_id = %s', (order_id))
        rows = cur.fetchall()
        cur.close()
        resp = jsonify(rows)
        resp.status_code=200
        return resp

if __name__ == '__main__':
    app.run(port = 3000, debug = True)