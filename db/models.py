from pony.orm import *


db = Database()


class Atm(db.Entity):
    id = PrimaryKey(int, auto=True)
    latitude = Required(float)
    longitude = Required(float)
    atm_categories = Set('AtmCategory')
    atm_info = Required('AtmInfo')


class Office(db.Entity):
    id = PrimaryKey(int, auto=True)
    latitude = Optional(float)
    longitude = Optional(float)
    work_hours = Set('WorkHours', reverse='office')
    categories = Set('Category')
    info = Required('Info')
    work_hours_org = Set('WorkHours', reverse='office_org')


class WorkHours(db.Entity):
    id = PrimaryKey(int, auto=True)
    open = Optional(str)
    close = Optional(str)
    day = Optional(str)
    is_org_time = Optional(float)
    office = Optional(Office, reverse='work_hours')
    office_org = Optional(Office, reverse='work_hours_org')


class Info(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    address = Optional(str)
    metro = Optional(str)
    ramp = Required(bool)
    rko = Required(bool)
    suo = Optional(bool)
    office = Optional(Office)


class Category(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    is_org = Optional(bool)
    sub_categories = Set('SubCategory')
    offices = Set(Office)


class SubCategory(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    category = Required(Category)


class AtmInfo(db.Entity):
    id = PrimaryKey(int, auto=True)
    atm = Optional(Atm)
    address = Optional(str)
    is_always = Optional(bool)
    support_rubles = Required(bool)
    support_dollar = Required(bool)
    support_euro = Required(bool)


class AtmCategory(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    atm_sub_categories = Set('AtmSubCategory')
    atms = Set(Atm)


class AtmSubCategory(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    atm_category = Optional(AtmCategory)


db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)
