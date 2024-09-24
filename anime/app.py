from animeflv import AnimeFLV
from flask import Flask, render_template, request, url_for
from api import AnimeFLV as ani
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
url = "https://api.jikan.moe/v4"
# Inicializa la clase AnimeFLV
anime_api = AnimeFLV()
ani_api = ani()



def dividir_lista(lista, partes):
    # Dividimos la lista en partes iguales
    longitud = len(lista)
    tamaño_parte = longitud // partes
    # Creamos las sublistas usando comprensión de listas
    return [lista[i * tamaño_parte: (i + 1) * tamaño_parte] for i in range(partes)]

@app.route('/', methods=['GET'])
@app.route('/-<int:sublist_index>', methods=['GET'])
@app.route('/<int:sublist_index>', methods=['GET'])
def home(sublist_index=0):
    # Obtiene los últimos animes
    last_animes = anime_api.get_latest_animes()

    # Obitiene los ultimos episodios emitidos
    last_episodes = anime_api.get_latest_episodes()

    #obtiene animes en emision
    emision = ani_api.animes_emision()
    partes = 2
    listas_divididas = dividir_lista(last_episodes, partes)
    print('1',listas_divididas[0],"1")
    print('2',listas_divididas[1],"2")


    print (sublist_index)
    return render_template('home.html', 
                           last_animes=last_animes,
                           last_episodes=last_episodes,
                           emision=emision

                           )

@app.route('/search', methods=['GET','POST'])
def search():
    query = request.form.get('query')
    if request.method == 'POST':
        # Busca el anime con la API de AnimeFLV
        search_results = anime_api.search(query)
            
        # Renderiza los resultados en una plantilla HTML
        return render_template('results.html', results=search_results)
    return render_template('search.html')


@app.route('/info/<anime_id>', methods=['GET'])
def info(anime_id):
    # Obtiene la información de un anime en particular
    anime_info = anime_api.get_anime_info(anime_id)
    
    # Renderiza la información del anime
    return render_template('info.html', anime_info=anime_info)

@app.route('/episode/<anime_id>/<episode_id>/<server>=MEGA', methods=['GET', 'POST'] )
def episode(anime_id,episode_id,server="MEGA"):
    episode = anime_api.get_video_servers(str(anime_id),int(episode_id))
    anime_info = anime_api.get_anime_info(anime_id)
    link = anime_api.get_links(str(anime_id),int(episode_id))
    next_episode = int(episode_id) + 1
    return render_template('episode.html', 
                           episode=episode,
                           episode_id=episode_id,
                           anime_id=anime_id,anime_name=anime_id.replace("-"," "),
                           link=link,
                           server=server,
                           next_episode=next_episode,
                           anime_info=anime_info)


@app.route("/api/search")
@app.route("/api/search/<int:page>")
@app.route("/api/search/<query>/<int:page>")
@app.route("/api/search/<query>/<int:page>")
def search_api(query='',page=1, genre=None):
    anime_list = anime_api.search(query=query, page=page)  # Consigue la lista de animes
    result_html = ""

    if not anime_list:
        return "No se encontraron animes"

    # Iteramos sobre los animes obtenidos
    for result in anime_list:
        result_html += f'''
        <div class="box" style="width:150px;height:auto;">
            <li>
                <img src="{result.poster}" alt="{result.title}" style="width:150px;height:auto;">
                <a href="{url_for('info', anime_id=result.id)}">{result.title}</a>
            </li>
        </div>
        '''

    return result_html

@app.route("/api/search_gene/<int:page>")
@app.route("/api/search_gene/<geners>/<int:page>")
def search_api_genre(geners=None,page=1):
    anime_list = ani_api.filter(geners=geners, page=page)  # Consigue la lista de animes
    result_html = ""

    if not anime_list:
        return "No se encontraron animes"

    # Iteramos sobre los animes obtenidos
    for result in anime_list:
        result_html += f'''
        <div class="box" style="width:150px;height:auto;">
            <li>
                <img src="{result.poster}" alt="{result.title}" style="width:150px;height:auto;">
                <a href="{url_for('info', anime_id=result.id)}">{result.title}</a>
            </li>
        </div>
        '''

    return result_html

@app.route('/search/geners', methods=['GET','POST'])
def search_gene():
    query = request.form.get('query')
    return render_template('search_gene.html')

if __name__ == '__main__':
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run(debug=True)

