import json
from datetime import date
from tabulate import tabulate
import datetime
import os
import tempfile
import shutil

months = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December",
}


def safe_write_json(filename, data):

    dir_name = os.path.dirname(filename) or "."
    with tempfile.NamedTemporaryFile("w", dir=dir_name, delete=False) as tmp:
        json.dump(data, tmp, indent=4)
        temp_name = tmp.name

    shutil.move(temp_name, filename)


def add_expense(description, amount):

    if amount <= 0:
        return "# Amount must be greater than 0"

    loaded_data = read_all_expenses()
    try:
        last_id = loaded_data[-1]["id"]
    except IndexError:
        last_id = -1

    current_id = last_id + 1

    expense = {
        "id": current_id,
        "Date": f"{date.today()}",
        "description": description,
        "amount": amount,
    }

    loaded_data.append(expense)
    updated_expenses = loaded_data

    safe_write_json("expenses.json", updated_expenses)

    return f"# Expense added successfully (ID: {expense['id']})"


def read_all_expenses():

    if not os.path.exists("expenses.json"):
        return []
    else:
        try:
            with open("expenses.json", "r") as f:
                return json.load(f)
        except json.decoder.JSONDecodeError:
            return []


def list_all_expenses():
    loaded_data = read_all_expenses()
    for expense in loaded_data:
        expense["amount"] = f"${expense['amount']:.2f}"
    return tabulate(loaded_data, headers="keys", tablefmt="grid")


def show_summary(month=None):
    total = 0
    loaded_data = read_all_expenses()

    for expense in loaded_data:
        if month is not None:
            if datetime.datetime.strptime(expense["Date"], "%Y-%m-%d").month == month:
                total = total + expense["amount"]
        else:
            total = total + expense["amount"]

    if month is not None:
        return f"# Total expenses for {months[month]}: ${total:.2f}"
    else:
        return f"# Total expenses: ${total:.2f}"


def delete_expense(id):

    exists = False
    loaded_data = read_all_expenses()

    for index in range(0, len(loaded_data)):
        if loaded_data[index]["id"] == id:
            exists = True
            loaded_data.pop(index)
            break

    if exists:

        safe_write_json("expenses.json", loaded_data)
        return "# Expense deleted successfully"

    else:
        return f"Expense with ID: {id} was not found"
