from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flaskext.mysql import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators



#Config MySQL
mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'serviceAdmin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'admin1!'
app.config['MYSQL_DATABASE_DB'] = 'servicedb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql.init_app(app)



#root page
'''
@app.route('/')
def index():
    return render_template('home.html')
'''

#about nie wiem czy potrzebna?? mozna cos wstawic albo wywalic
@app.route('/about')
def about():
    return render_template('about.html')


#Customers
@app.route('/customers')
def customers():
        #cursor
        cursor = mysql.get_db().cursor()

        #get customers

        result = cursor.execute("SELECT * FROM customers")

        customers = cursor.fetchall()

        if result > 0:

            return render_template('customers.html', customers = customers)
        else:
                msg = 'no customers found'
                return render_template('customers.html', msg = msg)

        #close conn
        cursor.close()


#single customer
@app.route('/customer/<string:id>/')
def customer(id):

    #cursor
    cursor = mysql.get_db().cursor()

    #get customer

    result = cursor.execute("SELECT * FROM customers WHERE id= %s", [id])

    customer = cursor.fetchone()



    return render_template('customer.html', customer = customer)

#User login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #Get form fields
        username = request.form['username']
        password_candidate = request.form ['password']



        # cursor
        cursor = mysql.get_db().cursor()

        #get user by username
        result = cursor.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            #taking data
            data = cursor.fetchone()
            password = data[3]

            #compare pass
            if password_candidate == password:
                session['logged_in'] = True
                session['username'] = username

                flash('U are now logged in', 'success')
                return redirect(url_for('dashboard'))
                cursor.close()

            else:
                error = 'Invalid login or password'
                return render_template('login.html', error=error)

        else:
            error = 'Username not found'
            return render_template('login.html', error=error)


    return render_template('login.html')


#logout
@app.route('/logout')
def logout():
    session.clear()
    flash('logged out', 'success')
    return redirect(url_for('login'))


#Dash
@app.route('/dashboard')
def dashboard():

    #cursor
    cursor = mysql.get_db().cursor()

    #get customers

    result = cursor.execute("SELECT * FROM customers")

    customers = cursor.fetchall()

    if result > 0:

        return render_template('dashboard.html', customers = customers)
    else:
            msg = 'no customers found'
            return render_template('dashboard.html', msg = msg)

    #close conn
    cursor.close()



# Customer form
class CustomerForm(Form):
    name = StringField('Name',[validators.Length(min=1, max=20)])
    surname = StringField('Surname',[validators.Length(min=1, max=20)])
    pesel = StringField('PESEL',[validators.Length(min=1, max=11)])
    pattern1 = StringField('pattern1',[validators.Length(min=1, max=100)])
    pattern2 = StringField('pattern2',[validators.Length(min=1, max=100)])
    pattern3 = StringField('pattern3',[validators.Length(min=1, max=100)])
    pattern4 = StringField('pattern4',[validators.Length(min=1, max=100)])
    pattern5 = StringField('pattern5',[validators.Length(min=1, max=100)])
    signature = StringField('signature',[validators.Length(min=1, max=100)])

#Customer ADD
@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    form = CustomerForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        surname = form.surname.data
        pesel = form.pesel.data
        pattern1 = form.pattern1.data
        pattern2 = form.pattern2.data
        pattern3 = form.pattern3.data
        pattern4 = form.pattern4.data
        pattern5 = form.pattern5.data
        signature = form.pattern1.data

        #Cursor
        connection = mysql.connect()
        cursor = connection.cursor()

        #execute
        cursor.execute("INSERT INTO customers(name, surname, pesel, pattern1, pattern2, pattern3, pattern4, pattern5, signature) VALUES(%s, %s, %s,%s, %s, %s,%s, %s, %s)", (name, surname, pesel, pattern1, pattern2, pattern3, pattern4, pattern5, signature))

        #commit
        connection.commit()

        #CLose connection
        cursor.close()

        flash('Customer created', 'success')

        return redirect(url_for('dashboard'))

    return render_template('add_customer.html', form=form)

#edit customer

@app.route('/edit_customer/<string:id>/', methods=['GET', 'POST'])
def edit_customer(id):

    #cursor
    cursor = mysql.get_db().cursor()

    #get customer by id

    result = cursor.execute("SELECT * FROM customers WHERE id = %s", [id])

    customer = cursor.fetchone()

    #form
    form = CustomerForm(request.form)

    #pop customer from fields
    form.name.data = customer[1]
    form.surname.data = customer[2]
    form.pesel.data = customer[3]
    form.pattern1.data = customer[4]
    form.pattern2.data = customer[5]
    form.pattern3.data = customer[6]
    form.pattern4.data = customer[7]
    form.pattern5.data = customer[8]
    form.signature.data = customer[9]

    if request.method == 'POST' and form.validate():
        name = request.form['name']
        surname = request.form['surname']
        pesel = request.form['pesel']
        pattern1 = request.form['pattern1']
        pattern2 = request.form['pattern2']
        pattern3 = request.form['pattern3']
        pattern4 = request.form['pattern4']
        pattern5 = request.form['pattern5']
        signature = request.form['signature']

        #Cursor
        connection = mysql.connect()
        cursor = connection.cursor()

        #execute
        cursor.execute("UPDATE customers SET name=%s, surname=%s, pesel=%s, pattern1=%s, pattern2=%s, pattern3=%s, pattern4=%s, pattern5=%s, signature=%s WHERE id=%s", (name, surname, pesel, pattern1, pattern2, pattern3, pattern4, pattern5, signature, id))

        #commit
        connection.commit()

        #CLose connection
        cursor.close()

        flash('Customer updated', 'success')

        return redirect(url_for('dashboard'))

    return render_template('edit_customer.html', form=form)


#Delete customer
@app.route('/delete_customer/<string:id>', methods=['POST'])
def delete_customer(id):
    #Cursor
    connection = mysql.connect()
    cursor = connection.cursor()

    #execute
    cursor.execute("DELETE FROM customers WHERE id=%s",[id])

    #commit
    connection.commit()

    #CLose connection
    cursor.close()

    flash('Customer deleted', 'success')

    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.secret_key='secure111'
    app.run(debug = True)
