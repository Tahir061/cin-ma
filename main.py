import sqlite3
from sqlite3 import Error
from apiTest import get_details
from datetime import date, datetime


class bold_color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def list_movies(conn):
    cur = conn.cursor()

    cur.execute(
        "SELECT id, title, duration, ChildrenAllowed, imdb_id FROM movies")

    rows = cur.fetchall()
    if len(rows) > 0:
        header = '+----+----------------------------+------+-----+-----------+\n'
        header += '| ID |        Title               | Duur | KNT |  IMDB_ID  |\n'
        header += '+----+----------------------------+------+-----+-----------+'
        print(header)

        for row in rows:
            id = row[0]
            title = row[1]
            dura = row[2]
            knt = 'Yes' if row[3] == 1 else 'No'
            imdb_id = row[4]
            print('|{0:^4}|{1:^28}|{2:^6}|{3:^5}|{4:^11}|'.format(
                id, title, dura, knt, imdb_id))
        print('+----+----------------------------+------+-----+-----------+')
    else:
        print('Leeg database')


def add_movies(conn):
    # imdb_id = 'tt0978764'
    imdb_id = input('IMDB id of movie: ')
    res = get_details(imdb_id)
    if res == -1:
        print(bold_color.RED, 'Film niet gevonden', bold_color.END)
        return
    title = input(bold_color.BOLD +
                  'Titel: ({0}) '.format(res['title'])+bold_color.END)
    duration = input(
        bold_color.BOLD+'Duur: ({0}) '.format(res['duration'])+bold_color.END)
    KNT = input(bold_color.BOLD +
                'KNT: ({0}) '.format(res['KNT'])+bold_color.END)

    if KNT == False:
        KNT = 0
    else:
        KNT = 1

    sql = "INSERT INTO movies (title, imdb_id, ChildrenAllowed, duration) VALUES ('{0}', '{1}', '{2}', '{3}')".format(
        title, imdb_id, KNT, int(duration))

    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

    print(bold_color.GREEN, "Film is succesvol toegevoegd", bold_color.END)


def search_movies(conn):
    # film op id zoeken: (id in db not imdb id)
    _id = input('Voer id in om in database te zoeken: ')
    sql = "SELECT id, title, duration, ChildrenAllowed, imdb_id FROM movies WHERE id = '{}'".format(
        _id)
    cur = conn.cursor()
    cur.execute(sql)

    rows = cur.fetchall()
    if len(rows) > 0:
        header = '+----+----------------------------+------+-----+-----------+\n'
        header += '| ID |        Titel               | Duur | KNT |  IMDB_ID  |\n'
        header += '+----+----------------------------+------+-----+-----------+'
        print(header)

        for row in rows:
            id = row[0]
            title = row[1]
            dura = row[2]
            knt = 'Yes' if row[3] == 1 else 'No'
            imdb_id = row[4]
            print('|{0:^4}|{1:^28}|{2:^6}|{3:^5}|{4:^11}|'.format(
                id, title, dura, knt, imdb_id))
        print('+----+----------------------------+------+-----+-----------+')
    else:
        print(bold_color.RED, 'Geen film gevonden in database', bold_color.END)


def delete_movies(conn):
    # Delete movie on id: (id in database not imdb id)
    _id = input('Voer id in om te verwijderen in database: ')
    sql = "DELETE FROM movies WHERE id = '{}'".format(_id)
    cur = conn.cursor()
    if cur.execute(sql):
        conn.commit()
    else:
        print(bold_color.RED, 'Geen film gevonden met opgegeven id!', bold_color.END)


def manage_movies(conn):
    i = -1

    prompt = '1. Lijst met films\n'
    prompt += '2. Voeg film toe\n'
    prompt += '3. Zoek film\n'
    prompt += '4. Verwijder film\n'
    prompt += '0. Terug naar hoofdmenu\n\n'
    prompt += 'Voer keuze in: '

    while i != 0:
        i = int(input(prompt))

        if i == 0:
            continue
        if i == 1:
            list_movies(conn)
        elif i == 2:
            add_movies(conn)
        elif i == 3:
            search_movies(conn)
        elif i == 4:
            delete_movies(conn)
        else:
            print('Ongeldige keuze, probeer het opnieuw\n')


def screening_today(conn):
    cur = conn.cursor()
    # sql = "SELECT id, movie_id, threeD, auditorium_id, starttime FROM screening_movie"
    sql = "SELECT s.id, m.title, s.threeD, s.auditorium_id, s.starttime FROM screening_movies s, movies m WHERE s.movie_id = m.id"
    cur.execute(sql)

    rows = cur.fetchall()
    if len(rows) > 0:
        header = '+----+------------------------+--------+--------+------+\n'
        header += '| ID |        Film            | Moment | Aud_ID |  3D  |\n'
        header += '+----+------------------------+--------+--------+------+'
        print(header)
        for row in rows:
            _id = row[0]
            _film = row[1]
            _3D = 'Yes' if row[2] == 1 else 'No'
            _aud_id = row[3]
            _dura = row[4].split(" ")[-1][:-3]
            print('|{0:^4}|{1:^24}|{2:^8}|{3:^8}|{4:^6}|'.format(
                _id, _film, _dura, _aud_id, _3D))
        print('+----+------------------------+--------+--------+------+')


def add_screening(conn):
    _today = date.today().strftime("%d-%m-%Y")
    _date = input(bold_color.BOLD +
                  "Date : ({0})".format(_today) + bold_color.END)
    if len(_date) == 0:
        _date = _today
    _title = input(bold_color.BOLD+'Title film: ' + bold_color.END)
    cur = conn.cursor()
    cur.execute(
        "SELECT id, title, threeD FROM movies WHERE title LIKE '%{0}%'".format(_title))

    rows = cur.fetchall()
    for row in rows:
        print(bold_color.YELLOW, row[0], '. ', bold_color.END, row[1])
    idx = int(input('Kies film id: '))

    for row in rows:
        if int(row[0]) == idx:
            _title = row[0]
            _3D = row[2]
    _audt = int(input('Auditorium: '))

    # check als film speelt op die dag

    cur.execute("SELECT auditorium_id, starttime FROM screening_movies")
    flag = False
    for row in cur.fetchall():
        if int(row[0]) == _audt and row[1] == _date+' 24:00:00':
            flag = True

    if not flag:
        sql = "INSERT INTO screening_movies (movie_id, threeD, auditorium_id, starttime) VALUES ('{0}', {1}, {2}, '{3}')".format(
            _title, _3D, _audt, _date+' 24:00:00')

        if cur.execute(sql):
            print(bold_color.GREEN, "Screening toegevoegd", bold_color.END)
            conn.commit()
    else:
        print(bold_color.RED, "Kan niet meerdere films op dezelfde dag in dezelfde audit vertonen {0}".format(
            _date), bold_color.END)


def delete_screening(conn):
    _id = int(input("Voeg screening id toe om te verwijderen: "))
    cur = conn.cursor()

    cur.execute("DELETE FROM screening_movies WHERE id = {0}".format(_id))
    conn.commit()
    if cur.rowcount > 0:
        print(bold_color.GREEN, "Verwijderd", bold_color.END)
    else:
        print(bold_color.RED, "Onjuiste index", bold_color.END)


def manage_screening(conn):
    i = -1

    prompt = '1. Screening vandaag\n'
    prompt += '2. Voeg screening toe\n'
    prompt += '3. Verwijder screening\n'
    prompt += '0. Terug naar hoofdmenu\n\n'
    prompt += 'Voer keuze in: '

    while i != 0:
        i = int(input(prompt))

        if i == 0:
            continue
        if i == 1:
            screening_today(conn)
        elif i == 2:
            add_screening(conn)
        elif i == 3:
            delete_screening(conn)
        else:
            print('Ongeldige keuze, probeer het opnieuw\n')


def weekly_ticketsale(conn):
    sql = "SELECT m.title, sum(r.ticketPaid) as s FROM movies m, reservations r WHERE r.movie_id = m.id GROUP BY m.title ORDER BY s desc"
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()

    header = '+------------------------+--------+\n'
    header += '|        Film            | Ticket |\n'
    header += '+------------------------+--------+'
    print(header)
    for row in rows:
        print('|{0:^24}|{1:^8}|'.format(row[0], row[1]))
    print('+------------------------+--------+')


def rank_movie_yeild(conn):
    sql = "SELECT m.title, sum(r.price) FROM movies m, reservations r WHERE r.movie_id = m.id GROUP BY m.title"
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()

    header = '+------------------------+---------+\n'
    header += '|        Film            | Omzet   |\n'
    header += '+------------------------+---------+'
    print(header)
    for row in rows:
        print('|{0:^24}|{1:^9}|'.format(row[0], row[1]))
    print('+------------------------+---------+')


def consult_tickets(conn):
    i = -1

    prompt = '1. Wekelijs verkoop\n'
    prompt += '2. Ranking omzet film\n'
    prompt += '0. Terug naar hoofdmenu\n\n'
    prompt += 'Voer keuze in: '

    while i != 0:

        i = int(input(prompt))

        if i == 0:
            continue
        if i == 1:
            weekly_ticketsale(conn)
        elif i == 2:
            rank_movie_yeild(conn)
        else:
            print('Onjuist keuze, probeer opnieuw\n')


def call_menu(conn):
    i = -1
    prompt = '1. Beheer Filmen\n'
    prompt += '2. Beheer Screening\n'
    prompt += '3. Raadpleeg tickets\n'
    prompt += '0. Sluit\n\n'
    prompt += 'Voer keuze in: '

    while i != 0:

        i = int(input(prompt))

        if i == 0:
            continue
        if i == 1:
            manage_movies(conn)
        elif i == 2:
            manage_screening(conn)
        elif i == 3:
            consult_tickets(conn)
        else:
            print('Ongeldige keuze, probeer het opnieuw\n')


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn


if __name__ == '__main__':
    db_file = 'cinemax.db'
    conn = create_connection(db_file)
    if conn:
        call_menu(conn)
        conn.close()


# tt3228774
# tt0993840
