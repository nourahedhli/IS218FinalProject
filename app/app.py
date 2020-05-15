from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'gradesData'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Grades Project'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblGrades ')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, grade=result)


@app.route('/view/<int:grad_id>', methods=['GET'])
def record_view(grad_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblGrades WHERE id=%s', grad_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', grad=result[0])


@app.route('/edit/<int:grad_id>', methods=['GET'])
def form_edit_get(grad_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblGrades WHERE id=%s', grad_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', grad=result[0])


@app.route('/edit/<int:grad_id>', methods=['POST'])
def form_update_post(grad_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Last_name'), request.form.get('First_name'), request.form.get('SSN'),
                 request.form.get('Test1'), request.form.get('Test2'),
                 request.form.get('Test3'), request.form.get('Test4'), request.form.get('Final'),
                 request.form.get('Grade'), grad_id)
    sql_update_query = """UPDATE tblGrades t SET t.Last_name = %s, t.First_name = %s, t.SSN= %s, t.Test1 = 
    %s, t.Test2 = %s, t.Test3 = %s,  t.Test4  = %s, t.Final = %s, t.Grade = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/grade/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Grade Form')


@app.route('/grade/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Last_name'), request.form.get('First_name'), request.form.get('SSN'),
                 request.form.get('Test1'), request.form.get('Test2'),
                 request.form.get('Test3'), request.form.get('Test4'), request.form.get('Final'),
                 request.form.get('Grade'))
    sql_insert_query = """INSERT INTO tblGrades (Last_name ,First_name ,SSN ,Test1,Test2,Test3,Test4,Final,
    Grade) VALUES (%s,%s,%s,%s,%s, %s,%s, %s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/delete/<int:grad_id>', methods=['POST'])
def form_delete_post(grad_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tblGrades WHERE id = %s """
    cursor.execute(sql_delete_query, grad_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/grade', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblGrades')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/grade/<int:grad_id>', methods=['GET'])
def api_retrieve(grad_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblGrades WHERE id=%s', grad_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/grade/<int:grad_id>', methods=['PUT'])
def api_edit(grad_id) -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['Last_name'], content['First_name'], content['SSN'],
                 content['Test1'], content['Test2'],
                 content['Test3'], content['Test4'],content['Final'],content['Grade'], grad_id)
    sql_update_query = """UPDATE tblGrades t SET t.Last_name = %s, t.First_name = %s, t.SSN= %s, t.Test1 = 
    %s, t.Test2 = %s, t.Test3 = %s,  t.Test4  = %s, t.Final = %s, t.Grade = %s WHERE t.id = %s  """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/grade', methods=['POST'])
def api_add() -> str:
    content = request.json

    cursor = mysql.get_db().cursor()
    inputData = (content['Last_name'], content['First_name'], content['SSN'],
                 content['Test1'], content['Test2'],
                 content['Test3'], content['Test4'],content['Final'],content['Grade'])
    sql_insert_query =  """INSERT INTO tblGrades (Last_name ,First_name ,SSN ,Test1,Test2,Test3,Test4,Final,
    Grade) VALUES (%s,%s,%s,%s,%s, %s , %s , %s , %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/grade/<int:grad_id>', methods=['DELETE'])
def api_delete(grad_id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tblGrades WHERE id = %s """
    cursor.execute(sql_delete_query, grad_id)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
