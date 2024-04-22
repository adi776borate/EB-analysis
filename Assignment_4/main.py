from flask import Flask, render_template, request
import mysql.connector
import json


app = Flask(__name__)

# Configuring MySQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Borate65'
app.config['MYSQL_DB'] = 'dcc4'

#connecting to mysql
conn = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB']
)

cursor = conn.cursor()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET','POST'])
def search():
    if request.method == 'POST':
        bond_no = request.form['bond_number']
        cursor.execute("SELECT * FROM redemption WHERE `Bond Number` = %s", (bond_no,))
        results = cursor.fetchall()
        cursor.execute("SELECT * FROM purchase WHERE `Bond Number` = %s", (bond_no,))
        results2 = cursor.fetchall()
        return render_template('search.html',results=results, results2=results2)
    return render_template('search.html')

@app.route('/submit1', methods=['POST'])
def submit1():
    return search()

@app.route('/company',methods=['GET','POST'])
def company():
    if request.method == 'GET':
        cursor.execute("SELECT DISTINCT `Name of the Purchaser` FROM purchase")
        companies = [company[0] for company in cursor.fetchall()]
        return render_template('company.html',companies=companies)
    else:
        cursor.execute(
            """SELECT
                    SUBSTRING(`Date of Purchase`, -2) AS YEAR,
                    COUNT(`Bond Number`) AS No_Of_Bonds_Purchased,
                    SUM(CAST(REPLACE(Denominations, ',', '') AS UNSIGNED)) AS Total_Value_Purchased
                FROM 
                    purchase
                WHERE 
                    `Name of the Purchaser` = %s
                GROUP BY 
                    SUBSTRING(`Date of Purchase`, -2)""", (request.form["company"],)
                    )
        columns = [column[0] for column in cursor.description]
        bonds = [dict(zip(columns, row)) for row in cursor.fetchall()]
        Year=[]
        NoOfBonds=[]
        Total=[]
        for bond in bonds:
            a=bond['YEAR']
            Year.append(f'20{a}')
        for bond in bonds:
            a=bond['No_Of_Bonds_Purchased']
            NoOfBonds.append(a)
        for bond in bonds:
            a=bond['Total_Value_Purchased']
            Total.append(a)
        
        selected_company = request.form['company']
        return render_template('company.html', bonds=bonds, selected_company=selected_company, year=Year, n=NoOfBonds, t=Total)
    
@app.route('/submit2', methods=['POST'])
def submit2():
    return company()


@app.route('/party',methods=['GET','POST'])
def party():
    if request.method == 'GET':
        cursor.execute("SELECT DISTINCT `Name of the Political Party` FROM redemption")
        parties = [party[0] for party in cursor.fetchall()]
        return render_template('party.html',parties=parties)
    else:
        cursor.execute(
            """SELECT
                    SUBSTRING(`Date of Encashment`, -2) AS YEAR,
                    COUNT(`Bond Number`) AS No_Of_Bonds,
                    SUM(CAST(REPLACE(Denominations, ',', '') AS UNSIGNED)) AS Total_Value
                FROM 
                    redemption
                WHERE 
                    `Name of the Political Party` = %s
                GROUP BY 
                    SUBSTRING(`Date of Encashment`, -2)""", (request.form["party"],)
                    )
        columns = [column[0] for column in cursor.description]
        bonds = [dict(zip(columns, row)) for row in cursor.fetchall()]
        Year=[]
        NoOfBonds=[]
        Total=[]
        for bond in bonds:
            a=bond['YEAR']
            Year.append(f'20{a}')
        for bond in bonds:
            a=bond['No_Of_Bonds']
            NoOfBonds.append(a)
        for bond in bonds:
            a=bond['Total_Value']
            Total.append(a)
        
        selected_party = request.form['party']
        return render_template('party.html', bonds=bonds, selected_party=selected_party, year=Year, n=NoOfBonds, t=Total)
    
@app.route('/submit3', methods=['POST'])
def submit3():
    return party()

@app.route('/donation-receive',methods=['GET','POST'])
def receive():
    if request.method == 'GET':
        cursor.execute("SELECT DISTINCT `Name of the Political Party` FROM redemption")
        parties = [party[0] for party in cursor.fetchall()]
        return render_template('donation-receive.html',parties=parties)
    else:
        cursor.execute("""SELECT 
                                `Name of the Purchaser`, 
                                SUM(CAST(REPLACE(Denominations, ',', '') AS UNSIGNED)) AS Denominations
                            FROM 
                                purchase
                            WHERE 
                                `Bond Number` IN (
                                    SELECT `Bond Number` 
                                    FROM redemption 
                                    WHERE `Name of the Political Party` = %s
                                )
                            GROUP BY 
                                `Name of the Purchaser`""", (request.form["party1"],)
                        )
        columns = [column[0] for column in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]

        Purchaser=[]
        Denom=[]
        for res in result:
            a=res['Name of the Purchaser']
            Purchaser.append(a)
        for res in result:
            a=res['Denominations']
            Denom.append(a)
        total = sum(Denom)
        

        selected_party = request.form['party1']
        return render_template('donation-receive.html',result=result,selected_party=selected_party,Purchaser=Purchaser,Denom=Denom,total=total)        

@app.route('/submit4', methods=['POST'])
def submit4():
    return receive()

@app.route('/donation-given',methods=['GET','POST'])
def given():
    if request.method == 'GET':
        cursor.execute("SELECT DISTINCT `Name of the Purchaser` FROM purchase")
        companies = [company[0] for company in cursor.fetchall()]
        return render_template('donation-given.html',companies=companies)
    else:
        cursor.execute("""  SELECT 
                                `Name of the Political Party`, 
                                SUM(CAST(REPLACE(Denominations, ',', '') AS UNSIGNED)) AS Denominations
                            FROM 
                                redemption
                            WHERE 
                                `Bond Number` IN (
                                                    SELECT `Bond Number` 
                                                    FROM purchase
                                                    WHERE `Name of the Purchaser` = %s
                                                )
                            GROUP BY 
                                `Name of the Political Party`""", (request.form["company1"],)
                        )
        columns = [column[0] for column in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]

        Redeemer=[]
        Denom=[]
        for res in result:
            a=res['Name of the Political Party']
            Redeemer.append(a)
        for res in result:
            a=res['Denominations']
            Denom.append(a)
        total = sum(Denom)
        

        selected_company = request.form['company1']
        return render_template('donation-given.html',result=result,selected_company=selected_company,Redeemer=Redeemer,Denom=Denom,total=total)
        
@app.route('/submit5', methods=['POST'])
def submit5():
    return given()

@app.route('/total-donation',methods=['GET','POST'])
def total_donation():
    cursor.execute("""
                    SELECT 
                        `Name of the Political Party`,
                        SUM(CAST(REPLACE(Denominations, ',', '') AS UNSIGNED)) AS Total_Donation
                    FROM 
                        redemption
                    GROUP BY 
                        `Name of the Political Party`""")
    columns = [column[0] for column in cursor.description]
    result = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return render_template('total-donation.html',result=result)

@app.route('/date',methods=['GET','POST'])  
def date():
    cursor.execute("""
                    SELECT 
                    `Date of Encashment`,
                    COUNT(`Bond Number`) AS Counts
                    FROM redemption
                    GROUP BY
                    `Date of Encashment`"""
                   )
    columns = [column[0] for column in cursor.description]
    result = [dict(zip(columns, row)) for row in cursor.fetchall()]

    dates=[]
    counts=[]
    for res in result:
        a=res['Date of Encashment']
        dates.append(a)
    for res in result:
        a=res['Counts']
        counts.append(a)



    cursor.execute("""
                    SELECT 
                    `Date of Purchase`,
                    COUNT(`Bond Number`) AS Counts
                    FROM purchase
                    GROUP BY
                    `Date of Purchase`"""
                   )
    columns = [column[0] for column in cursor.description]
    result2 = [dict(zip(columns, row)) for row in cursor.fetchall()]

    dates2=[]
    counts2=[]
    for res in result2:
        a=res['Date of Purchase']
        dates2.append(a)
    for res in result2:
        a=res['Counts']
        counts2.append(a)
    return render_template('date.html',result=result, dates=dates, counts=counts, result2=result2, dates2=dates2, counts2=counts2)
    

if __name__ == '__main__':
    app.run(debug=True)