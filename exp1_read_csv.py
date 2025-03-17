# import csv
#
# with open("./cafe-data.csv", newline="", encoding="utf-8") as csv_file:
#     data = csv.reader(csv_file, delimiter="@")
#     print("")
#
#     rows = []
#     for row in data:
#         rows.append(row)
#
# # print(rows)
#
# for n in rows[0]:
#     print(n)
#
# print("")
#
# for a in rows[1:]:
#     print(a)
#
#
# ==========================================
a = "A"
b = "B"
c = "C"


def add_data_csv(d1, d2, d3):
    with open('./cafe-data.csv', mode='a') as csv_file:
        data = f"\n{d1},{d2},{d3}"
        csv_file.write(data)


add_data_csv(a, b, c)

