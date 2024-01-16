import json
from elastic_enterprise_search import AppSearch
from flask import Flask, redirect, render_template, request, url_for
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

@app.route("/add_anime", methods=['GET', 'POST'])
def add_anime():
    if request.method == 'POST':
        title = request.form['title']
        genres = request.form.getlist('genres')
        studio = request.form['studio']
        description = request.form['description']
        hype=request.form['hype']

        # Assuming you have a function to add the anime to your search engine
        add_anime_to_index(title, genres, studio, description,hype)

        return redirect(url_for('home'))

    genres = ["Mystery", "Seinen", "Supernatural"]  # Add more genres as needed
    return render_template("add_anime.html", genres=genres)

def add_anime_to_index(title, genres, studio, description,hype):
    # Assuming you have a function to add the anime to your search engine
    document = {
        'title': title,
        'genres': genres,
        'studio': studio,
        'description': description,
        'hype':hype 
        # Add other fields as needed
    }

    # Assuming you have a function to index documents in your search engine
    client.index_document(engine_name, document)

    
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
   genres = ["Mystery", "Seinen", "Comedy","Ecchi","Fantasy","Harem","Romance","School","Sci-Fi","Supernatural"]  # Add more genres as needed
   studios = ["Bones", "Studio Ghibli", "Madhouse","A-1 Pictures","Trigger","Diomedea","Production I.G","Studio Pierrot","Studio Deen","Lay-duce","White Fox"]
   return render_template("index.html", data=data, genres=genres,studios=studios)

@app.route("/search", methods=['POST','GET'])
def search():
    """
    Search endpoint.
    ---
    parameters:
      - name: search
        in: query
        type: string
        description: The search query.
        required: false
      - name: genre
        in: query
        type: string
        description: The selected genre for filtering.
        required: false
    responses:
      200:
        description: A list of search results.
    """
    query = request.args.get('search', '')
    genre_filter = request.args.get('genre', '')
    studio_filter = request.args.get('studio', '')

    filters = {}
    if genre_filter:
        filters['genres'] = genre_filter
    if studio_filter:
        filters['studio'] = studio_filter

    data = client.search(engine_name, query, {'filters': filters})
    genres = ["Mystery", "Seinen", "Comedy","Ecchi","Fantasy","Harem","Romance","School","Sci-Fi","Supernatural"]  # Add more genres as needed
    studios = ["Bones", "Studio Ghibli", "Madhouse","A-1 Pictures","Trigger","Diomedea","Production I.G","Studio Pierrot","Studio Deen","Lay-duce","White Fox"]  # Add more studios as needed
    return render_template("index.html", data=data, genres=genres, studios=studios, selected_genre=genre_filter, selected_studio=studio_filter)


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
    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=False)
