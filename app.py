from flask import Flask, render_template, request
import sqlite3


app = Flask(__name__)

con = sqlite3.connect("usda.sql3")
print("Database opened successfully")




@app.route("/")
def index():
    return render_template("index.html")

@app.route("/view")
def view():
    con = sqlite3.connect("usda.sql3")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select name as FoodGroupName,id from food_group")
    rows = cur.fetchall()
    return render_template("view.html", rows=rows)



@app.route("/view/<string:id>",methods=["GET"])
def foodGroupInfo(id):
    con = sqlite3.connect("usda.sql3")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("""select f.short_desc as ShortDesc
    ,f.nitrogen_factor as Nitrogen
	,f.protein_factor as Protein
	,f.fat_factor as Fat
    ,f.calorie_factor as Calorie
	,fg.name
    from food f
    inner join food_group fg
    on f.food_group_id = fg.id
    where fg.id = ?""",[id])

    rows = cur.fetchall();
    return render_template("foodgroupinfo.html",rows = rows)

if __name__ == '__main__':
    app.run()
