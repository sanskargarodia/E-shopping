from flask import Flask, render_template, request, redirect, url_for,flash,session
#from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
import yaml
from datetime import date
import urllib.parse
import itertools






app = Flask(__name__)
app.secret_key = "super secret key"
db = yaml.load(open("templates/db.yaml"))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@127.0.0.1:3360/dbms_miniproject'
#db = SQLAlchemy(app)

mysql = MySQL(app)
Cust_Id = ''
managerid = ''
@app.route("/", methods=['GET', 'POST'])
def hello():
    global Cust_Id
    if request.method == 'POST':
        logindetails = request.form
        Cust_Id = logindetails['Cust_Id']
        Cust_Password = logindetails['Cust_Password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM dbms_miniproject.customer WHERE Cust_Id = %s AND Cust_Password = %s", [Cust_Id, Cust_Password])
        mysql.connection.commit()
        resultValue = cur.fetchall()
        for i in resultValue:
            if(i[0]):
                return redirect(url_for('miniproject'))
            else:
                flash("VAlid eafdf")

    return render_template('login.html')



@app.route("/login_manager", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        logindetails = request.form
        Manager_Id = logindetails['empid']
        session['empid'] = Manager_Id
        Manager_Password = logindetails['Emp_Password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM dbms_miniproject.employee WHERE empid = %s AND Emp_Password = %s", [Manager_Id, Manager_Password])
        mysql.connection.commit()
        resultValue = cur.fetchall()
        for i in resultValue:
            if (i[0]):
                return redirect(url_for('manager'))
    return render_template("login_manager.html")

Traderid = 0

@app.route("/login_trader", methods=['GET', 'POST'])
def login_trader():
    global Traderid
    if request.method == 'POST':
        logindetails = request.form
        traderid = logindetails['traderid']
        Traderid=traderid
        trader_password = logindetails['trader_password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM dbms_miniproject.trader WHERE traderid = %s AND trader_password = %s", [traderid, trader_password])
        mysql.connection.commit()
        resultValue = cur.fetchall()
        for i in resultValue:
            if (i[0]):
                return redirect(url_for('Trader'))
    return render_template("login_trader.html")



@app.route("/signup_trader", methods=['GET', 'POST'])
def signup_trader():
    if request.method == 'POST':
        userdetails = request.form
        traderid = userdetails['traderid']
        tradername = userdetails['tradername']
        traderloc = userdetails['traderloc']
        traderphone = userdetails['traderphone']
        trader_password = userdetails['trader_password']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO dbms_miniproject.trader values(%s,%s,%s,%s,%s)", (traderid, tradername, traderloc, traderphone, trader_password))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('login_trader'))

    return render_template("signup_trader.html")






@app.route("/manager", methods=['GET', 'POST'])
def manager():
    resultValue = session.get('empid', None)
    cur = mysql.connection.cursor()
    cur.execute("SELECT estore FROM dbms_miniproject.employee WHERE empid = %s", [resultValue])
    mysql.connection.commit()
    data1 = cur.fetchall()
    for i in data1:
        cur.execute("SELECT * FROM dbms_miniproject.stock WHERE storeid=%s", [i[0]])
        mysql.connection.commit()
        session['storeid'] = i[0]
        data = cur.fetchall()
        return render_template("manager.html", data=data)
    return render_template("manager.html")





@app.route("/signup_manager", methods=['GET', 'POST'])
def signup_manager():
    if request.method == 'POST':
        userdetails = request.form
        empid = userdetails['empid']
        session['empid']=empid
        ename = userdetails['ename']
        etype = userdetails['etype']
        ephone = userdetails['ephone']
        eaddress = userdetails['eaddress']
        salary = userdetails['salary']
        estore = userdetails['estore']
        Emp_Password = userdetails['Emp_Password']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO dbms_miniproject.employee values(%s,%s,%s,%s,%s,%s)", (empid, ename, etype, ephone, eaddress, salary, estore, Emp_Password))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('manager'))

    return render_template("signup_manager.html")




@app.route("/miniproject")
def miniproject():
    return render_template('miniproject.html')







@app.route("/signup", methods=['GET', 'POST'])
def signup():
    global Cust_Id
    if request.method == 'POST':
        userdetails = request.form
        Cust_Id = userdetails['Cust_Id']
        Cust_Password = userdetails['Cust_Password']
        Cust_Name = userdetails['Cust_Name']
        Cust_Email = userdetails['Cust_Email']
        Cust_Phone_No = userdetails['Cust_Phone_No']
        Cust_Address = userdetails['Cust_Address']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO dbms_miniproject.customer values(%s,%s,%s,%s,%s,%s)", (Cust_Id, Cust_Name, Cust_Email, Cust_Phone_No, Cust_Address, Cust_Password))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('miniproject'))

    return render_template("signup.html")





@app.route("/Fruits", methods=['GET', 'POST'])
def Fruits():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM dbms_miniproject.product WHERE product_type=%s OR product_type=%s ", ['Fruits', 'Vegetables'])
    mysql.connection.commit()
    data = cur.fetchall()
    return render_template("fruits.html", data=data)



@app.route("/Dairy", methods=['GET', 'POST'])
def Dairy():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM dbms_miniproject.product WHERE product_type=%s", ['Dairy'])
    mysql.connection.commit()
    data = cur.fetchall()
    return render_template("dairy.html", data=data)



@app.route("/PersonalCare", methods=['GET', 'POST'])
def PersonalCare():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM dbms_miniproject.product WHERE product_type=%s", ['Personal Care'])
    mysql.connection.commit()
    data = cur.fetchall()
    return render_template("personalcare.html", data=data)



@app.route("/Vegetables", methods=['GET', 'POST'])
def Vegetables():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM dbms_miniproject.product WHERE product_type=%s OR product_type=%s ", ['Fruits', 'Vegetables'])
    mysql.connection.commit()
    data = cur.fetchall()
    return render_template("fruits.html", data=data)



@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        searchdetails = request.form
        Search = searchdetails['Search']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM dbms_miniproject.product where product_name like %s or product_type like %s", [Search, Search])
        mysql.connection.commit()
        data = cur.fetchall()
        for i in data:
            None;
        if len(data) != 0:
            cur.execute("SELECT * FROM dbms_miniproject.product WHERE product_type = %s", [i[2]])
            mysql.connection.commit()
            data1 = cur.fetchall()
        else:
            cur.execute("SELECT * FROM dbms_miniproject.product")
            mysql.connection.commit()
            data1 = cur.fetchall()
            data = ['empty']
    return render_template("search.html", data=data, data1=data1)









@app.route("/manager_order", methods=['GET','POST'])
def manager_order():
    qty = []
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute("SELECT product_id FROM dbms_miniproject.product")
        mysql.connection.commit()
        product = cur.fetchall()
        x = date.today()
        tobeorder = request.form.getlist('checkboxes')
        storeid = session.get('storeid', None)
        traderid = request.form.getlist('traderid')
        quantity = request.form.getlist('quantity')
        for item in quantity:
            if item != 0:
                qty.append(item)
        for (item, item1, item2) in zip(tobeorder, traderid, qty):
            cur.execute("INSERT INTO dbms_miniproject.order_stock values(%s,%s,%s,%s,%s)", [item, x, item1, storeid, item2])
            mysql.connection.commit()
        cur.execute("SELECT * FROM dbms_miniproject.product")
        mysql.connection.commit()
        data = cur.fetchall()
        cur.execute("SELECT * FROM dbms_miniproject.trader")
        mysql.connection.commit()
        data2 = cur.fetchall()
        return render_template("manager_order.html", data=data, data2=data2)
    return render_template("manager_order.html")



@app.route("/manager_order1", methods=['GET','POST'])
def manager_order1():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute("SELECT product_id FROM dbms_miniproject.product")
        mysql.connection.commit()
        product = cur.fetchall()
        x = date.today()
        tobeorder = request.form['checkboxes']
        storeid = session.get('storeid', None)
        traderid = request.form['traderid']
        quantity = request.form['quantity']
        cur.execute("INSERT INTO dbms_miniproject.order_stock values(%s,%s,%s,%s,%s)", [tobeorder, x, traderid, storeid, quantity])
        mysql.connection.commit()
        cur.execute("SELECT * FROM dbms_miniproject.product")
        mysql.connection.commit()
        data = cur.fetchall()
        cur.execute("SELECT * FROM dbms_miniproject.trader")
        mysql.connection.commit()
        data2 = cur.fetchall()
        return render_template("manager_order.html", data=data, data2=data2)
    return render_template("manager_order.html")




@app.route("/ordered", methods=['GET','POST'])
def ordered():
    if request.method =='POST':
        add=request.form


@app.route("/map", methods=['GET','POST'])
def map():
    cur = mysql.connection.cursor()
    cur.execute("SELECT c.Cust_Address,e.eaddress FROM Customer as c ,employee as e where c.Cust_Id = Cust_Id")
    mysql.connection.commit()
    data1 = cur.fetchall()
    cur.execute("SELECT DISTINCT storeid,storename from dbms_miniproject.store")
    mysql.connection.commit()
    data = cur.fetchall()
    return render_template("map.html", data=data)



@app.route("/HomeCare", methods=['GET', 'POST'])
def HomeCare():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM dbms_miniproject.product WHERE product_type=%s", ['Home Care'])
    mysql.connection.commit()
    data = cur.fetchall()
    return render_template("HomeCare.html", data=data)



@app.route("/Trader", methods=['GET', 'POST'])
def Trader():
    if request.method == 'POST':
        delivery = request.form['delivery']
        cur = mysql.connection.cursor()
        cur.execute(" DELETE FROM dbms_miniproject.order_stock where product_id =%s", [delivery])
        mysql.connection.commit()
        return redirect(url_for('Trader'))
    global Traderid
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM dbms_miniproject.order_stock where traderid = %s", [Traderid])
    mysql.connection.commit()
    data = cur.fetchall()
    cur.execute("SELECT * FROM dbms_miniproject.delivered_stock where traderid = %s", [Traderid])
    mysql.connection.commit()
    data1 = cur.fetchall()

    return render_template("trader.html", data=data, data1=data1)


@app.route("/order_tracking", methods=['GET', 'POST'])
def order_tracking():
    return render_template("order_tracking.html")



@app.route("/redirectmap", methods=['GET', 'POST'])
def redirectmap():
    value = request.form['storeid']
    cur = mysql.connection.cursor()
    cur.execute("SELECT storeid,longitude,latitude FROM dbms_miniproject.store")
    mysql.connection.commit()
    data = cur.fetchall()
    url = "https://apis.mapmyindia.com/advancedmaps/v1/rosqzbkj3fkly2ir1xyfdryymrkihm1k/route_adv/driving/"
    for item in data:
        if value == item[0]:
            getvars = {'item[1]', 'item[2]'}
            urlfinal = (url+'20.5522967,74.516408;'+'20.5590996,74.5159936')
            print(urlfinal)
    return render_template("urlfinal")




@app.route("/login_employee", methods=['GET', 'POST'])
def login_employee():
    if request.method == 'POST':
        global empid
        logindetails = request.form
        empid = logindetails['empid']
        Emp_Password = logindetails['Emp_Password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM dbms_miniproject.employee WHERE empid = %s AND Emp_Password = %s", [empid, Emp_Password])
        mysql.connection.commit()
        resultValue = cur.fetchall()
        for i in resultValue:
            if(i[0]):
                return redirect(url_for('employee'))
    return render_template('login_employee.html')


@app.route("/employee", methods=['GET', 'POST'])
def employee():
    global empid
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM dbms_miniproject.bill b  where storeid=(select estore from dbms_miniproject.employee where empid=%s) and delivery_status='p'",[empid])
    mysql.connection.commit()
    data = cur.fetchall()
    return render_template("employee.html", data=data)

@app.route("/deliver_order", methods=['GET', 'POST'])
def deliver_order():
    if request.method=='POST':
        global empid
        changestatus = request.form
        orderid= changestatus['orderid']
        cur = mysql.connection.cursor()
        cur.execute("insert into dbms_miniproject.deliver_order values (%s,%s,curdate())",[orderid,empid])
        mysql.connection.commit()
        return redirect(url_for('employee'))
    return render_template("employee.html")


@app.route("/cart", methods=['GET','POST'])
def cart():
    if request.method == 'POST':
        global Cust_Id
        additem = request.form
        product_name = additem['product_name']
        price = additem['price']
        cur = mysql.connection.cursor()
        cur.execute("SELECT product_id FROM dbms_miniproject.product WHERE product_name = %s", [product_name])
        mysql.connection.commit()
        product_id = cur.fetchall()
        cur.execute("SELECT product_id FROM dbms_miniproject.cart WHERE product_id = %s and Cust_Id=%s ", [product_id, Cust_Id])
        mysql.connection.commit()
        y = cur.fetchall()
        if y != product_id:
            cur.execute("INSERT INTO dbms_miniproject.cart(Cust_Id, product_id, qty) VALUES(%s,%s,1)", [Cust_Id, product_id])
            mysql.connection.commit()
        cur.execute("SELECT * FROM dbms_miniproject.cart where Cust_Id=%s", [Cust_Id])
        mysql.connection.commit()
        data = cur.fetchall()
        cur.execute("SELECT * FROM dbms_miniproject.product")
        mysql.connection.commit()
        data1 = cur.fetchall()
        cur.execute("select sum(qty*price) from cart c natural join product p where p.product_id=c.product_id and c.Cust_Id=%s",[Cust_Id])
        mysql.connection.commit()
        totalval = cur.fetchall()
        return render_template("cart.html", data=data, data1=data1, totalval=totalval)
    return render_template("cart.html")


@app.route("/cart2", methods=['GET','POST'])
def cart2():
    global Cust_Id
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM dbms_miniproject.cart where Cust_Id =%s", [Cust_Id])
    mysql.connection.commit()
    data = cur.fetchall()
    cur.execute("SELECT * FROM dbms_miniproject.product")
    mysql.connection.commit()
    data1 = cur.fetchall()
    cur.execute("select sum(qty*price) from cart c natural join product p where p.product_id=c.product_id and c.Cust_Id=%s", [Cust_Id])
    mysql.connection.commit()
    totalval = cur.fetchall()
    return render_template("cart.html", data=data, data1=data1, totalval=totalval)


@app.route("/add", methods=['GET','POST'])
def add():
    if request.method == 'POST':
        global Cust_Id
        add=request.form
        addtocart = add['Quantity']
        product_id = add['product_id']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE cart SET qty=%s WHERE product_id=%s and Cust_Id=%s", [addtocart, product_id,Cust_Id])
        mysql.connection.commit()
        cur.execute("SELECT * FROM dbms_miniproject.cart where Cust_Id=%s",[Cust_Id])
        mysql.connection.commit()
        data = cur.fetchall()
        cur.execute("SELECT * FROM dbms_miniproject.product")
        mysql.connection.commit()
        data1 = cur.fetchall()
        cur.execute("select sum(qty*price) from cart c natural join product p where p.product_id=c.product_id and c.Cust_Id=%s",[Cust_Id])
        mysql.connection.commit()
        totalval = cur.fetchall()
        return render_template("cart.html", data=data, data1=data1, totalval=totalval)
    return render_template("cart.html")

@app.route("/remove", methods=['GET','POST'])
def remove():
    if request.method == 'POST':
        global Cust_Id
        remove = request.form
        product_id = remove['product_id']
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM cart WHERE product_id=%s and Cust_Id=%s", [product_id,Cust_Id])
        mysql.connection.commit()
        cur.execute("SELECT * FROM dbms_miniproject.cart where Cust_Id=%s",[Cust_Id])
        mysql.connection.commit()
        data = cur.fetchall()
        cur.execute("SELECT * FROM dbms_miniproject.product")
        mysql.connection.commit()
        data1 = cur.fetchall()
        cur.execute("select sum(qty*price) from cart c natural join product p where p.product_id=c.product_id and c.Cust_Id=%s",[Cust_Id])
        mysql.connection.commit()
        totalval = cur.fetchall()
        return render_template("cart.html", data=data, data1=data1, totalval=totalval)
    return render_template("cart.html")


@app.route("/checkout", methods=['GET','POST'])
def checkout():
    if request.method == 'POST':
        global Cust_Id
        checkout = request.form
        storeid = checkout['storeid']
        cur = mysql.connection.cursor()
        cur.execute("call checkout(%s,%s)",[storeid,Cust_Id])
        mysql.connection.commit()
        return render_template("miniproject.html")
    return render_template("miniproject.html")


@app.route("/order_history", methods=['GET', 'POST'])
def order_history():
    if request.method == 'POST':
        global Cust_Id
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM dbms_miniproject.bill WHERE Cust_Id = %s", [Cust_Id])
        mysql.connection.commit()
        data = cur.fetchall()
        cur.execute("SELECT * FROM dbms_miniproject.order_details o inner join dbms_miniproject.product p where p.product_id=o.product_id ")
        mysql.connection.commit()
        data1 = cur.fetchall()
        return render_template("order_history.html", data=data, data1=data1)
    return render_template("order_history.html")






if __name__ == '__main__' :
    app.run(debug=True)
