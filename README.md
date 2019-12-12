# BitcoinTrade-System
Team Rocket
Hua Yang/ ShiChao Xu/ChenXiang Ji
A Local crypto currency

Step1:
You should have mysql(include workbench),windows Powershell,visual studio,Python(All latest version)

Step 2:
In mysql
in your local host 
create a new database,like relation_model (if you do not name it 'relation_model',make sure you change database name in python in the future)
use relation_model
import rocket_sql_database.sql in the relation_model

Note:
def get_connection():
    return mc.connect(user = 'root', password = 'yourpassword', host = '127.0.0.1',database = 'relation_model', auth_plugin ='mysql_native_password')
make sure every thing in get_connection() is same in your database

Step3:
Put the app folder under the C/users/your username/
In powershell
pip install flask
pip install mysql_connector_python
pip install websocket
pip install pusher
pip install plotly
pip install apscheduler
$env:FLASK_DEBUG=1
code .
flask run

step 4:

If you refresh website, the price,upl will change every 15 seconds.
A live line graph and bar chart in behind.

Note: You can trade on float. upl = unrealized profit/loss rpl = realized profit/loss vwap = volumn weighted price


