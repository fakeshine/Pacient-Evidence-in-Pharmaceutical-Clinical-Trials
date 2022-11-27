from flask import Flask, redirect, url_for, render_template , request, session
from datetime import timedelta
import pyodbc


app = Flask(__name__)
# We need a key to encrypt and decrypt the data
app.secret_key = "hello"

# We need permanent sessions not to lose all the information about the session when we close our browser
app.permanent_session_lifetime = timedelta(days = 1)


# Define pages - py functions

# Home page
# Where to go to go to the page - route
@app.route("/")
def first_page():
    pacienti = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dbo.PACIENTI")
    for row in cursor.fetchall():
        pacienti.append({"idPacient": row[0] , "Nume": row[1] , "Prenume": row[2] , "CNP": row[3] , "IMC": row[4] , "Istoric": row[5]})
    conn.close()
    return render_template("homepage.html" , pacienti = pacienti)

@app.route("/<name>")
def home(name):
    return render_template("index.html")

@app.route("/login" , methods=["POST" , "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user
        return redirect(url_for("user"))
    else:
        if "user" in session:
            return redirect(url_for("user"))
        return render_template("login.html")

@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return f"<h1>{user}</h1>"
    else:
        return redirect(url_for("login"))
         
# Delete info when someone logs out from the session

@app.route("/logout")
def logout():
    session.pop("user" , None)
    return redirect(url_for("login"))

# DB Connection 

def connection():
    #s = 'DESKTOP-AN3HT4O\SQLEXPRESS' #Your server name 
    #d = 'Evidenta_Pacienti_Testare_Medicamente' 
    #u = 'sa' #Your login
    #p = '00324834' #Your login password
    #cstr = 'DRIVER={ODBC Driver 18 for SQL Server};SERVER='+s+';DATABASE='+d+';UID='+u+';PWD='+ p
    conn = pyodbc.connect('DSN=my_BD_Project;UID=sa;PWD=00324834')
    return conn

if __name__ == "__main__" : 
    app.run(debug=True)