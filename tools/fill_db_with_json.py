from db.models import *
import json


atms_file = "db_json/atms.json"
offices_file = "db_json/offices.json"

category = {
    "Кредит": ["Кредит наличиными", "Экспресс-кредит", "Рефинансирование", "Кредит под залог недвижимости"],
    "Карты": ["Дебетовые карты", "Кредитные карты", "Пенсионные карты", "Карты жителя", "Социальные карты"],
    "Инвестиции": ["Счет в плюсе", "ОФЗ", "Облигации", "Акции", "ВТБ Мои Инвестиции", "ИИС"],
    "Ипотека": ["Для семей с детьми от 4,6%", "Льготная имотека для всех от 7,6%",
                  "Ипотека на вторичное жилье от 14%", "Ипотека на новостройки от 14%",
                  "Рефинансирование ипотеки от 5%", "Ипотечный калькулятор"],
    "Вклады и счета": ["Накопительный счет Сейф до 13%", "Накопительный счет Копилка до 11%",
                         "ВТБ-Вклад в рублях до 13%", "Вклад Новое время до 11,5%",
                         "Вклад Выгодное начало до 11,7%", "ВТБ-Вклад в юанях до 3,35%"],
    "Автокредит": ["Госпрограмма 2023", "Автокредит наличными", "Автокредит в автосалоне", "Авто по подписке",
                     "Купить автомобиль", "Выкуп авто"],

}
org_category = {
    "Кредит": ["Экспресс-кредит онлайн", "Оборотный кредит", "Финансирование капитальных затрат","Рефинансирование "],
    "Бизнес-карты": ["Виртуальная карта", "Универсальная карта","Премиальная карта","Таможенная карта"],
    "Расчетный счет": ["Расчетный счет для ИП", "Расчетный счет для ООО","Подобрать пакет РКО","Специальные счета","Банковское сопровождение","Открыть счет онлайн"],
    "Регистрация бизнеса": ["Регистрация ИП", "Регистрация в качестве самозанятого","Регистрация ООО","Открыть счет для ИП","Открыть счет для ООО"],
    "Сервисы для бизнеса": ["Электронная подпись", "Сервис внесения изменений в ЕГРИП/ЕГРЮЛ","Бухгалтерия на аутсорсе для ИП и ООО","Расчеты с самозанятыми","Онлайн-медици","ВТБ-Вклад в юанях до 3,35%"],
}
atm_categoty = {
    "Переводы": ["Переводы денег по номеру телефона или СПБ", "Пополнение карт и счетов","Настройка автоплатежей","Оплата услуг по карте"],
    "Кредиты": ["Оставить заявку на кредит", "Погашение кредитов"],
    "Снятие наличных": ["Снятие наличных по карте", "Снятие наличных по QR-коду"],
    "Прочее": ["Измненение ПИН-кода", "Подключение и оплата СМС от ВТБ","Получение логина и пароля для ВТБ Онлайн"],

}


@db_session
def get_categories():
    categories = []
    for k in category:
        sub_categories = []
        for sk in category[k]:
            sub_categories.append(SubCategory(name=sk))
        categories.append(Category(name=k, sub_categories=sub_categories))
    return categories

@db_session
def get_org_categories():
    org_categories = []
    for k in category:
        sub_org_categories = []
        for sk in category[k]:
            sub_org_categories.append(SubCategory(name=sk))
        org_categories.append(Category(name=k, sub_categories=sub_org_categories))
    return org_categories

@db_session
def get_atm_categories():
    atm_categories = []
    for k in category:
        sub_atm_categories = []
        for sk in category[k]:
            sub_atm_categories.append(AtmSubCategory(name=sk))
        atm_categories.append(AtmCategory(name=k, atm_sub_categories=sub_atm_categories))
    return atm_categories


def read_to_dict(filename):
    with open(filename, 'r') as f:
        return json.load(f)


@db_session
def save_atms_dict_to_db(atms):
    for atm in atms["atms"]:
        # Get atm info
        address = atm["address"]
        latitude = float(atm["latitude"])
        longitude = float(atm["longitude"])
        all_day = bool(atm["allDay"])

        support_rubles = True if atm["services"]["supportsRub"]["serviceCapability"] == "SUPPORTED" else False
        support_dollar = True if atm["services"]["supportsUsd"]["serviceCapability"] == "SUPPORTED" else False
        support_euro = True if atm["services"]["supportsEur"]["serviceCapability"] == "SUPPORTED" else False
        # Save info to db
        atm = Atm(
            latitude=latitude,
            longitude=longitude,
            atm_categories=get_atm_categories(),
            atm_info=AtmInfo(
                address=address,
                is_always=all_day,
                support_rubles=support_rubles,
                support_dollar=support_dollar,
                support_euro=support_euro,
            )
        )


@db_session
def save_office_dict_to_db(offices):
    for office in offices:
        # Getting main info
        name = office["salePointName"]
        address = office["address"]
        latitude = float(office["latitude"])
        longitude = float(office["longitude"])
        suo = True if office["suoAvailability"] == "Y" else False
        rko = True if (not office["rko"] is None) and "есть" in office["rko"] else False
        ramp = True if office["hasRamp"] == "Y" else False
        metro = office["metroStation"] if office["metroStation"] else ""
        # Getting work time
        work_times = []
        for time in office["openHoursIndividual"]:
            open, close = "выходной", "выходной"
            day = time["days"]
            if time["hours"] is None:
                open, close = "выходной", "выходной"
            elif time["hours"].lower() != "выходной":
                open, close = time["hours"].split("-")
            work_times.append(WorkHours(
                open=open,
                close=close,
                day=day
            ))
        work_times_org = []
        for time_org in office["openHours"]:
            day = time_org["days"]
            open, close = "выходной", "выходной"
            if time_org["hours"] is None:
                open, close = "выходной", "выходной"
            elif time_org["hours"] != "выходной":
                open, close = time_org["hours"].split("-")
            work_times_org.append(WorkHours(
                open=open,
                close=close,
                day=day
            ))
        # Save info to db
        office = Office(
            latitude=latitude,
            longitude=longitude,
            work_hours=work_times,
            work_hours_org=work_times_org,
            info=Info(
                name=name,
                address=address,
                metro=metro,
                ramp=ramp,
                rko=rko,
                suo=suo
            )
        )


# Save atms from json file to DB
save_atms_dict_to_db(read_to_dict(atms_file))
# Save office from json to file
save_office_dict_to_db(read_to_dict(offices_file))
