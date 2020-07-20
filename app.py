from flask import Flask, render_template, request
import sqlite3


app = Flask(__name__)


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


@app.route("/viewfoodinfos")
def viewFoodInfo():
    con = sqlite3.connect("usda.sql3")
    con.text_factory = lambda b: b.decode(errors='ignore')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select id, short_desc, long_desc, manufac_name, sci_name from food")
    rows = cur.fetchall()
    return render_template("viewfoodinfo.html", rows=rows)


@app.route("/viewfoodinfos/<string:id>", methods=["GET"])
def viewSelectedFoodInfo(id):
    con = sqlite3.connect("usda.sql3")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("""select fg.name
    ,short_desc
    ,long_desc
    ,manufac_name
    ,sci_name from food f
    inner join food_group fg
    on f.food_group_id = fg.id
    where f.id = ?""", [id])

    rows = cur.fetchall();
    return render_template("selectedfoodinfo.html", rows=rows, id=id)


@app.route("/updatefoodinfo/<string:id>", methods=["POST", "GET"])
def enterDetails(id):
    if request.method == "GET":
        con = sqlite3.connect("usda.sql3")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT name from food_group")
        rows = cur.fetchall()
        sends = [each["name"] for each in rows]
    return render_template("updatefoodinfo.html", sends=sends, id=id)


@app.route("/updatedetails/<string:id>", methods=["POST", "GET"])
def updatedetails(id):
    if request.method == "POST":
        try:
            foodGroupName = str(request.form.get("sends"))
            shortDesc = request.form["short_desc"]
            longDesc = request.form["long_desc"]
            manifacName = request.form["manufac_name"]
            sciName = request.form["sci_name"]

            with sqlite3.connect("usda.sql3") as con:
                cur = con.cursor()
                cur.execute("SELECT id from food_group WHERE name = ?", [foodGroupName])
                foodGroupIds = cur.fetchall()
                foodGroupId = foodGroupIds[0]


            with sqlite3.connect("usda.sql3") as con:
                con.row_factory = sqlite3.Row
                cur = con.cursor()
                sqlQuery = """UPDATE food
                    SET food_group_id = "{}"
                    ,short_desc = "{}"
                    ,long_desc = "{}"
                    ,manufac_name = "{}"
                    ,sci_name = "{}"
                    WHERE id = {}""".format(int(foodGroupId[0]), str(shortDesc), str(longDesc), str(manifacName),
                                            str(sciName), id)
                cur.execute(sqlQuery)
                con.commit()



        except Exception as e:
            con.rollback()

        finally:

            return render_template("/index.html")
            con.close()

@app.route("/viewfoodnutritioninfos", methods=["GET"])
def viewFoodNamesForNutritions():
    con = sqlite3.connect("usda.sql3")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select id,short_desc from food")
    rows = cur.fetchall()
    return render_template("viewshortnamelinks.html", rows=rows)


@app.route("/viewfoodnutritioninfos/<string:id>",methods=["GET"])
def viewSelectedFoodNutrions(id):

    con = sqlite3.connect("usda.sql3")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("""select fg.name
    ,short_desc
    ,long_desc
    ,manufac_name
    ,sci_name from food f
    inner join food_group fg
    on f.food_group_id = fg.id
    where f.id = ?""", [id])
    rows = cur.fetchall()


    cur.execute("""select DISTINCT f.short_desc
    ,w.description
    ,w.gm_weight
    from food f
    inner join nutrition n
    on f.id = n.food_id
    inner join weight w
    on n.food_id = w.food_id
    where f.id = ?""", [id])
    rows2 = cur.fetchall()


    cur.execute("""select f.id
    ,f.short_desc
    ,nt.name
    ,n.amount
    ,nt.units
    from food f
    inner join nutrition n
    on f.id = n.food_id
    inner join nutrient nt
    on n.nutrient_id = nt.id
    where f.id = ?""",[id])

    rows3 = cur.fetchall()
    return render_template("selectedfoodnutrientinfos.html",rows = rows, rows2 = rows2, rows3 = rows3, id = id)


if __name__ == '__main__':
    app.run()