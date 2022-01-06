from datetime import date
from collections import defaultdict, OrderedDict
from http.server import HTTPServer, SimpleHTTPRequestHandler

from pandas import read_excel
from jinja2 import Environment, FileSystemLoader, select_autoescape


WINERY_ESTABLISHED = 1920
DRINKS_FILENAME = "wine3.xlsx"


env = Environment(
    loader=FileSystemLoader("."), autoescape=select_autoescape(["html", "xml"])
)
template = env.get_template("template.html")


def count_years_since(established: int) -> str:
    """Get winery age in years since year opened
    with [год, года, лет] suffix"""

    age = str(date.today().year - established)
    suffix = "лет"

    if age.endswith("1"):
        suffix = "год"
    elif age.endswith(("2", "3", "4")):
        suffix = "года"

    return f"{age} {suffix}"


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


rendered_page = template.render(
    winery_age=count_years_since(WINERY_ESTABLISHED),
    categories=get_drinks(DRINKS_FILENAME),
)

with open("index.html", "w", encoding="utf8") as file:
    file.write(rendered_page)


server = HTTPServer(("0.0.0.0", 8000), SimpleHTTPRequestHandler)
server.serve_forever()
