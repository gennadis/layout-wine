from datetime import date
from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape

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


winery_age = get_age(1920)
suffix = get_suffix(winery_age)

rendered_page = template.render(
    winery_age=winery_age,
    suffix=suffix,
)

with open("index.html", "w", encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(("0.0.0.0", 8000), SimpleHTTPRequestHandler)
server.serve_forever()
