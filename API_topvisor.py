import json
import time

import pandas as pd
import requests


def get_poritions_altailbroiler(*args, **kwargs):
    project = "5027269"
    headers = {
        'Content-Type': 'application/json',
        'User-Id': '1160',
        'Authorization': ''  # Вставить ключ из кабинета топвизора
    }

    date_report = "2023-05-31"  # Поставить дату съёма позиций

    region_indexes = {
        1: "Yandex — Москва",
        2: "Google — Москва",
        106: "Yandex — Барнаул",
        168: "Google — Барнаул",
        111: "Yandex — Новокузнецк",
        171: "Google — Новокузнецк",
        89: "Yandex — Кемерово",
        153: "Google — Кемерово",
        793: "Yandex — Бийск",
        993: "Google — Бийск",
        90: "Yandex — Новосибирск",
        154: "Google — Новосибирск"
    }

    queries = []
    responses = []

    for region in region_indexes.keys():
        query = {
            "project_id": project,
            "fields": [
                "id",
                "name",
                f"position:{date_report}:{project}:{region}",
                "group_name"
            ]
        }
        queries.append(json.dumps(query))

    for ind, query in enumerate(queries):
        response = requests.get('https://api.topvisor.com/v2/json/get/keywords_2/keywords/',
                                headers=headers,
                                data=query).text
        res = json.loads(response)
        responses.append(res['result'])
        if ind % 3 == 0:
            time.sleep(0.2)

    responses_data = responses[0] + sum(responses[1:], [])

    results = []

    for item in responses[0]:
        tup = tuple(responses[0][0])
        name = tup[1]
        groupName = tup[2]
        position = tup[3]
        results.append([item[name], item[groupName], item.get(position, "N")])

    responses.pop(0)

    for res in responses:
        tup = tuple(res[0])
        position = tup[3]
        for ind, item in enumerate(res):
            value = item.get(position)
            results[ind].append(value if value is not None else "N")

    for row in results:
        for i, value in enumerate(row):
            if value == "--":
                row[i] = "100"

    columns = ['Запрос', 'Группа'] + list(region_indexes.values())
    df = pd.DataFrame(results, columns=columns)
    df = df[df['Группа'] != "Брендовые запросы без посадочной"]
    df = df.sort_values(by='Группа')

    df.to_excel('output_Topvisor.xlsx', index=False)
    print("Файл output_Topvisor.xlsx сохранён")


get_poritions_altailbroiler()
