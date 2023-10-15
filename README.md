<h1 align="center">Cервис для подбора оптимального отделения банка</h1>

Данный проект создан для хакатона [**MORE.Tech VTB 2023**](https://moretech.vtb.ru/)

Приложение с алгоритмом, учитывающим загрузку отделений, которая определяется благодаря количеству зарегистрированных талонов на услуги за час. Для, пользователя при построении маршрута, регистрируется электронный талон. Есть AI-бот, который помогает подобрать услугу/решить проблему клиента.


## Команда:

Бикчуров Карим 

Згонников Роберт

Юркин Данила 

Аванесян Александр 

Быков Михаил


---
## How to launch

Для запуска понадобится Python3 и uvicorn.

Для скачивания uvicorn:
linux/macos: pip3 install uvicorn
windows: pip install uvicorn

Далее нужно скачать все нужные библиотеки и зависимости:
linux/macos: pip3 install -r requirements.txt
windows: pip install -r requirements.txt

Чтобы заполнить базу стартовыми данными, нужно зайти в директорию tools и вызвать:
linux/macos: python3 fill_db_with_json.py
windows: python fill_db_with_json.py


[Alt text](./image_file_name.png)
