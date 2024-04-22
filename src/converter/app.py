from flask import request, render_template, jsonify, Response

from converter.core import create_app, update_currencies, get_updated_at, convert_currencies, get_currencies_list

app, db = create_app()


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@app.route("/currencies", methods=["GET", "POST"])
def currencies():
    if request.method == "POST":
        updated_at = update_currencies(db)
        print(updated_at)
        return jsonify({"is_updated": True, "updated_at": updated_at})
    elif request.method == "GET":
        updated_at = get_updated_at(db)
        return str(updated_at)

@app.route("/currencies/list", methods=["GET"])
def currencies_list():
    if request.method == "GET":
        currencies = get_currencies_list(db)
        return jsonify(currencies)

@app.route("/convert", methods=["GET"])
def convert():    
    if request.method == "GET":
        try:
            res = convert_currencies(db, **request.args.to_dict())
            return str(res)
        except Exception as exc:
            return Response("Введены неправильные значения", status=400) 
        