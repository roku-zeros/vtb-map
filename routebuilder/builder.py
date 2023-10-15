import pandas as pd
import json
import numpy as np
from copy import deepcopy

def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    r = 6371
    return c * r


def run():
    with open('../tools/db_json/offices.json', 'r', encoding='utf-8') as file:
        data = json.load(file)


    office_data = []


    for office in data["offices"]:
        salePointName = office["salePointName"]
        address = office["address"]
        status = office["status"]
        rko = office["rko"]
        officeType = office["officeType"]
        salePointFormat = office["salePointFormat"]
        suoAvailability = office["suoAvailability"]
        hasRamp = office["hasRamp"]
        latitude = office["latitude"]
        longitude = office["longitude"]
        metroStation = office["metroStation"]
        distance = office["distance"]
        kep = office["kep"]
        myBranch = office["myBranch"]

        # Создаем DataFrame для часов работы
        openHours = pd.DataFrame(office["openHours"])
        openHoursIndividual = pd.DataFrame(office["openHoursIndividual"])

        # Добавляем данные в список
        office_data.append({
            "salePointName": salePointName,
            "address": address,
            "status": status,
            "rko": rko,
            "officeType": officeType,
            "salePointFormat": salePointFormat,
            "suoAvailability": suoAvailability,
            "hasRamp": hasRamp,
            "latitude": latitude,
            "longitude": longitude,
            "metroStation": metroStation,
            "distance": distance,
            "kep": kep,
            "myBranch": myBranch,
            "openHours": openHours.to_dict(orient='records'),
            "openHoursIndividual": openHoursIndividual.to_dict(orient='records')
        })


    dataframe_offices = pd.DataFrame(office_data)



    with open("../tools/db_json/atms.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    address = []
    latitude = []
    longitude = []
    allDay = []
    services = []
    wheelchair = []
    serviceCapability = []
    serviceActivity = []
    nfcForBankCards = []


    for atm in data["atms"]:
        address.append(atm["address"])
        latitude.append(atm["latitude"])
        longitude.append(atm["longitude"])
        allDay.append(atm["allDay"])

        service = atm["services"]
        services.append(service)

        wheelchair_service = service.get("wheelchair", {})
        serviceCapability.append(wheelchair_service.get("serviceCapability", "UNKNOWN"))
        serviceActivity.append(wheelchair_service.get("serviceActivity", "UNKNOWN"))

        nfc_service = service.get("nfcForBankCards", {})
        nfcForBankCards.append(nfc_service.get("serviceCapability", "UNKNOWN"))


    atms_data = {
        "address": address,
        "latitude": latitude,
        "longitude": longitude,
        "allDay": allDay,
        "services": services,
        "wheelchair": serviceCapability,
        "serviceCapability": serviceCapability,
        "serviceActivity": serviceActivity,
        "nfcForBankCards": nfcForBankCards
    }

    atms_dataframe = pd.DataFrame(atms_data)




    # Given current location coordinates
    loc_latitude = 55.726492
    loc_longitude = 37.604295


    atms_dataframe['distance'] = atms_dataframe.apply(lambda row: haversine(loc_latitude, loc_longitude, row['latitude'], row['longitude']), axis=1)
    atms_dataframe['time'] = atms_dataframe.apply(lambda row: round(row['distance']*12), axis=1)



    atms_dataframe['distance'] = atms_dataframe.apply(lambda row: haversine(loc_latitude, loc_longitude, row['latitude'], row['longitude']), axis=1)
    atms_dataframe['time_feet']=atms_dataframe.apply(lambda row: round(row['distance']*12), axis=1)
    atms_dataframe['time_car']=atms_dataframe.apply(lambda row: round(row['distance']*4), axis=1)




    dataframe_offices['distance'] = atms_dataframe.apply(lambda row: haversine(loc_latitude, loc_longitude, row['latitude'], row['longitude']), axis=1)
    dataframe_offices['time_feet'] = atms_dataframe.apply(lambda row: round(row['distance'] * 12), axis=1).astype(int)
    dataframe_offices['time_car'] = atms_dataframe.apply(lambda row: round(row['distance'] * 4), axis=1).astype(int)

    dataframe_offices['Talons'] = np.random.randint(0, 41, size=len(dataframe_offices))

    #dataframe_offices['Total_Time_feet'] = dataframe_offices['time_feet'] + dataframe_offices['time_of_service']
    #dataframe_offices['Total_Time_car'] = dataframe_offices['time_car'] + dataframe_offices['time_of_service']

    dataframe_offices_sorted = ''
    atms_dataframe_sorted = ''

    json_data = atms_dataframe.to_json(orient="records", force_ascii=False)
    with open("locations_atms.json", "w", encoding="utf-8") as json_file:
        json_file.write(json_data)


    with open("locations_atms.json", "r", encoding="utf-8") as json_file:
        loaded_json_data = json.load(json_file)
    print(loaded_json_data)



    json_data_1 = dataframe_offices.to_json(orient="records", force_ascii=False)
    with open("locations_offices.json", "w", encoding="utf-8") as json_file_1:
        json_file_1.write(json_data)


    with open("locations_offices.json", "r", encoding="utf-8") as json_file_1:
        loaded_json_data_1 = json.load(json_file_1)
    print(loaded_json_data_1)





    #%%
