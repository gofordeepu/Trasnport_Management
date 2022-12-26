from flask import Flask,render_template,request
from datetime import datetime
import sqlite3
# connection to sqlite3
def db_connection():
    con=sqlite3.connect("transport.db")
    return con

app = Flask(__name__)
# homepage
@app.route('/')
def home():
    return render_template("home.html")

# see transactions
@app.route('/transactions')
def see_transactions():
    return render_template("see_transactions.html") 


# add transactions
@app.route('/addtransactions',methods=['GET','POST'])
def add_transactions():
    if request.method=='POST':
        status=''
        company=request.form['company']
        sAdd=request.form['sAdd']
        dAdd=request.form['dAdd']
        sDate = str(request.form['sDate'])
        vehicle=request.form['vehicle']
        con=db_connection()
        cur=con.cursor()
        cur.execute("""insert into transactions  """)
        print(company,sAdd,dAdd,vehicle,sDate)       
        return render_template('add_transactions.html',status=status)
    else:
        con=db_connection()
        cur=con.cursor()
        result=cur.execute("select * from vehicles")
        options=dict(result.fetchall())
        con.close()  
        return render_template("add_transactions.html",options=options.values())

# see vehicals
@app.route('/vehicals')
def see_vehicals():
    return render_template("see_vehicals.html")

 
# main driver function
if __name__ == '__main__':
    app.run(debug=True)