from animeflv import AnimeFLV
from flask import Flask, render_template, request, url_for
from api import AnimeFLV as ani
from werkzeug.middleware.proxy_fix import ProxyFix
from tinydb import TinyDB, Query

app = Flask(__name__)
url = "https://api.jikan.moe/v4"
# Inicializa la clase AnimeFLV
anime_api = AnimeFLV()
ani_api = ani()
# inisalicacion de la clase shove
db = TinyDB('my_database.json')
db_s = TinyDB('my_databases.json')




@app.route('/', methods=['GET'])
def home():
    # Obtiene los últimos animes
    last_animes = anime_api.get_latest_animes()

    # Obtiene los últimos episodios emitidos
    last_episodes = anime_api.get_latest_episodes()

    # Obtiene animes en emisión
    emision = ani_api.animes_emision()
    emision.reverse()

    # Obtiene la sinopsis y el rating del anime
    aim = {}
    User = Query()
    for last_anime in last_animes:
        aid = last_anime.id
        # Busca en la base de datos usando 'aid' como campo de búsqueda
        user_data = db.search(User.id == aid)
        print(user_data)

        if user_data:
            # Si existe en la base de datos, lo cargamos
            aim[aid] = user_data[0]['info']
            print(1)
            continue

        # Si no existe, se obtiene la información de la API
        print(aid)
        anime_info = ani_api.get_anime_info(aid)
        if anime_info == "atributo error":
            result = ["error", "error"]
        else:
            result = [anime_info.synopsis, anime_info.rating]
            print(2, result)

        # Almacena la información en 'aim' y en la base de datos
        aim[aid] = result
        db.insert({'id': aid, 'info': result})  # Almacena con 'id' fijo

        # Comprueba si se insertó correctamente
        user_data = db.search(User.id == aid)
        print(user_data)

    return render_template('home.html', 
                           last_animes=last_animes,
                           last_episodes=last_episodes,
                           emision=emision,
                           anime_info=aim
                          )




        
    return render_template('home.html', 
                           last_animes=last_animes,
                           last_episodes=last_episodes,
                           emision=emision,
                           anime_info=aim

                           )

@app.route('/search', methods=['GET','POST'])
def search():
    

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
@app.route("/api/search/<query>/<genre>/<int:page>")
def search_api(query='',page=1, genre=None):
    anime_list = anime_api.search(query=query, page=page)  # Consigue la lista de animes
    result_html = ""

    

    if not anime_list:
        return "No se encontraron animes"



    # Iteramos sobre los animes obtenidos
    for result in anime_list:
        print(result.synopsis)
        result_html += f'''
        <div class="box" style="width:150px;height:auto;">
        <li class="boxa">
            <a  href="{ url_for('info', anime_id=result.id) }" class="button-img-anime-a">
                <div class="nonis">
                    <div class="noni">
                        <img src="{result.poster}" alt="{result.title}" style="width:150px;height:auto;">
                        
                    </div>
                    <div class="nonas">
                        <p>{result.rating}</p>
                        {result.synopsis}
                    </div>
                </div>
                { result.title }
            </a>
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


