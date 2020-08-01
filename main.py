# pip install flask-cors
from flask import Flask, redirect, render_template, jsonify
from flaskext.mysql import MySQL
from flask_cors import CORS

mysql = MySQL()
app = Flask(__name__)
# Set CORS rules (default, all)
CORS(app)
app.config['MYSQL_DATABASE_USER'] = 'x'
app.config['MYSQL_DATABASE_PASSWORD'] = 'x'
app.config['MYSQL_DATABASE_DB'] = 'sakila'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
mysql.init_app(app)

#Make one connection and use it over, and over, and over...
conn = mysql.connect()
# set up a cursor object whihc is what the sql object uses to connect and run queries
cursor = conn.cursor()

@app.route('/api', methods=['GET'])
def customers():
	query = "SELECT name, address, city, `zip code`, sum(payment.amount), staff.username as total FROM customer_list LEFT JOIN payment ON customer_list.id = payment.customer_id LEFT JOIN staff ON customer_list.SID = staff.staff_id LEFT JOIN store ON staff.store_id = store.store_id WHERE SID = 1 GROUP BY name, address, city, `zip code`, staff.username"

	query2 = "SELECT customer.first_name, customer.last_name, address, city, SUM(amount), CONCAT(staff.first_name, ' ', staff.last_name) AS staff_full_name FROM customer INNER JOIN customer_list ON customer.customer_id = customer_list.ID INNER JOIN staff ON staff.store_id = customer.store_id INNER JOIN payment ON payment.customer_id = customer_list.ID WHERE 1 GROUP BY payment.customer_id ORDER BY customer.last_name"

	cursor.execute(query2)
	data = cursor.fetchall()
	data_as_list = list(data)
	# result_as_dictionary = dict(map(None, str(*[iter(1)]*2)))
	return jsonify(results = data_as_list)
	# return render_template('customer.html',data = data)

@app.route('/hambone')
def customers_view():
	return render_template('customers.html')

if __name__ == "__main__":
	app.run(debug=True)
