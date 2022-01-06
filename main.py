from datetime import date
from collections import defaultdict, OrderedDict
from http.server import HTTPServer, SimpleHTTPRequestHandler


from pandas import read_excel
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pandas.io import excel

env = Environment(
    loader=FileSystemLoader("."), autoescape=select_autoescape(["html", "xml"])
)

template = env.get_template("template.html")


def get_age(year_opened: int) -> int:
    """Get winery age in years since year opened."""
    age = date.today().year - year_opened
    return age


def get_suffix(age: int) -> str:
    """Get год / года / лет suffix."""
    if str(age).endswith("1"):
        return "год"
    if str(age).endswith(("2", "3", "4")):
        return "года"
    return "лет"


def get_drinks(filename: str) -> dict:
    """Get drinks from excel file
    and return them divided by categories"""

    df = read_excel(filename, na_values=None, keep_default_na=False)
    drinks = df.to_dict(orient="records")
    categories = defaultdict(list)

    for drink in drinks:
        categories[drink["Категория"]].append(drink)

    sorted_categories = OrderedDict(sorted(categories.items()))

    return sorted_categories


winery_age: int = get_age(1920)
suffix: str = get_suffix(winery_age)
categories: dict = get_drinks("wine3.xlsx")

rendered_page = template.render(
    winery_age=winery_age,
    suffix=suffix,
    categories=categories,
)

with open("index.html", "w", encoding="utf8") as file:
    file.write(rendered_page)


server = HTTPServer(("0.0.0.0", 8000), SimpleHTTPRequestHandler)
server.serve_forever()
