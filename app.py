from flask import Flask , request , url_for , redirect , session , render_template , g
from flask.json import jsonify
from flask.wrappers import Request
import sqlite3
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'Thisissecret!'

def connect_db():
    sql = sqlite3.connect("data.db")
    sql.row_factory = sqlite3.Row
    return sql
def get_db():
    if not hasattr(g,'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db
@app.teardown_appcontext
def close_db(error):
    if hasattr(g,'sqlite_db'):
        g.sqlite_db.close()

@app.route('/viewresults')
def viewresults():
    db = get_db()
    cur = db.execute("select * from users")
    results =  cur.fetchall()
    return f"<h1>This id is {results[0]['id']} , name is {results[0]['name']}, the location is {results[0]['location']}</1>"

@app.route('/')
def index():
    session.pop('name',None)
    return "<h1>ยินดีต้อนรับครับ ขอเกรด A นะครับ</1>"

@app.route('/home' ,methods = ['POST','GET'],defaults={'name': 'Test Default'})

@app.route('/home/<string:name>' ,methods = ['POST','GET'])
def home(name):
    session['name'] = name
    db = get_db()
    cur = db.execute("select * from users")
    results = cur.fetchall()

    return render_template('home.html' , name2=name ,display=False 
    ,mylist=['one','two','three'],mylist_of_dict = [{'name' : 'noraphat'},{'name':'somjai'}],results=results), 200 

@app.route('/json')
def json():
    if 'name' in session:
        name  = session['name']
    else:
        name = 'Not Value in Session'
    return jsonify({'key':'velue','listkey':[1,2,3] , 'name': name})

@app.route('/query')
def query():
    name = request.args.get('name')
    location = request.args.get('location')
    return f"<h1>Hi {name} . You are from {location} You are on the query page</h1>"

@app.route('/theform',methods = ['POST','GET'])
def theform():
    if request.method == 'GET':
        return render_template('form.html'), 200 
    else:
        name = request.form['name']
        location = request.form['location']

        db = get_db()
        db.execute("insert into users(name,location) values(?,?)",[name,location])
        db.commit()

        return redirect(url_for('home',name=name))
    
@app.route('/process',methods=['POST'])
def process():
    name = request.form['name']
    location = request.form['location']
    return f"<h1>Hi {name} . You are from {location} You Have summitted the form sucfully!!!</h1>"

@app.route('/processjson',methods=['POST'])
def processjson():
    data = request.get_json()
    name = data['name']
    location = data['location']
    randomlist = data['randomlist']
    return jsonify({'result':'Success!','name': name , 'location' : location, 'randomkey_in_list':randomlist[0]})

if __name__ == '__main__':
    app.run()