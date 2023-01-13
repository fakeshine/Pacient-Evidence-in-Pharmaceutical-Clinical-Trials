from flask import Flask, redirect, url_for, render_template , request, session
from datetime import timedelta
# from flask_session import Session
# from flask_cors import CORS
import pyodbc
from datetime import datetime



app = Flask(__name__)
# We need a key to encrypt and decrypt the data
app.secret_key = "hello"

# We need permanent sessions not to lose all the information about the session when we close our browser
app.permanent_session_lifetime = timedelta(days = 1)
# app.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True)
app.config.from_object(__name__)
# Session(app)
# CORS(app)


# Define pages - py functions

# Home page

@app.route("/", methods = ['GET','POST'])
def home_page():

    return render_template("homepage.html")
    

# Web page with search filter having multiple search criteria and the table of results shown below

@app.route("/find_study", methods = ['GET','POST'])
def find_study():

    if request.method == 'GET' :
        if request.path == '/all_studies_results':
            return redirect(url_for('all_studies_results'))
        else :
            return render_template('find_study.html')

    if request.method == 'POST' :
        
        disease              = request.form['disease']
        physician_first_name = request.form['physician_first_name']
        physician_last_name  = request.form['physician_last_name']
        drug_name            = request.form['drug_name']
        drug_manufacturer    = request.form['drug_manufacturer']
        active_ingredient    = request.form['active_ingredient']
        no_min_drugs         = request.form['no_min_drugs']
        physician_specialty  = request.form['physician_specialty']


        # print (request.form['disease'])
        # print (request.form['physician_first_name'])
        # print (request.form['physician_last_name'])
        # print (request.form['drug_name'])
        # print (request.form['drug_manufacturer'])
        # print (request.form['active_ingredient'])
        # print (request.form['no_min_drugs'])
        # print (request.form['physician_specialty'])

        studies = []

        

        if request.form['disease'] != '' and request.form['physician_first_name'] == '' and request.form['physician_last_name'] == '' and request.form['drug_name'] == '' and request.form['drug_manufacturer'] == '' and request.form['active_ingredient'] == '' and request.form['no_min_drugs'] == '' and request.form['physician_specialty'] == '':

            conn = connection()
            cursor = conn.cursor()

            studies_aux = cursor.execute('''    SELECT DISTINCT S.Denumire_Studiu , S.Boala_Tinta, M.Denumire_Medicament , M.Producator , M.Substanta_Activa , CP.Nume +' '+ CP.Prenume AS Nume_Medic ,
                                              (SELECT COUNT(*) FROM PACIENTI AS P INNER JOIN ISTORIC_STUDII_PACIENTI ISP2 ON ISP2.ID_Pacient = P.ID_Pacient WHERE P.ID_Pacient = ISP.ID_Pacient) 
                                               AS Pacients_enrolled
                                                FROM ISTORIC_STUDII_PACIENTI AS ISP INNER JOIN STUDII AS S ON ISP.ID_Studiu = S.ID_Studiu
                                                INNER JOIN MEDICAMENTE AS M ON S.ID_Medicament = M.ID_Med
                                                INNER JOIN COORDONATORI_PROIECT AS CP ON S.ID_Coordonator = CP.ID_Coordonator
                                                WHERE S.Boala_Tinta = ? ''' , disease).fetchall()

            conn.commit()

            for row in studies_aux:
                studies.append({"Denumire_Studiu": row[0] , "Boala_Tinta": row[1] , "Denumire_Medicament": row[2] , "Producator": row[3] , "Substanta_Activa": row[4] , "Doctor_Name": row[5], "Pacients_enrolled": row[6]})
        # print (studies)
            conn.close()
        
        if request.form['disease'] != '' and request.form['physician_first_name'] != '' and request.form['physician_last_name'] != '' and request.form['drug_name'] == '' and request.form['drug_manufacturer'] == '' and request.form['active_ingredient'] == '' and request.form['no_min_drugs'] == '' and request.form['physician_specialty'] == '':

            conn = connection()
            cursor = conn.cursor()

            studies_aux = cursor.execute('''SELECT DISTINCT S.Denumire_Studiu , S.Boala_Tinta, M.Denumire_Medicament , M.Producator , M.Substanta_Activa , 
                                              CP.Nume +' '+ CP.Prenume AS Nume_Medic ,(SELECT COUNT(*) FROM PACIENTI AS P INNER JOIN ISTORIC_STUDII_PACIENTI ISP2 ON ISP2.ID_Pacient = P.ID_Pacient 
                                              WHERE P.ID_Pacient = ISP.ID_Pacient) AS Pacients_enrolled
                                            FROM ISTORIC_STUDII_PACIENTI AS ISP INNER JOIN STUDII AS S ON ISP.ID_Studiu = S.ID_Studiu
                                            INNER JOIN MEDICAMENTE AS M ON S.ID_Medicament = M.ID_Med
                                            INNER JOIN COORDONATORI_PROIECT AS CP ON S.ID_Coordonator = CP.ID_Coordonator
                                            WHERE S.Boala_Tinta = ? AND CP.Prenume = ? AND CP.Nume = ?''' , disease , physician_first_name , physician_last_name).fetchall()

            conn.commit()

            # print(studies_aux)

            for row in studies_aux:
                studies.append({"Denumire_Studiu": row[0] , "Boala_Tinta": row[1] , "Denumire_Medicament": row[2] , "Producator": row[3] , "Substanta_Activa": row[4] , "Doctor_Name": row[5], "Pacients_enrolled": row[6]})
            # print (studies)
            conn.close()

        elif request.form['disease'] != '' and request.form['physician_first_name'] != '' and request.form['physician_last_name'] != '' and request.form['drug_name'] == '' and request.form['drug_manufacturer'] == '' and request.form['active_ingredient'] != '' and request.form['no_min_drugs'] == '' and request.form['physician_specialty'] == '':

            conn = connection()
            cursor = conn.cursor()

            studies_aux = cursor.execute('''SELECT DISTINCT S.Denumire_Studiu , S.Boala_Tinta, M.Denumire_Medicament , M.Producator , M.Substanta_Activa , 
                                                CP.Nume +' '+ CP.Prenume AS Nume_Medic ,(SELECT COUNT(*) FROM PACIENTI AS P 
                                                INNER JOIN ISTORIC_STUDII_PACIENTI ISP2 ON ISP2.ID_Pacient = P.ID_Pacient WHERE P.ID_Pacient = ISP.ID_Pacient) AS Pacients_enrolled
                                            FROM ISTORIC_STUDII_PACIENTI AS ISP INNER JOIN STUDII AS S ON ISP.ID_Studiu = S.ID_Studiu
                                            INNER JOIN MEDICAMENTE AS M ON S.ID_Medicament = M.ID_Med
                                            INNER JOIN COORDONATORI_PROIECT AS CP ON S.ID_Coordonator = CP.ID_Coordonator
                                WHERE S.Boala_Tinta = ? AND CP.Prenume = ? AND CP.Nume = ? AND M.Substanta_Activa = ? ''' , disease , physician_first_name , physician_last_name, active_ingredient).fetchall()

            conn.commit()

            for row in studies_aux:
                studies.append({"Denumire_Studiu": row[0] , "Boala_Tinta": row[1] , "Denumire_Medicament": row[2] , "Producator": row[3] , "Substanta_Activa": row[4] , "Doctor_Name": row[5], "Pacients_enrolled": row[6]})
            # print (studies)
            conn.close()

        elif request.form['disease'] != '' and request.form['physician_first_name'] != '' and request.form['physician_last_name'] != '' and request.form['drug_name'] != '' and request.form['drug_manufacturer'] != '' and request.form['active_ingredient'] != '' and request.form['no_min_drugs'] == '' and request.form['physician_specialty'] == '':

            conn = connection()
            cursor = conn.cursor()

            studies_aux = cursor.execute('''SELECT DISTINCT S.Denumire_Studiu , S.Boala_Tinta, M.Denumire_Medicament , M.Producator , M.Substanta_Activa , 
                                                CP.Nume +' '+ CP.Prenume AS Nume_Medic ,(SELECT COUNT(*) FROM PACIENTI AS P 
                                                INNER JOIN ISTORIC_STUDII_PACIENTI ISP2 ON ISP2.ID_Pacient = P.ID_Pacient WHERE P.ID_Pacient = ISP.ID_Pacient) AS Pacients_enrolled
                                            FROM ISTORIC_STUDII_PACIENTI AS ISP INNER JOIN STUDII AS S ON ISP.ID_Studiu = S.ID_Studiu
                                            INNER JOIN MEDICAMENTE AS M ON S.ID_Medicament = M.ID_Med
                                            INNER JOIN COORDONATORI_PROIECT AS CP ON S.ID_Coordonator = CP.ID_Coordonator
                                            WHERE S.Boala_Tinta = ? AND CP.Prenume = ? AND CP.Nume = ? AND M.Substanta_Activa = ? AND M.Denumire_Medicament = ? AND M.Producator = ?''' 
                                            , disease , physician_first_name , physician_last_name, active_ingredient , drug_name , drug_manufacturer).fetchall()

            conn.commit()

            for row in studies_aux:
                studies.append({"Denumire_Studiu": row[0] , "Boala_Tinta": row[1] , "Denumire_Medicament": row[2] , "Producator": row[3] , "Substanta_Activa": row[4] , "Doctor_Name": row[5], "Pacients_enrolled": row[6]})
            # print (studies)
            conn.close()


        elif request.form['disease'] != '' and request.form['physician_first_name'] == '' and request.form['physician_last_name'] == '' and request.form['drug_name'] == '' and request.form['drug_manufacturer'] == '' and request.form['active_ingredient'] == '' and request.form['no_min_drugs'] != '' and request.form['physician_specialty'] == '':

            conn = connection()
            cursor = conn.cursor()

            studies_aux = cursor.execute('''SELECT DISTINCT S.Denumire_Studiu , S.Boala_Tinta, M.Denumire_Medicament , M.Producator , M.Substanta_Activa , 
                                                CP.Nume +' '+ CP.Prenume AS Nume_Medic ,(SELECT COUNT(*) FROM PACIENTI AS P 
                                                INNER JOIN ISTORIC_STUDII_PACIENTI ISP2 ON ISP2.ID_Pacient = P.ID_Pacient WHERE P.ID_Pacient = ISP.ID_Pacient) AS Pacients_enrolled
                                            FROM ISTORIC_STUDII_PACIENTI AS ISP INNER JOIN STUDII AS S ON ISP.ID_Studiu = S.ID_Studiu
                                            INNER JOIN MEDICAMENTE AS M ON S.ID_Medicament = M.ID_Med
                                            INNER JOIN COORDONATORI_PROIECT AS CP ON S.ID_Coordonator = CP.ID_Coordonator
                                            WHERE S.Boala_Tinta = ? AND ? <= (SELECT COUNT(*) AS no_min_drug FROM MEDICAMENTE AS M2 WHERE M2.Producator = M.Producator)''' 
                                            , disease , no_min_drugs).fetchall()

            conn.commit()

            for row in studies_aux:
                studies.append({"Denumire_Studiu": row[0] , "Boala_Tinta": row[1] , "Denumire_Medicament": row[2] , "Producator": row[3] , "Substanta_Activa": row[4] , "Doctor_Name": row[5], "Pacients_enrolled": row[6]})
        # print (studies)
            conn.close()


        elif request.form['disease'] == '' and request.form['physician_first_name'] == '' and request.form['physician_last_name'] == '' and request.form['drug_name'] == '' and request.form['drug_manufacturer'] == '' and request.form['active_ingredient'] == '' and request.form['no_min_drugs'] == '' and request.form['physician_specialty'] != '':

            conn = connection()
            cursor = conn.cursor()

            studies_aux = cursor.execute('''SELECT DISTINCT S.Denumire_Studiu , S.Boala_Tinta , M.Denumire_Medicament , M.Producator , M.Substanta_Activa , 
                                                    CP.Nume +' '+ CP.Prenume AS Nume_Medic ,(SELECT COUNT(*) FROM PACIENTI AS P
                                                    INNER JOIN ISTORIC_STUDII_PACIENTI ISP2 ON ISP2.ID_Pacient = P.ID_Pacient WHERE P.ID_Pacient = ISP.ID_Pacient) AS Pacients_enrolled
                                            FROM ISTORIC_STUDII_PACIENTI AS ISP INNER JOIN STUDII AS S ON ISP.ID_Studiu = S.ID_Studiu
                                            INNER JOIN MEDICAMENTE AS M ON S.ID_Medicament = M.ID_Med
                                            INNER JOIN COORDONATORI_PROIECT AS CP ON S.ID_Coordonator = CP.ID_Coordonator
                                            WHERE CP.Specializare = ?''' , physician_specialty).fetchall()

            conn.commit()

            for row in studies_aux:
                studies.append({"Denumire_Studiu": row[0] , "Boala_Tinta": row[1] , "Denumire_Medicament": row[2] , "Producator": row[3] , "Substanta_Activa": row[4] , "Doctor_Name": row[5], "Pacients_enrolled": row[6]})
        # print (studies)
            conn.close()    

        return render_template('find_study.html' , studies = studies)
    

# Page with all pacients in our database

@app.route("/pacient_list")
def pacient_list():
    pacienti = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT P.Nume, P.Prenume, P.CNP, P.Indice_Masa_Corporala, P.Istoric_Medical FROM dbo.PACIENTI AS P")
    for row in cursor.fetchall():
        pacienti.append({"Nume": row[0] , "Prenume": row[1] , "CNP": row[2] , "IMC": row[3] , "Istoric": row[4]})
    conn.commit()
    conn.close()
    return render_template("pacient_list.html" , pacienti = pacienti)

# All pacients enrolled in clinical pharmaceutical trials

@app.route("/pacients_enrolled")
def pacients_enrolled():
    pacients = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(''' SELECT P.Nume, P.Prenume, P.CNP, P.Indice_Masa_Corporala, P.Istoric_Medical, S.Denumire_Studiu , 
                        ISP.Data_Start, ISP.Data_Stop, ISP.Frecventa_Administrare, ISP.Cantitate_Administrare
                       FROM dbo.PACIENTI AS P INNER JOIN ISTORIC_STUDII_PACIENTI AS ISP ON P.ID_Pacient = ISP.ID_Pacient
					                          INNER JOIN STUDII AS S ON ISP.ID_Studiu = S.ID_Studiu''')
    for row in cursor.fetchall():
        pacients.append({"Last_Name": row[0] , "First_Name": row[1] , "CNP": row[2] , "BMI": row[3] , "Med_history": row[4] , "Study_Title": row[5] , "Start_Date": row[6] , "Stop_Date": row[7] , "Drug_Frequency": row[8] , "Drug_Quantity": row[9]})
    conn.commit()
    conn.close()
    return render_template("pacients_enrolled.html" , pacients = pacients)

# All drugs enlisted in our databse

@app.route("/drugs")
def drugs():
    drugs = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute('''  SELECT M.Denumire_Medicament , RA.Denumire_Reactie_Adversa
                        FROM REACTII_ADVERSE_PACIENTI AS RAP INNER JOIN ISTORIC_STUDII_PACIENTI AS ISP ON RAP.ID_Istoric_Studiu_Pacienti = ISP.ID_Istoric
                                                             INNER JOIN STUDII AS S ON ISP.ID_Studiu = S.ID_Studiu
                                                             INNER JOIN MEDICAMENTE AS M ON S.ID_Medicament = M.ID_Med
                                                             INNER JOIN REACTII_ADVERSE AS RA ON RAP.ID_Reactie_Adversa = RA.ID_Reactie_Adversa
                        GROUP BY M.Denumire_Medicament , RA.Denumire_Reactie_Adversa , RA.ID_Reactie_Adversa
                        ORDER BY M.Denumire_Medicament ASC''')
    for row in cursor.fetchall():
        drugs.append({"Drug_Name": row[0] , "Side_Effect": row[1]})
    conn.commit()
    conn.close()
    return render_template("drugs.html" , drugs = drugs)


# All our Doctors who are Study Managers

@app.route("/doctors")
def doctors():
    doctors = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute('''  SELECT CP.Nume + ' ' + CP.Prenume AS Doctor_Name , S.Denumire_Studiu 
                        FROM STUDII AS S INNER JOIN COORDONATORI_PROIECT AS CP ON S.ID_Coordonator = CP.ID_Coordonator
                        ORDER BY Doctor_Name ASC ''')
    for row in cursor.fetchall():
        doctors.append({"Doctor_Name": row[0] , "Study_Title": row[1]})
    conn.commit()
    conn.close()
    return render_template("doctors.html" , doctors = doctors)
    

# All clinical trials shown in a table form, after clicking the "All Studies" button on homepage search filter

@app.route("/all_studies_results")
def all_studies_results():
    studies = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT DISTINCT S.Denumire_Studiu , S.Boala_Tinta , M.Denumire_Medicament , M.Producator , M.Substanta_Activa , 
                            CP.Nume +' '+ CP.Prenume AS Nume_Medic ,(SELECT COUNT(*) FROM PACIENTI AS P 
                            INNER JOIN ISTORIC_STUDII_PACIENTI ISP2 ON ISP2.ID_Pacient = P.ID_Pacient WHERE P.ID_Pacient = ISP.ID_Pacient) AS Pacients_enrolled
                    FROM ISTORIC_STUDII_PACIENTI AS ISP INNER JOIN STUDII AS S ON ISP.ID_Studiu = S.ID_Studiu
					INNER JOIN MEDICAMENTE AS M ON S.ID_Medicament = M.ID_Med
					INNER JOIN COORDONATORI_PROIECT AS CP ON S.ID_Coordonator = CP.ID_Coordonator
                    ORDER BY S.Denumire_Studiu DESC''')
    studies.clear()
    for row in cursor.fetchall():
        studies.append({"Denumire_Studiu": row[0] , "Boala_Tinta": row[1] , "Denumire_Medicament": row[2] , "Producator": row[3] , "Substanta_Activa": row[4] , "Doctor_Name": row[5], "Pacients_enrolled": row[6]})
    conn.commit()
    conn.close()
    return render_template("all_studies_results.html" , studies = studies)


# Delete studies

@app.route('/delete/<string:study_title>', methods=['GET','POST'])
def delete(study_title):
    conn = connection()
    cursor = conn.cursor()
    id_study_to_delete = cursor.execute('SELECT S.ID_Studiu FROM dbo.STUDII S WHERE S.Denumire_Studiu = ?' , study_title).fetchone()
    cursor.commit()
    # Delete Studii
    # for cu Delete Istoric_Studii_Pacienti pentru fiecare inregistrare care are ID_Studiu = id

    cursor.execute('DELETE FROM dbo.ISTORIC_STUDII_PACIENTI WHERE ID_Studiu = ?' , id_study_to_delete)
    cursor.commit()
    cursor.execute('DELETE FROM dbo.STUDII WHERE ID_Studiu = ?' , id_study_to_delete)
    cursor.commit()
    cursor.close()
    return redirect(url_for('all_studies_results'))

# Enroll pacient in clinical study page. You will be redirected here after clicking on "Enroll in Study" button on the top of any page

@app.route("/pacient_add" , methods = ['GET','POST'])
def pacient_add(): 
    
    if request.method == 'GET' :
         return render_template("pacient_add.html")
    elif request.method == 'POST' :

        pacient_first_name = str(request.form['pacient_first_name'])
        pacient_last_name  = str(request.form['pacient_last_name'])
        cnp                = str(request.form['cnp'])
        study_title        = str(request.form['study_title'])
        medical_history    = str(request.form['medical_history'])
        start_year         = int(request.form['start_year'])
        start_month        = int(request.form['start_month'])
        start_day          = int(request.form['start_day'])


        # print(pacient_first_name)
        # print (pacient_last_name)
        # print (cnp)
        # print (study_title)
        # print (medical_history)
        # print (start_year)
        # print (start_month)
        # print (start_day)

        start_date = datetime(start_year, start_month, start_day)

        conn   = connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO dbo.PACIENTI (Nume, Prenume, CNP, Indice_Masa_Corporala , Istoric_Medical) VALUES (?, ?, ?, ? , ?)", 
                        pacient_last_name, pacient_first_name, cnp, "unknown" , medical_history)
        conn.commit()
        conn.close()

        conn   = connection()
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO dbo.ISTORIC_STUDII_PACIENTI (ID_Studiu, ID_Pacient, Data_Start) 
        VALUES ((SELECT S.ID_Studiu FROM STUDII S WHERE S.Denumire_Studiu = ?) , (SELECT P.ID_Pacient FROM PACIENTI P WHERE P.CNP = ?), ?''', study_title, cnp , start_date)
        conn.commit()
        conn.close()

        # return render_template("pacient_add.html")
        return redirect('/')

# Update pacient data page. You will be redirected here after clicking on "Update Pacient Data" button on the top of any page

@app.route("/update_pacient_data", methods = ['GET','POST'])
def update_pacient_data():

    if request.method == 'GET' :
         return render_template("update_pacient_data.html")
    elif request.method == 'POST' :

        cnp                = str(request.form['cnp'])
        study_title        = str(request.form['study_title'])
        pacient_first_name = str(request.form['pacient_first_name'])
        pacient_last_name  = str(request.form['pacient_last_name'])
        bmi                = str(request.form['bmi'])
        drug_frequency     = str(request.form['drug_frequency'])
        drug_quantity      = str(request.form['drug_quantity'])
        stop_year          = int(request.form['stop_year'])
        stop_month         = int(request.form['stop_month'])
        stop_day           = int(request.form['stop_day'])

        stop_date = datetime(stop_year, stop_month, stop_day)
        
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE dbo.PACIENTI SET Nume = ?, Prenume = ? , Indice_Masa_Corporala = ? WHERE ID_Pacient = (SELECT P.ID_Pacient FROM PACIENTI P WHERE P.CNP = ?)"
                        , pacient_last_name, pacient_first_name, bmi, cnp)
        conn.commit()
        conn.close()

        conn = connection()
        cursor = conn.cursor()
        cursor.execute('''UPDATE dbo.ISTORIC_STUDII_PACIENTI SET Frecventa_Administrare = ? , Cantitate_Administrare = ? , Data_Stop = ? 
                        WHERE ID_Studiu = (SELECT S.ID_Studiu FROM STUDII S WHERE S.Denumire_Studiu = ?) AND ID_Pacient = (SELECT P.ID_Pacient FROM PACIENTI P WHERE P.CNP = ?)'''
                        , drug_frequency , drug_quantity , stop_date, study_title, cnp)
        # cursor.execute("UPDATE dbo.ISTORIC_STUDII_PACIENTI SET Frecventa_Administrare = ? , Cantitate_Administrare = ? WHERE ID_Studiu = (SELECT S.ID_Studiu FROM STUDII S WHERE S.Denumire_Studiu = ?) AND ID_Pacient = (SELECT P.ID_Pacient FROM PACIENTI P WHERE P.CNP = ?)", drug_frequency , drug_quantity , study_title, cnp)
        conn.commit()
        conn.close()

        return redirect('/')



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