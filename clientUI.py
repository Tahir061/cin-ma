from tkinter import *
from main import create_connection


def get_movies(conn):
    cur = conn.cursor()
    sql = "SELECT m.title, m.duration, m.threeD, (SELECT sum(ticketPaid) FROM reservations WHERE substr(starttime, 1, 10) = strftime('%d-%m-%Y') ), s.starttime, m.id FROM movies m, screening_movies s WHERE  s.movie_id = m.id AND s.threeD = m.threeD AND substr(s.starttime, 1, 10) = strftime('%d-%m-%Y')"
    cur.execute(sql)
    rows = cur.fetchall()

    return rows


def main(conn):
    def check_btn1(event):
        v1 = int(adult_spin.get())+1
        v2 = int(kid_spin.get())
        if details_list.get(ACTIVE):
            if v1 > 0 or v2 > 0:
                    btn['state'] = ACTIVE
            else:
                btn['state'] = DISABLED
            v_price_lbl.set("Totaal prijs tickets €{0}".format((v2 * 7) + (v1 * 10)))

    def check_btn2(event):
        v1 = int(adult_spin.get())
        v2 = int(kid_spin.get())+1
        if details_list.get(ACTIVE):
            if v1 > 0 or v2 > 0:
                    btn['state'] = ACTIVE
            else:
                btn['state'] = DISABLED
            v_price_lbl.set("Totaal prijs tickets €{0}".format((v2 * 7) + (v1 * 10)))

    def callback_update(event):
        active = movies_list.get(ACTIVE)
        try:
            details_list.delete(0, END)
        except:
            pass
        finally:
            i = 1
            for d in details:
                if d[0].__str__() == active.__str__():
                    s = '3D-' if  d[2] == 1 else ''
                    time = d[4].__str__().split(' ')[-1][:-3]
                    s += 'Timing '+ time + ' Tickets : '+d[3].__str__()
                    details_list.insert(i, s)
                    i += 1

    def insert_reservaion():
        _movie_name = movies_list.get(ACTIVE)
        _id = ''
        for d in details:
            if d[0].__str__() == _movie_name:
                _id = d[-1]
        price = (int(adult_spin.get()) * 10) + (int(kid_spin.get()) * 7)
        sql = "INSERT INTO reservations (canceled, ticketPaid, kids, price, adults, movie_id)"
        sql += "VALUES (0, {4}, {0}, {1}, {2}, {3})".format(kid_spin.get(), price, adult_spin.get(), _id, int(kid_spin.get()) + int(adult_spin.get()))

        cur = conn.cursor()
        try:
            cur.execute(sql)
            conn.commit()
        except:
            print('Fout bij het invoegen van rij')
    details = get_movies(conn)
    top = Tk()
    top.winfo_toplevel().title('Cinémax')
    # top.configure(bg='blue')

    # top.geometry("200x250")

    lbl = Label(top, text="Cinémax")

    movies_list = Listbox(top)
    for idx, r in enumerate(details):
        movies_list.insert(idx+1, r[0])

    details_list = Listbox(top)

    adult_lbl = Label(top, text="Volwassen aantal:     ")
    kid_lbl = Label(top,   text="Kinderen aantal:       ")

    kid_spin = Spinbox(top, from_= 0, to = 25, width=4)
    adult_spin = Spinbox(top, from_= 0, to = 25, width=4)

    v_price_lbl = StringVar()
    v_price_lbl.set("Totaal prijs tickets €{0}".format((int(kid_spin.get())*7)+(int(adult_spin.get())*10)))
    price_lbl = Label(top, textvariable=v_price_lbl)
    btn = Button(top, text="Boek Ticket", command=insert_reservaion)
    btn['state'] = DISABLED
    movies_list.grid(column=1, row=2, rowspan=6, sticky='NS')
    details_list.grid(column=2, row=3, columnspan=2, sticky='EW')
    adult_lbl.grid(column=2, row=4)
    kid_lbl.grid(column=2, row=5)
    adult_spin.grid(column=3, row=4)
    kid_spin.grid(column=3, row=5)
    price_lbl.grid(column=2, row=6, columnspan=2, sticky='EW')
    btn.grid(column=2, row=7, columnspan=2, sticky='EW')

    adult_spin.bind("<Button-1>", check_btn1)
    kid_spin.bind("<Button-1>", check_btn2)
    details_list.bind("<<ListboxSelect>>")
    movies_list.bind("<<ListboxSelect>>", callback_update)
    lbl.grid(row=1, column=1, columnspan=3)

    top.mainloop()


if __name__ == '__main__':
    db_file = 'cinemax.db'
    conn = create_connection(db_file)
    if conn is not None:
        main(conn)
