import os
from datetime import datetime

from flask import Flask
import requests
from loguru import logger

from converter.db import DB

CURRENCIES_API = "https://www.cbr-xml-daily.ru/latest.js"


def create_app() -> Flask:
    template_dir = os.path.abspath(os.path.join("src", "converter", "templates"))
    app = Flask(__name__, template_folder=template_dir)

    try: 
        db = DB()
        db.create_db()
    except Exception as exc: 
        logger.error(exc)

    return app, db


def get_rates(url: str = CURRENCIES_API) -> dict:
    resp = requests.get(url)
    data = resp.json()
    rates = data.get("rates", {})    
    return rates


def update_currencies(db: DB) -> datetime:
    rates = get_rates()
    updated_at = datetime.now()
    db.update_all_currencies(rates=rates, updated_at=updated_at)
    return updated_at


def get_updated_at(db: DB) -> datetime:
    updated_at = db.get_last_updated_at()
    return updated_at


def get_currencies_list(db: DB) -> list: 
    currencies = db.get_currencies_list()
    return currencies

def convert_currencies(db: DB, from_name: str, to_name: str, val: float) -> float:
    curs = [from_name, to_name]
    
    val = float(val)

    rates = db.get_rates(curs)

    if from_name not in rates or to_name not in rates:
        raise Exception("Такой валюты нет")
    
    to_cur = round(val / rates[from_name] / (1.0 / rates[to_name]), 4)
    return to_cur