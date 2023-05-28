from flask import *
import ibm_db



conn =ibm_db.connect("DATABASE=bludb;HOSTNAME=764264db-9824-4b7c-82df-40d1b13897c2.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=32536;SECURITY=SSL;SSLServerCertificate=D:/Assignment-2/Flask/DigiCertGlobalRootCA.crt;UID=pgt96221;PWD=6CSjvUvlaf3qh60c",'','')

print('connected')

app = Flask(__name__)

@app.route('/',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        EMAIL = request.form['Email']
        PASSWORD = request.form['Password']
        sql = "SELECT * FROM REGISTER WHERE EMAIL =? AND PASSWORD=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,EMAIL)
        ibm_db.bind_param(stmt,2,PASSWORD)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print (account)
        print(EMAIL,PASSWORD)
        if account:
            flash("Login successful")
            return redirect(url_for('login'))
        else:
            flash("Login unsuccessful. Incorrect username/password !")
            return redirect(url_for('login'))
    return render_template("login.html")

@app.route('/register',methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        NAME=request.form['Name']
        EMAIL=request.form['Email']
        PASSWORD=request.form['Password']
        sql = "SELECT * FROM REGISTER WHERE EMAIL =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,EMAIL)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            flash("You are already a member, please login using your details")
            return render_template('login.html', pred="You are already a member, please login using your details")
        else:
            insert_sql = "INSERT INTO  REGISTER VALUES (?, ?, ?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, NAME)
            ibm_db.bind_param(prep_stmt, 2, EMAIL)
            ibm_db.bind_param(prep_stmt, 3, PASSWORD)
            ibm_db.execute(prep_stmt)
            flash("Registration Successful, please login using your details")
            return render_template('login.html')
    return render_template("register.html")



if __name__ == "__main__":
    app.secret_key = '1234567890'
    app.run(debug = True,port = 8080)