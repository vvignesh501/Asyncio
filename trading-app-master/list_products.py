import csv
import os

cur_path = os.path.dirname(__file__)


def list_products():
    with open(os.path.join(cur_path, "static/csv/products.csv"), "r") as f:
        products = [{k: str(v) for k, v in row.items()}
                    for row in csv.DictReader(f, skipinitialspace=True)]
        return products
