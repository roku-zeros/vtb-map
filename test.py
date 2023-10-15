from pony.orm import *
from db.models import *

with db_session:
    offices = list(select(o for o in Office))
print(offices)