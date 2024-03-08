# -------------------------#
# ---Program by MiVainer---#
import csv
import json
import re

# Преобразование строки из json в словарь python
with open("baza/post.json", "r") as f:
    post_json = f.read()

post = json.loads(post_json)
a = post["pack"]
print(a)


#Наполнение словаря данными из csv базы
with open("baza/testbd.csv") as f:
    reader = csv.DictReader(f, delimiter=';')
    k = 0
    for row in reader:
        k = k+1
        #stre = int(filter(str.isdigit, row['Phone']))
        stre = re.sub('[^0-9]', '', row['Phone'])
        a.append({"phone": f"{stre}",
                  "message": "Сударь, это тестовая рассылка",
                  "link": "https://ермак.shop/"})
        print(f"Запись № {k}: {row['Phone']}")
    print(f"Всего в базе {k} записей")

baza = post

# красивая запись в json
with open("baza/baza.json", "w", encoding="utf-8") as f:
    for chunk in json.JSONEncoder(ensure_ascii=False, indent=4).iterencode(baza):
        f.write(chunk)


    #json.dump(baza, f, ensure_ascii=False)

    #print(json.dumps(baza, indent=4, sort_keys=True))


        #k += 1


