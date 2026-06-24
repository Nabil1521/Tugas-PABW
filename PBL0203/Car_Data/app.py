import cherrypy
import pandas as pd
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("index.html")

class WebApp:

    @cherrypy.expose
    def index(self):
        df = pd.read_csv("CarPrice_Assignment.csv")

        data = df.head(20).to_dict(orient="records")
        
        return template.render(data=data)
        for row in data:
            html = html.replace("{{ row.car_ID }}", str(row["car_ID"]))

        return html

if __name__ == "__main__":
    cherrypy.quickstart(WebApp())