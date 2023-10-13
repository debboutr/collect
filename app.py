import sqlite3 as sql
from datetime import datetime as dt
from datetime import timedelta
from pathlib import Path

from flask import (Flask, flash, redirect, render_template, request, session,
                   url_for)

DATABASE = Path(__file__).parent / "data/database.db"

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    context = dict()
    now = dt.now()
    last_year = dt(now.year - 1, 12, 31, 4, 20, 47)
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
    loops = """select date, wage, bags, loops.group_id, name
                from loops 
                inner join groups
                on loops.group_id = groups.group_id"""
    cur.execute(loops)
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
            group = request.form["group"]
            pw = request.form["pw"]
            if pw == "47":
                with sql.connect(DATABASE) as con:
                    cur = con.cursor()
                    if num == "new":
                        cur.execute(
                            "INSERT INTO loops (date, wage,bags, group_id) VALUES (?,?,?,?)",
                            (day, wage, bags, group),
                        )
                    else:
                        cur.execute(
                            f"UPDATE loops SET date='{day}', wage={wage}, bags={bags}, group_id={group} WHERE id={num}",
                        )
                    con.commit()
                    context["msg"] = "Record successfully updated"
            else:
                context["msg"] = "PW incorrect"
        except:
            con.rollback()
            context["msg"] = "error in update operation"
    with sql.connect(DATABASE) as con:
        con.row_factory = sql.Row
        cur = con.cursor()
        if num == "new":
            cur.execute(f"select * from groups order by group_id desc limit 5")
            group = cur.fetchall()
            now = dt.now()
            row = dict(
                id="new",
                date=now.strftime("%Y-%m-%d"),
                wage=None,
                bags=None,
                owner_id=1,
            )
        else:
            find_group = """select id, date, wage, bags, loops.group_id, name
                            from loops
                            inner join groups
                            on loops.group_id = groups.group_id
                            where id='{}';"""
            cur.execute(find_group.format(num))
            row = cur.fetchone()
            cur.execute(f"select * from groups order by group_id desc limit 5")
            group = cur.fetchall()
            group = [g for g in group if g["group_id"] != row["group_id"]]
    context.update(
        {
            "row": row,
            "num": num,
            "group": group,
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


@app.route("/group/<num>", methods=["GET", "POST"])
def create_group(num):
    context = dict()
    if request.method == "POST":
        try:
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            pw = request.form["pw"]
            if pw == "47":
                with sql.connect(DATABASE) as con:
                    cur = con.cursor()
                    if num == "new":
                        out = cur.execute(
                            "INSERT INTO groups (name) VALUES (?)", (last_name,)
                        )
                        cur.execute(
                            "INSERT INTO people (first_name, last_name, notes, group_id) VALUES (?,?,?,?)",
                            (first_name, last_name, "", out.lastrowid),
                        )
                        con.commit()
                        return redirect(url_for("home"))
                    else:
                        cur.execute(
                            f"INSERT INTO people (first_name, last_name, notes, group_id) VALUES (?,?,?,?)",
                            (first_name, last_name, "", num),
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
        row = dict(
            id="new", date=now.strftime("%Y-%m-%d"), wage=None, bags=None, owner_id=1
        )
        people = {}
    else:
        with sql.connect(DATABASE) as con:
            con.row_factory = sql.Row
            cur = con.cursor()
            cur.execute(f"select * from groups where group_id={num}")
            row = cur.fetchone()
            cur.execute(f"select * from people where group_id={num}")
            people = cur.fetchall()
    context.update(
        {
            "num": num,
            "row": row,
            "people": people,
            "user": session,
        }
    )
    return render_template("group.html", **context)


@app.route("/person/<num>", methods=["GET", "POST"])
def person(num):
    context = dict()
    if request.method == "POST":
        try:
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            notes = request.form["notes"].strip()
            lat = request.form["lat"]
            lon = request.form["lon"]
            pw = request.form["pw"]
            if pw == "47":
                with sql.connect(DATABASE) as con:
                    cur = con.cursor()
                    cur.execute(
                        f"UPDATE people SET last_name='{last_name}', first_name='{first_name}', notes='{notes}', lat={lat}, lon={lon} WHERE id={num}",
                    )
                    con.commit()
                    context["msg"] = "Record successfully updated"
            else:
                context["msg"] = "PW incorrect"
        except:
            con.rollback()
            context["msg"] = "error in update operation"
    con = sql.connect(DATABASE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute(f"select * from people where id={num}")
    row = cur.fetchone()
    con.close()
    context.update(
        {
            "num": num,
            "row": row,
            "user": session,
        }
    )
    return render_template("person.html", **context)


if __name__ == "__main__":
    app.run()
