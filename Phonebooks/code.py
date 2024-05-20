from pprint import pprint
import csv
import re

# читаем адресную книгу в формате CSV в список contacts_list
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# Функция для обработки имен
def process_name(name_parts):
    full_name = " ".join(name_parts[:3]).split()
    if len(full_name) == 2:
        full_name.append('')
    return full_name

# Функция для форматирования телефона
def format_phone(phone):
    pattern = re.compile(
        r'(\+7|8)?\s*\(?(\d{3})\)?\s*[-\s]?(\d{3})[-\s]?(\d{2})[-\s]?(\d{2})(\s*(доб\.)\s*(\d+))?'
    )
    substitution = r'+7(\2)\3-\4-\5'
    formatted_phone = pattern.sub(substitution, phone)

    if pattern.search(phone):
        if pattern.search(phone).group(6):
            formatted_phone += f' доб.{pattern.search(phone).group(8)}'
    return formatted_phone

# Функция для объединения дублирующихся записей
def merge_contacts(contacts):
    contacts_dict = {}
    for contact in contacts:
        lastname, firstname, surname = contact[:3]
        # Если отчество отсутствует, то группируем только по фамилии и имени
        full_name = (lastname, firstname)

        if full_name not in contacts_dict:
            contacts_dict[full_name] = contact
        else:
            existing_contact = contacts_dict[full_name]
            for i in range(3, len(contact)):
                if not existing_contact[i] and contact[i]:
                    existing_contact[i] = contact[i]
    return list(contacts_dict.values())

# Проходим по каждой строке в контактах и обрабатываем имена и телефоны
processed_contacts = []
for contact in contacts_list:
    lastname, firstname, surname = process_name(contact[:3])
    contact[0], contact[1], contact[2] = lastname, firstname, surname

    if len(contact) > 5:
        contact[5] = format_phone(contact[5])

    processed_contacts.append(contact)

# Объединяем дублирующиеся записи
merged_contacts_list = merge_contacts(processed_contacts)

# Записываем результат в новый CSV файл
with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(merged_contacts_list)

# Проверяем результат
pprint(merged_contacts_list)
