from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pony.orm import *
from db.models import *
from extra.extra import *
from typing import Dict, Any
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def root():
    """
        Привет ВТБ!
    """
    return {"Hello": "VTB!"}


@app.get("/offices")
async def read_offices():
    """
        Список всех офисов
    """
    response = {}
    with db_session:
        offices = list(Office.select())
        for o in offices:
            response[o.id] = {
                "latitude": o.latitude,
                "longitude": o.longitude
            }
    return response


@app.get("/atms")
async def read_atms():
    """
        Список всех банкоматов
    """
    response = {}
    with db_session:
        atms = list(Atm.select())
        for a in atms:
            response[a.id] = {
                "latitude": a.latitude,
                "longitude": a.longitude
            }
    return response


@app.get("/closest_offices/{latitude}&{longitude}")
async def read_closest_offices(latitude: float, longitude: float):
    """
    Возвращает ближайшие отделения в радиусе 1км и 3 км
    :param latitude:
    :param longitude:
    :return:
    """
    response = {}
    with db_session:
        # Get offices in 1 km radius
        rect1, rect2 = count_near_1(latitude, longitude), count_near_3(latitude, longitude)
        offices = list(Office.select().where(min(rect1[0], rect1[2]) < latitude < max(rect1[0], rect1[2]),
                                             min(rect2[1], rect2[3]) < longitude < max(rect2[1], rect2[3])))
        for o in offices:
            response["1km"]: {
                o.id: {
                    "latitude": o.latitude,
                    "longitude": o.longitude
                }
            }
        # Get offices in 3 km radius
        rect11, rect22 = count_near_3(latitude, longitude), count_near_3(latitude, longitude)
        offices = list(Office.select().where(min(rect11[0], rect11[2]) < latitude < max(rect11[0], rect11[2]),
                                             min(rect22[1], rect22[3]) < longitude < max(rect22[1], rect22[3])))
        for o in offices:
            response["3km"]: {
                o.id: {
                    "latitude": o.latitude,
                    "longitude": o.longitude
                }
            }
    return {"offices_near": response}


@app.get("/closest_atms/{latitude}&{longitude}")
async def read_closest_atms(latitude: float, longitude: float):
    """
    Возвращает ближайшие банкоматы в радиусе 1км и 3 км
    :param latitude:
    :param longitude:
    :return:
    """
    response = {}
    with db_session:
        # Get offices in 1 km radius
        rect1, rect2 = count_near_1(latitude, longitude), count_near_3(latitude, longitude)
        atms = list(Atm.select().where(min(rect1[0], rect1[2]) < latitude < max(rect1[0], rect1[2]),
                                       min(rect2[1], rect2[3]) < longitude < max(rect2[1], rect2[3])))
        for a in atms:
            response["1km"]: {
                a.id: {
                    "latitude": a.latitude,
                    "longitude": a.longitude
                }
            }
        # Get offices in 3 km radius
        rect11, rect22 = count_near_3(latitude, longitude), count_near_3(latitude, longitude)
        atms = list(Atm.select().where(min(rect11[0], rect11[2]) < latitude < max(rect11[0], rect11[2]),
                                       min(rect22[1], rect22[3]) < longitude < max(rect22[1], rect22[3])))
        for a in atms:
            response["3km"]: {
                a.id: {
                    "latitude": a.latitude,
                    "longitude": a.longitude
                }
            }
    return {"offices_near": response}


@app.get("/office_info/id")
async def read_office_info(id: int):
    """
    Отдает информацию по индексу об отделении
    :param id:
    :return:
    """
    with db_session:
        # atm by ind
        office = Office.select().where(id=id).first
    return {"office_info": office}


@app.get("/atm_info/id")
async def read_atm_info(id: int):
    """
    Отдает информацию по индексу о банкомате
    :param id:
    :return:
    """
    response = {}
    with db_session:
        # atm by ind
        atms = Atm.select().where(id=id).first
    return {"atms_info": atms}


@app.get("/chatbot/req")
async def chatbot(req: str):
    """
    Отправляет запрос в бот, и возвращает варианты ответа
    :param req:
    :return:
    """
    answer = ""
    category = Category.select().where(name=answer).first
    return {"answers": category.sub_categories}


@app.get("/bestpoint/{latitude}&{longitude}")
async def find_best_point(latitude: float, longitude: float):
    """
        Накходит опмтиальное отделение для пользщователя
    """
    return {"point": ""}


@app.post("/office/")
async def create_office(office: Any):
    """
    Метод создает отделение банка
        :param office:
        :return:
    """
    try:
        with db_session:
            of = Office
            commit()
        return {"status": "Department created"}
    except:
        print("error")
    return {"status": "Error"}


@app.post("/atm/")
async def create_office(atm: Any):
    """
    Метод создает абнкомат
    :param atm:
    :return:
    """
    try:
        with db_session:
            of = Office
            commit()
        return {"status": "Department created"}
    except:
        print("error")
    return {"status": "Error"}
