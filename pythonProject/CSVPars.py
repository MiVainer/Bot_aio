# -------------------------#
# ---Program by MiVainer---#
import csv
import json

# Преобразование строки из json в словарь python
with open("baza/post.json", "r") as f:
    post_json = f.read()
    f.close()
post = json.loads(post_json)
a = (post["pack"])


#Наполнение словаря данными из csv базы
with open("baza/testbd.csv") as f:
    reader = csv.DictReader(f)
    k = 0
    for row in reader:
        a.append({"phone": f"{row['Phone']}",
                  "message": "Сударь, это тестовая рассылка",
                  "link": "https://ермак.shop/"})
    f.close()

baza = post

# красивая запись в json
with open("baza/baza.json", "w", encoding="utf-8") as f:
    for chunk in json.JSONEncoder(ensure_ascii=False, indent=4).iterencode(baza):
        f.write(chunk)
    f.close()


    #json.dump(baza, f, ensure_ascii=False)

    #print(json.dumps(baza, indent=4, sort_keys=True))


        #k += 1
        #print(f"Запись № {k}: {row['Phone']}")
    #print(f"Всего в базе {k} записей")'''


