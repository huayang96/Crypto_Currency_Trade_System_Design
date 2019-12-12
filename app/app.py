from flask import Flask
from flask import render_template
from flask import request
import mysql.connector as mc
from flask import Flask, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from pusher import Pusher
import requests, json, atexit, time, plotly, plotly.graph_objs as go


import asyncio
import websockets
import threading

app = Flask(__name__)

@app.route("/")
def main_web():
    conn= get_connection()
    result=conn.cmd_query("select product_name from product")
    crypto_list=conn.get_rows()
    results=conn.cmd_query("select action_type from action")
    action_list=conn.get_rows()
    conn.close()
    p_ls = show_p_l()
    products = show_product()
    orders = show_orders()
    return render_template('index.html', list_of_cryptos=crypto_list[0], list_of_action=action_list[0],p_ls=p_ls,products=products,orders=orders)


# configure pusher object
pusher = Pusher(
    app_id='916651',
    key='1041b4929ec9dd297e03',
    secret='ac4cbd39a9cb20de1a49',
    cluster='us2',
    ssl= True
)

# define variables for data retrieval
times = []
currencies = ["BTC","ETH","LTC"]
prices = {"BTC":[],"ETH":[],"LTC":[]}

def retrieve_data():
    # create dictionary for saving current prices
    current_prices = {}
    for currency in currencies:
        current_prices[currency] = []
    # append new time to list of times
    times.append(time.strftime('%H:%M:%S'))

    # make request to API and get response as object
    api_url = "https://min-api.cryptocompare.com/data/pricemulti?fsyms={}&tsyms=USD".format(",".join(currencies))
    response = json.loads(requests.get(api_url).content)

    # append new price to list of prices for graph
    # and set current price for bar chart
    for currency in currencies:
        price = response[currency]['USD']
        if currency == 'BTC':
            update_price_BTC(price)
        if currency == 'ETH':
            update_price_ETH(price)  
        if currency == 'LTC':
            update_price_LTC(price)         

        current_prices[currency] = price
        prices[currency].append(price)

    # create an array of traces for graph data
    graph_data = [go.Scatter(
        x=times,
        y=prices.get(currency),
        name="{} Prices".format(currency)
        ) for currency in currencies]

    # create an array of traces for bar chart data
    bar_chart_data = [go.Bar(
        x=currencies,
        y=list(current_prices.values())
        )]

    data = {
        'graph': json.dumps(list(graph_data), cls=plotly.utils.PlotlyJSONEncoder),
        'bar_chart': json.dumps(list(bar_chart_data), cls=plotly.utils.PlotlyJSONEncoder)
    }

    # trigger event
    pusher.trigger("crypto", "data-updated", data)

# create schedule for retrieving prices
scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=retrieve_data,
    trigger=IntervalTrigger(seconds=10),
    id='prices_retrieval_job',
    name='Retrieve prices every 10 seconds',
    replace_existing=True)
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

# run Flask app
app.run(debug=True, use_reloader=False)




def get_price(coin_id):
    conn = get_connection()
    # result = conn.cmd_query("select * from product")
    _coin_id = str(coin_id)
    result = conn.cmd_query("select price from product where product_id = " +str(_coin_id)+"")  
    rows =conn.get_rows()
    conn.close()
    price = float(str(rows[0][0][0]))
    return str(price) 


def update_upl_table(Quantity_coin,Pre_Coin_quantity,Coin_price,pre_rpl,Coin_vwap,Product_id,Action_Id):

    if Product_id == 1: 
        if Action_Id == 1:
            if Pre_Coin_quantity == 0:
                Coin_vwap = Coin_price
                Coin_total_qty = Quantity_coin
            else:
                Coin_vwap = (Coin_vwap * Pre_Coin_quantity +Quantity_coin *Coin_price)/(Pre_Coin_quantity + Quantity_coin)
                Pre_Coin_quantity = float(get_qty(Product_id))
                Coin_total_qty =Pre_Coin_quantity + Quantity_coin
            update_p_l_buy(Coin_total_qty,Coin_vwap,Product_id)
        if Action_Id == 2:
            Coin_total_qty = Pre_Coin_quantity - Quantity_coin
            if pre_rpl == 0:
                Coin_rpl = Quantity_coin*(Coin_price-Coin_vwap)
            else:
                Coin_rpl = pre_rpl + Quantity_coin*(Coin_price-Coin_vwap)
            update_p_l_sell(Coin_rpl,Coin_total_qty,Product_id)
        new_vwap_Coin = float(get_vwap(Product_id))
        upl = (Coin_price-new_vwap_Coin )*Coin_total_qty
        update_p_l_upl(upl,Product_id)

    if Product_id == 2: 
        if Action_Id == 1:
            if Pre_Coin_quantity == 0:
                Coin_vwap = Coin_price
                Coin_total_qty = Quantity_coin
            else:
                Coin_vwap = (Coin_vwap * Pre_Coin_quantity +Quantity_coin *Coin_price)/(Pre_Coin_quantity + Quantity_coin)
                Pre_Coin_quantity = float(get_qty(Product_id))
                Coin_total_qty =Pre_Coin_quantity + Quantity_coin
            update_p_l_buy(Coin_total_qty,Coin_vwap,Product_id)
        if Action_Id == 2:
            Coin_total_qty = Pre_Coin_quantity - Quantity_coin

            if pre_rpl == 0:
                Coin_rpl = Quantity_coin*(Coin_price-Coin_vwap)
            else:
                Coin_rpl = pre_rpl + Quantity_coin*(Coin_price-Coin_vwap)
            update_p_l_sell(Coin_rpl,Coin_total_qty,Product_id)
        new_vwap_Coin = float(get_vwap(Product_id))
        upl = (Coin_price-new_vwap_Coin )*Coin_total_qty
        update_p_l_upl(upl,Product_id)

    if Product_id == 3: 
        if Action_Id == 1:
            if Pre_Coin_quantity == 0:
                Coin_vwap = Coin_price
                Coin_total_qty = Quantity_coin
            else:
                Coin_vwap = (Coin_vwap * Pre_Coin_quantity +Quantity_coin *Coin_price)/(Pre_Coin_quantity + Quantity_coin)
                Pre_Coin_quantity = float(get_qty(Product_id))
                Coin_total_qty =Pre_Coin_quantity + Quantity_coin
            update_p_l_buy(Coin_total_qty,Coin_vwap,Product_id)
        if Action_Id == 2:
            Coin_total_qty = Pre_Coin_quantity - Quantity_coin

            if pre_rpl == 0:
                Coin_rpl = Quantity_coin*(Coin_price-Coin_vwap)
            else:
                Coin_rpl = pre_rpl + Quantity_coin*(Coin_price-Coin_vwap)
            update_p_l_sell(Coin_rpl,Coin_total_qty,Product_id)
        new_vwap_Coin = float(get_vwap(Product_id))
        upl = (Coin_price-new_vwap_Coin )*Coin_total_qty
        update_p_l_upl(upl,Product_id)

def update_p_l_upl(upl,Product_id):
    connection = get_connection()
    sql = "UPDATE p_l SET p_l.upl = " +str(upl)+" WHERE product_id = "+str(Product_id)+";"
    result = connection.cmd_query(sql)
    connection.commit()

def update_p_l_buy(qty,vwap,Product_id):
    connection = get_connection()
    sql = "UPDATE p_l SET p_l.qty = " +str(qty)+",p_l.vwap = " +str(vwap)+" WHERE product_id = "+str(Product_id)+";"
    result = connection.cmd_query(sql)
    connection.commit()

def update_p_l_sell(rpl,qty,Product_id):
    connection = get_connection()
    sql = "UPDATE p_l SET p_l.rpl = " +str(rpl)+", p_l.qty = " +str(qty)+" WHERE product_id = "+str(Product_id)+";"
    result = connection.cmd_query(sql)
    connection.commit()

def update_price_BTC(BTCprice):
    connection = get_connection()
    if BTCprice:
        sql = "UPDATE product SET product.price = " +str(BTCprice)+" WHERE product_id = '1';"
        result = connection.cmd_query(sql)
    connection.commit()

def update_price_LTC(LTCprice):
    connection = get_connection()
    if LTCprice:
        sql = "UPDATE product SET product.price = " +str(LTCprice)+" WHERE product_id = '3';"
        result = connection.cmd_query(sql)
    connection.commit()

def update_price_ETH(ETHprice):
    connection = get_connection()
    if ETHprice:
        sql = "UPDATE product SET product.price = " +str(ETHprice)+" WHERE product_id = '2';"
        result = connection.cmd_query(sql)
    connection.commit()




@app.route("/Rocket_processorder",methods = ['get','post'] )
def Rocket_processorder():
    R_Qty = request.form['myqty']
    R_Coin_type = request.form["coin_type"]
    R_act_type = request.form["act_type"]
    Product_list = ['BTC','ETH','LTC']
    Action_list = ['buy','sell']

    Product_id = Product_list.index(R_Coin_type) + 1
    Action_Id = Action_list.index(R_act_type) +1
    Quantity_coin = float(R_Qty)
    Pre_Coin_quantity = float(get_qty(Product_id))
    Coin_price = float(get_price(Product_id))
    pre_rpl = float(get_rpl(Product_id))
    Coin_vwap = float(get_vwap(Product_id))
    if Action_Id == 2 and Pre_Coin_quantity < Quantity_coin:
        return 'No,that is not valid,you do not have that much '+ R_Coin_type
    update_upl_table(Quantity_coin,Pre_Coin_quantity,Coin_price,pre_rpl,Coin_vwap,Product_id,Action_Id)
    insert_order(Product_id,Action_Id,R_Qty)
    return 'You just ' + R_act_type +'  '  + R_Qty +'  ' + R_Coin_type +' at unit price($) '+ str(Coin_price) +' ,this order is processed'


def show_product():
    conn = get_connection()
    result = conn.cmd_query("select product_name,price from product")
    rows =conn.get_rows()
    conn.close()
    return rows[0]

def show_p_l():
    conn = get_connection()
    result = conn.cmd_query("select product_name,round(upl,2),round(rpl,2),round(qty,2),round(vwap,2) from p_l join product on p_l.product_id = product.product_id")

    Quantity_BTC_Coin = float(get_qty(1))
    vwap_BTC_Coin = float(get_vwap(1))
    BTC_price = float(get_price(1))
    BTC_upl = (BTC_price-vwap_BTC_Coin )*Quantity_BTC_Coin
    update_p_l_upl(BTC_upl,1)

    Quantity_ETH_Coin = float(get_qty(2))
    vwap_ETH_Coin = float(get_vwap(2))
    ETH_price = float(get_price(2))
    ETH_upl = (ETH_price-vwap_ETH_Coin )*Quantity_ETH_Coin
    update_p_l_upl(ETH_upl,2)

    Quantity_LTC_Coin = float(get_qty(3))
    vwap_LTC_Coin = float(get_vwap(3))
    LTC_price = float(get_price(3))
    LTC_upl = (LTC_price-vwap_LTC_Coin )*Quantity_LTC_Coin
    update_p_l_upl(LTC_upl,3)

    rows =conn.get_rows()
    conn.close()
    return rows[0]


def show_orders():
    connection = get_connection()
    sql = "select product_name,quantity,transaction_id,coin_price,lastUpdated,action_type from blotter join product on blotter.product_id = product.product_id join action on action.action_id = blotter.action_id order by transaction_id desc limit 5"
    result = connection.cmd_query(sql)
    rows = connection.get_rows()
    connection.close()
    orders = rows[0]
    return orders

def get_rpl(coin_id):
    conn = get_connection()
    # result = conn.cmd_query("select * from product")
    _coin_id = str(coin_id)
    result = conn.cmd_query("select rpl from p_l where product_id = " +str(coin_id)+"")  
    rows =conn.get_rows()
    conn.close()
    rpl = float(str(rows[0][0][0]))
    
    return str(rpl)

def get_vwap(coin_id):
    conn = get_connection()
    # result = conn.cmd_query("select * from product")
    _coin_id = str(coin_id)
    result = conn.cmd_query("select vwap from p_l where product_id = " +str(coin_id)+"")  
    rows =conn.get_rows()
    conn.close()
    vwap = float(str(rows[0][0][0]))
    return str(vwap)

def get_qty(coin_id):
    conn = get_connection()
    # result = conn.cmd_query("select * from product")
    _coin_id = str(coin_id)
    result = conn.cmd_query("select qty from p_l where product_id = " +str(_coin_id)+"")  
    rows =conn.get_rows()
    conn.close()
    qty = float(str(rows[0][0][0]))
    return str(qty)




def insert_order(product_id,action_id,quantity):
    connection = get_connection()

    coin_price =get_price(product_id)
    sql = "insert into blotter (product_id,action_id,quantity,coin_price) values (" +str(product_id)+"," +str(action_id)+"," +str(quantity)+"," +str(coin_price)+");"
    result = connection.cmd_query(sql)
    connection.commit()



def get_connection():
    return mc.connect(user = 'root', password = '123456', host = '127.0.0.1',database = 'relation_model', auth_plugin ='mysql_native_password')

