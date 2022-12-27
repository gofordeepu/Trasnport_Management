from flask import Flask,render_template,request,send_file
from datetime import datetime
import sqlite3
import pandas as pd
import os
import pdfkit as pdf
# connection to sqlite3
def db_connection():
    con=sqlite3.connect("transport.db")
    return con

app = Flask(__name__)
# homepage
@app.route('/')
def home():
    try:
        con=db_connection()
        cur=con.cursor()
        cur.execute("select count(tid) from transactions")
        transactions=cur.fetchall()
        print(transactions)
        cur.execute("select count(vid) from vehicles")
        vehicles=cur.fetchall()
        print(vehicles)
    except BaseException as e:
        print(e)
    return render_template("home.html",transactions=transactions[0][0],vehicles=vehicles[0][0])

# see transactions
@app.route('/transactions')
def see_transactions():
    try:
        con=db_connection()
        cur=con.cursor()
        cur.execute("select t.tid,t.company,v.vehiclenumber,t.transaction_date,t.source,t.destination from transactions t join vehicles v on t.vehicle=v.vid order by t.tid desc limit 5")
        tdata=cur.fetchall()
    except BaseException as e:
        print(e)
    return render_template("view_transactions.html",tdata=tdata) 


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
        try:
            con=db_connection()
            cur=con.cursor()
            cur.execute("select count(tid) from transactions")
            count=cur.fetchall()
            print(count)
            cur.execute(f"""insert into transactions(tid,company,vehicle,source,destination,transaction_date)values({count[0][0]+1},'{company}','{vehicle}','{sAdd}','{dAdd}','{sDate}')""")
            con.commit()
            con.close()
            status=1
        except BaseException as e:
            print(e)
            status=0   
        return render_template('add_transactions.html',status=status)
    else:
        con=db_connection()
        cur=con.cursor()
        result=cur.execute("select * from vehicles")
        options=dict(result.fetchall())
        print(options)
        con.close()  
        return render_template("add_transactions.html",options=options)

# see vehicals
@app.route('/vehicals')
def see_vehicals():
    try:
        con=db_connection()
        cur=con.cursor()
        cur.execute("select * from vehicles")
        vehicles=cur.fetchall()
    except BaseException as e:
        print(e)
    return render_template("see_vehicals.html",vehicles=vehicles)


# download the pdf
@app.route('/download',methods=['GET','POST'])
def download():
    try:
        if request.method=='POST':
            fromDate=str(request.form['from'])
            toDate=str(request.form['to'])
            template=f"""<h1>Transactions from {fromDate} to {toDate}"""
            con=db_connection()
            cur=con.cursor()
            query=f"""
            select t.tid,t.company,v.vehiclenumber,t.transaction_date,t.source,t.destination
            from transactions t join vehicles v 
            on t.vehicle=v.vid where(t.transaction_date between '{fromDate}' AND '{toDate}') 
            order by t.transaction_date
            """
            cur.execute(query)
            data=cur.fetchall()
            heading=['transaction_id','Company Name','Vehicle Number','Transaction Date','Source Address','Destination Address']
            df=pd.DataFrame(data,columns=heading)
            transactions=df.to_html(index=False)
            with open('deepu.html','w') as file:
                file.write(template+transactions)
            pdf.from_file('deepu.html','transaction.pdf')
            os.remove('deepu.html')
            return send_file('transaction.pdf') 
    except BaseException as e:
        print(e)
        return "something went wrong"
 
# main driver function
if __name__ == '__main__':
    app.run(debug=True)