import json
from elastic_enterprise_search import AppSearch
from flask import Flask, render_template, request
from elastic_app_search import Client
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

with open("config.json") as json_data_file:
    config = json.load(json_data_file)

client = Client(
    base_endpoint=config['appsearch']['base_endpoint'],
    api_key=config['appsearch']['api_key'],
    use_https=True
)

engine_name = config['appsearch']['engine_name']

@app.route("/")
def home():
   """
    Home endpoint.
    ---
    responses:
      200:
        description: A list of search results or documents.
        content:
          application/json:
            example:
              - studio: Bones
                genres:
                  - Mystery
                  - Seinen
                  - Supernatural
                hype: 31993
                description: "Nakajima Atsushi was kicked out of his orphanage..."
                title:
                  link: "http://myanimelist.net/anime/31478/Bungou_Stray_Dogs"
                  text: "Bungou Stray Dogs"
                start_date: "Apr 7, 2016, 01:05 (JST)"
    """
   data = client.search(engine_name, "", {})
   return render_template("index.html", data=data)

@app.route("/search", methods=['POST'])
def search():
    """
    Search endpoint.
    ---
    parameters:
      - name: search
        in: formData
        type: string
        description: The search query.
        required: true
    responses:
      200:
        description: A list of search results.
    """
    if request.method == 'POST':
        query = request.form['search']
        data = client.search(engine_name, query, {})
        return render_template("index.html", data=data)

@app.route("/index")
def index():
    """
    Index endpoint.
    ---
    responses:
      200:
        description: Information about the indexing process.
    """
    f = open('data.json',)
    documents = json.load(f)
    data = client.index_documents(engine_name, documents)
    return render_template("about.html", data=data)

if __name__ == "__main__":
    app.run(debug=False)
