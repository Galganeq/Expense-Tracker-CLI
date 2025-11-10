import argparse
from functions import add_expense, list_all_expenses, show_summary, delete_expense

parser = argparse.ArgumentParser(description="Expense Tracker CLI")
subparsers = parser.add_subparsers(dest="command", required=True)

parser_add = subparsers.add_parser("add", help="Add an expense")
parser_add.add_argument("--amount", type=int, help="Amount", required=True)
parser_add.add_argument(
    "--description", type=str, help="What is the expense", required=True
)

parser_list = subparsers.add_parser("list", help="List expenses")

parser_delete = subparsers.add_parser("delete", help="Delete expense")
parser_delete.add_argument(
    "--id", type=int, help="Id of the task to delete", required=True
)

parser_summary = subparsers.add_parser("summary", help="Summarise all of the expenses")
parser_summary.add_argument("--month", type=int, help="Provide the month")

args = parser.parse_args()


match args.command:
    case "list":
        print(list_all_expenses())
    case "add":
        print(add_expense(args.description, args.amount))
    case "summary":
        print(show_summary(args.month))
    case "delete":
        print(delete_expense(args.id))
