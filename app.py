from flask import Flask, request
from makeOrder import make_order, bcolors, change_order

app = Flask(__name__)

@app.route("/accessAfterInsert", methods=['GET', 'POST'])
def accessAfterInsert():
    # for k in request.form:
    #     print(k, request.form[k]) 18641595300
    if request.method == 'POST':
        name_f = request.form['user[name_f]']
        name_l = request.form['user[name_l]']
        email = request.form['user[email]']
        print(bcolors.OKBLUE + 'INSERT')
        print(bcolors.OKGREEN + name_f + ' ' + name_l + ': ' + email + ' ' + request.form['access[product_id]'] + bcolors.ENDC)
        if request.form['access[product_id]'] == '9': 
            print('FOR PRODUCT_ID 9')
            make_order(name_f, name_l, email)
        return "OK"
    else:
        return "TEST"

@app.route("/accessAfterDelete", methods=['GET', 'POST'])
def accessAfterDelete():
    # for k in request.form:
    #     print(k, request.form[k]) 18641595300
    if request.method == 'POST':
        name_f = request.form['user[name_f]']
        name_l = request.form['user[name_l]']
        email = request.form['user[email]']
        print(bcolors.OKBLUE + 'CHANGE')
        print(bcolors.OKGREEN + name_f + ' ' + name_l + ': ' + email + ' ' + request.form['access[product_id]'] + bcolors.ENDC)
        if request.form['access[product_id]'] == '9': 
            print('FOR PRODUCT_ID 9')
            change_order(name_f, name_l, email)
        return "OK"
    else:
        return "TEST"

@app.route("/", methods=['GET'])
def home():
    return "Created By @coder910"