
import os

from openpyxl import Workbook
from openpyxl.styles import Font


def read_txt():
    data = []
    data.append([
        "НАЗВАНИЕ", "ОПИСАНИЕ", "АДРЕС&ТЕЛЕФОН", "EMAIL", "САЙТ", "URL",
        ])

    content = os.listdir('Out')
    for file_name in content:
        with open(f"Out\\{file_name}", encoding="utf8") as f:
            row = ["", "", "", "", "", "", ]

            s = f.readlines()
            s = [st.replace("\n", "") for st in s]

            row[0] = s[0]   # название
            row[1] = s[1]   # описние
            row[5] = "https://alestech.ru/factory/" + file_name.split(".")[0]
            for i in range(2, len(s)):
                if ("@" in s[i]) and ("." in s[i]):
                    row[3] += s[i]      # email
                elif "http" in s[i]:
                    row[4] += s[i]      # сайт
                elif ("Нет сайта" not in s[i]) and \
                        ("Официальный сайт" not in s[i]) and \
                        ("Cайт холдинга" not in s[i]):
                    row[2] = row[2] + ' ' + s[i]    # адрес и телефон
        data.append(row)

    return data


def txt_to_excel():
    # сохраняем данные в excel
    excel_file = Workbook()
    excel_sheet = excel_file.create_sheet(title="Data", index=0)

    list(map(lambda x: excel_sheet.append(x), read_txt()))

    excel_sheet.row_dimensions[1].font = Font(bold=True)
    excel_sheet.column_dimensions["A"].font = Font(bold=True)
    excel_sheet.freeze_panes = "A2"

    excel_file.save(filename="LesTech.xlsx")


def save_result():
    txt_to_excel()


if __name__ == '__main__':
    save_result()
