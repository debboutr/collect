import sqlite3 as sql
from datetime import datetime as dt
from datetime import timedelta
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, session, url_for

DATABASE = Path(__file__).parent / "data/database.db"

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    context = dict()
    now = dt.now()
    last_year = dt(now.year-1, 12, 31, 4, 20, 47)
    total_days = (now - last_year).days
    con = sql.connect(DATABASE)
    cursor = con.cursor()
    find_wages = """select sum(wage), sum(bags)
                    from loops
                    where
                        substr(date, 0, 5) = '{}';"""
    cursor.execute(find_wages.format(now.year))
    tot_wages, tot_bags = cursor.fetchone()
    tot_wages = tot_wages if tot_wages else 0
    tot_bags = tot_bags if tot_bags else 0.47
    avg_wage = round(tot_wages / tot_bags, 2)

    find_work_days = """select count(*)
                        from loops
                        where bags > 0 and
                        substr(date, 0, 5) = '{}';"""
    cursor.execute(find_work_days.format(now.year))
    work_days = cursor.fetchone()[0]

    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from loops")
    rows = cur.fetchall()[-5:]
    context.update(
        {
            "rows": rows,
            "tot_bags": tot_bags,
            "tot_wages": tot_wages,
            "avg_wage": avg_wage,
            "user": session,
            "total_days": total_days,
            "work_days": work_days,
            "year": dt.now().year,
        }
    )
    con.close()
    return render_template("home.html", **context)


@app.route("/edit/<num>", methods=["GET", "POST"])
def edit(num):
    context = dict()
    if request.method == "POST":
        try:
            day = request.form["day"]
            wage = request.form["wage"]
            bags = request.form["bags"]
            pw = request.form["pw"]
            if pw == "47":
                with sql.connect(DATABASE) as con:
                    cur = con.cursor()
                    if num == "new":
                        cur.execute(
                            "INSERT INTO loops (date, wage,bags) VALUES (?,?,?)",
                            (day, wage, bags),
                        )
                    else:
                        cur.execute(
                            f"UPDATE loops SET date='{day}', wage={wage}, bags={bags} WHERE id={num}",
                        )
                    con.commit()
                    context["msg"] = "Record successfully updated"
            else:
                context["msg"] = "PW incorrect"
        except:
            con.rollback()
            context["msg"] = "error in update operation"
    if num == "new":
        now = dt.now()
        row = dict(id="new", date=now.strftime("%Y-%m-%d"), wage=None, bags=None, owner_id=1)
    else:
        con = sql.connect(DATABASE)
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute(f"select * from loops where id={num}")
        row = cur.fetchone()
        con.close()
    context.update(
        {
            "row": row,
            "user": session,
        }
    )
    return render_template("edit.html", **context)


@app.route("/delete/<num>", methods=["POST"])
def delete(num):
    if request.method == "POST":
        try:
            with sql.connect(DATABASE) as con:
                cur = con.cursor()
                cur.execute(
                    f"DELETE from loops WHERE id={num}",
                )
                con.commit()
        except:
            con.rollback()
    return redirect(url_for("total"))


@app.route("/months", methods=["GET"])
def months():
    context = dict()
    con = sql.connect(DATABASE)
    cursor = con.cursor()
    con.row_factory = sql.Row
    sum_month = """select
                        sum(wage) as wages,
                        sum(bags) as bags,
                        count(*) as days,
                        substr(date, 0, 5) Year,
                        substr(date, 6, 2) as Month
                    from
                        loops
                    group by
                        Year,
                        Month
                    order by
                        Year desc;"""
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
    #breakpoint()
    context.update({"rows": ans, "months": months, "user": session})
    con.close()
    return render_template("months.html", **context)


@app.route("/month/<year>/<month>", methods=["GET"])
def month_detail(year, month):
    con = sql.connect(DATABASE)
    con.row_factory = sql.Row
    cur = con.cursor()
    month_data = """select * from loops
                    where
                        substr(date, 0, 5) = '{}'
                    and
                        substr(date, 6, 2) = '{}';"""
    cur.execute(month_data.format(year, month))
    rows = cur.fetchall()
    context = {"rows": rows}
    con.close()
    return render_template("total.html", **context)


@app.route("/total", methods=["GET"])
def total():
    con = sql.connect(DATABASE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from loops order by date desc")
    rows = cur.fetchall()
    context = {"rows": rows}
    con.close()
    return render_template("total.html", **context)


@app.route("/group", methods=["GET", "POST"])
def create_group():
    con = sql.connect(DATABASE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from loops order by date desc")
    rows = cur.fetchall()
    context = {"rows": rows}
    con.close()
    return render_template("total.html", **context)


if __name__ == "__main__":
    app.run()
