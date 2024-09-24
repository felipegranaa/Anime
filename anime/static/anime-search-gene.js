let currentPage = 1;
let isLoading = false;
const animeList = document.getElementById('anime-list');
const loadingIndicator = document.getElementById('loading');
const apiEndpoint = '/api/search_gene'; // API de Jikan (MyAnimeList)
const apiEndpoint1 = '/api/search';
let statuss = true;

// Función para obtener animes de la API
async function fetchAnimes(query = '', page = currentPage) {
    console.log("Fetching animes..."); // Agregar log para verificar si la función se ejecuta
    isLoading = true;
    loadingIndicator.style.display = 'block'; // Mostrar el indicador de carga
    try {
        if (query === ''){
            const response = await fetch(`${apiEndpoint}/${page}`);
            const body = await response.text();
            console.log(response)
            console.log(body);  // Verificar si los datos se obtienen correctamente
            return body
        }
        else{
            const response = await fetch(`${apiEndpoint}/${query}/${page}`);
            const body = await response.text();
            console.log(response)
            console.log(body);  // Verificar si los datos se obtienen correctamente
            return body
        }
        
    } catch (error) {
        console.error('Error al obtener animes:', error);
        return "error";
    } finally {
        isLoading = false;
        loadingIndicator.style.display = 'none'; // Ocultar el indicador de carga
    }
}async function fetchAnimes1(query = '', page = currentPage) {
    console.log("Fetching animes..."); // Agregar log para verificar si la función se ejecuta
    isLoading = true;
    loadingIndicator.style.display = 'block'; // Mostrar el indicador de carga
    try {
        if (query === ''){
            const response = await fetch(`${apiEndpoint}/${page}`);
            const body = await response.text();
            console.log(response)
            console.log(body);  // Verificar si los datos se obtienen correctamente
            return body
        }
        else{
            const response = await fetch(`${apiEndpoint}/${query}/${page}`);
            const body = await response.text();
            console.log(response)
            console.log(body);  // Verificar si los datos se obtienen correctamente
            return body
        }
    } catch (error) {
        console.error('Error al obtener animes:', error);
        return "error";
    } finally {
        isLoading = false;
        loadingIndicator.style.display = 'none'; // Ocultar el indicador de carga
    }
}
// Función para agregar animes a la página
function appendAnimes(animes) {
    if (animes.length === 0) {
        console.log('No se encontraron más animes.');
        return;
    }

    animes.forEach(anime => {
        const animeItem = document.createElement('div');
        animeItem.classList.add('anime-item');
        animeItem.innerHTML = `
            <h3>${anime.data[0].title}</h3>
            <img src="${anime.data[0].images.jpg.image_url}" alt="${anime.title}" width="200">
            <p>${anime.synopsis}</p>
        `;
        animeList.appendChild(animeItem);
    });
}

// Función para manejar el envío del formulario
document.getElementById('search-form').addEventListener('submit', async function (event) {
    event.preventDefault();
    console.log('Formulario enviado'); // Verificar si el formulario se envía
    animeList.innerHTML = ''; // Limpiar los resultados anteriores
    currentPage = 1;
    const query = document.getElementById('query').value;
    console.log('Buscando anime:', query); // Verificar la búsqueda
    await searchAnime1(query, currentPage);
    statuss = true;
    
});
document.getElementById('generos').addEventListener('submit', async function (event) {
    event.preventDefault();
    console.log('Formulario de géneros enviado'); 
    animeList.innerHTML = ''; // Limpiar los resultados anteriores
    currentPage = 1;
    const selectedGenres = Array.from(document.querySelectorAll('#genero option:checked')).map(option => option.value);
    const query = selectedGenres.join(','); // Formateamos los géneros seleccionados
    console.log('Buscando animes con géneros:', query);
    const animes = await fetchAnimes(query, currentPage);
    await searchAnime(query,currentPage ); // Suponiendo que la API retorna una lista en `data`
    statuss = false;
});

async function searchAnime(query,page) {
    console.log('Cargando más animes...'); // Verificar si se llega al final de la página

    
    const animeList = document.getElementById('anime-list');
    for (let i = 0; i < 7; i++) {
        const animes = await fetchAnimes(query, currentPage);
        currentPage = currentPage+1; 

        const animeItem = document.createElement('div');
        animeItem.innerHTML = animes; 
        animeList.appendChild(animeItem); 
    }
}
async function searchAnime1(query='',currentPage=1) {
    console.log('Cargando más animes...'); // Verificar si se llega al final de la página

    
    const animeList = document.getElementById('anime-list');
    for (let i = 0; i < 7; i++) {
        const animes = await fetchAnimes1(query, currentPage);
        currentPage = currentPage+1; 

        const animeItem = document.createElement('div');
        animeItem.innerHTML = animes; 
        animeList.appendChild(animeItem); 
    }
}
// Cargar más animes cuando el usuario se desplaza hacia abajo
window.addEventListener('scroll', async function () {
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 100 && !isLoading && statuss === true) {
        const query = document.getElementById('query').value;
        currentPage = currentPage + 7;
        await searchAnime1(query,currentPage);
        
    
    }
    else if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 100 && !isLoading && statuss === false){
        const selectedGenres = Array.from(document.querySelectorAll('#genero option:checked')).map(option => option.value);
        currentPage = currentPage + 7;
        await searchAnime(query=selectedGenres,currentPage)
        
    }
});

searchAnime1();
