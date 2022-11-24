from flask import Flask,render_template,request

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
        print(request.form['company'])
        return render_template('add_transactions.html')
    else:
        return render_template("add_transactions.html")

# see vehicals
@app.route('/vehicals')
def see_vehicals():
    return render_template("see_vehicals.html")

 
# main driver function
if __name__ == '__main__':
    app.run(debug=True)