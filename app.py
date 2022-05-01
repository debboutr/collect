import os
from pathlib import Path
from flask import Flask, render_template, request, session, flash
import sqlite3 as sql
from datetime import datetime as dt

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    HOME = str(Path(os.getcwd()).parent / "data")
    context = dict()
    if request.method == 'POST':
        date = dt.now().strftime("%m-%d")
        try:
            wage = request.form['wage']
            bags = request.form['bags']
            pw = request.form['pw']
            if pw == "47":
               
            # import pdb
            # pdb.set_trace()
                with sql.connect(f"{HOME}/database.db") as con:
                    cur = con.cursor()
                    cur.execute("INSERT INTO loops (date, wage,bags) VALUES (?,?,?)", (date,wage,bags))
                    con.commit()
                    context["msg"] = "Record successfully added"
            else:
                context["msg"] = "PW incorrect"
        except:
            con.rollback()
            context["msg"] = "error in insert operation"
    con = sql.connect(f"{HOME}/database.db")
    cursor = con.cursor()

    find_all_wages = "select sum(wage) from loops"
    cursor.execute(find_all_wages)
    tot_wages = cursor.fetchone()[0]

    find_all_bags = "select sum(bags) from loops"
    cursor.execute(find_all_bags)
    tot_bags = cursor.fetchone()[0]

    avg_wage=round((tot_wages/tot_bags), 2)

    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from loops")
    rows = cur.fetchall()[-5:];
    context.update({
        "rows":rows,
        "tot_bags":tot_bags,
        "tot_wages":f"${tot_wages:,}",
        "avg_wage":avg_wage,
        "user": session
        })
    # print(context)

    con.close()
    return render_template("home.html", **context)

@app.route('/months', methods=['GET'])
def months():
    HOME = str(Path(os.getcwd()).parent / "data")
    context = dict()
    con = sql.connect(f"{HOME}/database.db")
    cursor = con.cursor()


    con.row_factory = sql.Row
    sum_month = """select 
                        sum(wage) as wages, 
                        sum(bags) as bags,
                        substr(date, 1, 2) as Month 
                    from 
                        loops 
                    group by 
                        substr(date, 1, 2)"""
    cur = con.cursor()
    cur.execute(sum_month)
    ans = cur.fetchall()
    months = {
            "01": "January",
            "02": "February",
            "03": "March",
            "04": "April",
            "05": "May",
            "06": "June",
            "07": "July",
            "08": "August",
            "09": "September",
            "10": "October",
            "11": "November",
            "12": "December",
            }
    context.update({
        "rows":ans,
        "months": months,
        "user": session
        })

    con.close()
    return render_template("months.html", **context)


if __name__ == '__main__':
    app.run(debug=True)
