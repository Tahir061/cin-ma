from tmdbv3api import TMDb, Movie

tmdb = TMDb()
tmdb.api_key = 'd095db72fae359f32c066ffdb20b7576'

tmdb.language = 'en'
tmdb.debug = True

movie = Movie()


def get_details(id):
    try:
        m = movie.details(id)
        return {'title': m['title'],
                'KNT': m['adult'],
                'duration': m['runtime']
                }
    except:
        return -1
