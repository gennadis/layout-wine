from datetime import date
from collections import defaultdict, OrderedDict
from http.server import HTTPServer, SimpleHTTPRequestHandler

from pandas import read_excel
from jinja2 import Environment, FileSystemLoader, select_autoescape


WINERY_ESTABLISHED_YEAR = 1920
DRINKS_FILEPATH = "example.xlsx"


def count_years_since(year_established: int) -> str:
    """Get winery age in years since year opened
    with [год, года, лет] suffix"""

    age = str(date.today().year - year_established)
    suffix = "лет"

    if age.endswith("1"):
        suffix = "год"
    elif age.endswith(("2", "3", "4")):
        suffix = "года"

    return f"{age} {suffix}"


def get_drinks(filepath: str) -> dict:
    """Get drinks from excel file
    and return them divided by categories"""

    df = read_excel(filepath, na_values=None, keep_default_na=False)
    drinks = df.to_dict(orient="records")
    drinks_by_categories = defaultdict(list)

    for drink in drinks:
        drinks_by_categories[drink["Категория"]].append(drink)

    sorted_drinks_by_categories = OrderedDict(sorted(drinks_by_categories.items()))

    return sorted_drinks_by_categories


def main():
    env = Environment(
        loader=FileSystemLoader("."), autoescape=select_autoescape(["html", "xml"])
    )
    template = env.get_template("template.html")

    rendered_page = template.render(
        winery_age=count_years_since(WINERY_ESTABLISHED_YEAR),
        categories=get_drinks(DRINKS_FILEPATH),
    )

    with open("index.html", "w", encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(("0.0.0.0", 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
