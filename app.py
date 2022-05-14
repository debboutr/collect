import os
from pathlib import Path
from flask import Flask, render_template, request, session, flash
import sqlite3 as sql
from datetime import datetime as dt

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    HOME = str(Path(os.getcwd()).parent / "data")
    context = dict()
    last_year = dt(2021, 12, 31, 4, 20, 47)
    total_days = (dt.now() - last_year).days
    if request.method == "POST":
        date = dt.now().strftime("%m-%d")
        try:
            day = request.form["day"]
            wage = request.form["wage"]
            bags = request.form["bags"]
            pw = request.form["pw"]
            date = date if day == "" else day
            if pw == "47":
                with sql.connect(f"{HOME}/database.db") as con:
                    cur = con.cursor()
                    cur.execute(
                        "INSERT INTO loops (date, wage,bags) VALUES (?,?,?)",
                        (date, wage, bags),
                    )
                    con.commit()
                    context["msg"] = "Record successfully added"
            else:
                context["msg"] = "PW incorrect"
        except:
            con.rollback()
            context["msg"] = "error in insert operation"
    con = sql.connect(f"{HOME}/database.db")
    cursor = con.cursor()

    find_wages = "select sum(wage), sum(bags) from loops"
    cursor.execute(find_wages)
    tot_wages, tot_bags = cursor.fetchone()

    find_work_days = "select count(*) from loops where bags > 0"
    cursor.execute(find_work_days)
    work_days = cursor.fetchone()[0]

    avg_wage = round(tot_wages / tot_bags, 2)

    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from loops")
    rows = cur.fetchall()[-5:]
    context.update(
        {
            "rows": rows,
            "tot_bags": tot_bags,
            "tot_wages": f"${tot_wages:,}",
            "avg_wage": avg_wage,
            "user": session,
            "total_days": total_days,
            "work_days": work_days,
        }
    )
    con.close()
    return render_template("home.html", **context)


@app.route("/months", methods=["GET"])
def months():
    HOME = str(Path(os.getcwd()).parent / "data")
    context = dict()
    con = sql.connect(f"{HOME}/database.db")
    cursor = con.cursor()

    con.row_factory = sql.Row
    sum_month = """select
                        sum(wage) as wages,
                        sum(bags) as bags,
                        count(*) as days,
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
    context.update({"rows": ans, "months": months, "user": session})

    con.close()
    return render_template("months.html", **context)


@app.route("/total", methods=["GET", "POST"])
def total():
    HOME = str(Path(os.getcwd()).parent / "data")
    con = sql.connect(f"{HOME}/database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from loops")
    rows = cur.fetchall()
    context = {"rows": rows}
    con.close()
    return render_template("total.html", **context)


if __name__ == "__main__":
    app.run()
