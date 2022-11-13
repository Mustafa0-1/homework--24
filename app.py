import itertools
import os
import re

from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

commands_list = ["filter", "map", "unique", "sort", "limit"]


def commands(cmd: str, value: str, data: list[str]) -> list:
    """
    Функция для работы с данными
    """
    if cmd == "filter":
        result = list(filter(lambda v: value in v, data))
    elif cmd == "map":
        col_num = int(value)
        result = list(map(lambda v: v.split()[col_num], data))
    elif cmd == "unique":
        result = list(set(data))
    elif cmd == "sort":
        result = sorted(data) if value == "asc" else sorted(data, reverse=True)
    elif cmd == "limit":
        col_num = int(value)
        result = list(itertools.islice(data, col_num))
    elif cmd == "regex":
        regex = re.compile(value)
        result = list(filter(lambda v: re.search(regex, v), data))

    return result


@app.route("/perform_query", methods=["POST"])
def perform_query():
    """
    роут для работы с данными из файла
    """
    cmd1 = request.json.get("cmd1")
    value1 = request.json.get("value1")
    cmd2 = request.json.get("cmd2")
    value2 = request.json.get("value2")
    filename = request.json.get("filename")


    if cmd1 and cmd2 not in commands_list:
        return BadRequest, 400

    if filename is None or not os.path.exists(os.path.join(DATA_DIR, filename)):
        return BadRequest, 400

    with open(os.path.join(DATA_DIR, filename), encoding='utf-8') as file:
        res1 = commands(cmd1, value1, file)
        res2 = commands(cmd2, value2, res1)

        return jsonify(res2)


if __name__ == "__main__":
    app.run(debug=True)

# Для запроса в Postman:
#     {
#         "cmd1": "regex",
#         "value1": "images/\\w+\\.png",
#         "cmd2": "sort",
#         "value2": "asc",
#         "filename": "apache_logs.txt"
#     }
