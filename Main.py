import tkinter as tk
import mysql.connector
from mysql.connector import errorcode


user = 'root'
password = 'whc970330'
host = '127.0.0.1'
database = 'covid19'


class Application(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        root.geometry('700x400')
        root.title('CS480 Final Project')

        self.grid_columnconfigure(0, weight=1)

        # create frames
        self.frame_mainpage = tk.Frame(root)
        self.frame_query = tk.Frame(root)
        self.frame_query2 = tk.Frame(root)
        frames = [self.frame_mainpage, self.frame_query, self.frame_query2]
        for frame in frames:
            frame.grid(row=0, column=0, sticky='news')

        self.create_frame_mainpage(self.frame_mainpage)
        self.raise_frame(self.frame_mainpage)

    def create_frame_mainpage(self, frame):
        print('create frame mainpage')
        title = tk.Label(frame, text='COVID-19 Database', font=30)
        title.grid(row=0, column=0, pady=20)

        query_btn = tk.Button(frame, text='Show Database (first 15 line)', width=100, command=lambda: self.query())
        query_btn.grid(row=1, column=0, pady=5, padx=10)

        query_btn2 = tk.Button(frame, text='Country has confirmed cases more than one million', width=100,
                               command=lambda: self.query2(
                                   "select `Country/Region`, Confirmed from covid19 "
                                   "where Confirmed > 1000000 "
                                   "order by Confirmed",
                                   ('Country', 'Confirmed')))
        query_btn2.grid(row=2, column=0, pady=5, padx=10)

        query_btn3 = tk.Button(frame, text='Country has more than 100,000 deaths', width=100,
                               command=lambda: self.query2(
                                   'select `Country/Region`, Deaths from covid19 '
                                   'where Deaths > 100000',
                                   ('Country', 'Deaths')))
        query_btn3.grid(row=3, column=0, pady=5, padx=10)

        query_btn4 = tk.Button(frame, text='Country has death rate more than 1', width=100,
                               command=lambda: self.query2(
                                   'select `Country/Region`, `Deaths / 100 Cases` from covid19 '
                                   'where `Deaths / 100 Cases` > 1 '
                                   'order by `Deaths / 100 Cases` DESC',
                                   ('Country', 'Death Rate')))
        query_btn4.grid(row=4, column=0, pady=5, padx=10)

        query_btn5 = tk.Button(frame, text='Country has less than 1,000 deaths', width=100,
                               command=lambda: self.query2(
                                   'select `Country/Region`, Deaths from covid19 '
                                   'where Deaths < 1000 '
                                   'order by Deaths DESC',
                                   ('Country', 'Deaths')))
        query_btn5.grid(row=5, column=0, pady=5, padx=10)

        query_btn6 = tk.Button(frame, text='Country has confirmed cases less than 1,000 and less than 1,000 deaths',
                               width=100,
                               command=lambda: self.query2(
                                   'select `Country/Region`, Confirmed, Deaths from covid19 '
                                   'where Deaths < 1000 and Confirmed < 1000 '
                                   'order by Confirmed DESC',
                                   ('Country', 'Confirmed', 'Deaths')))
        query_btn6.grid(row=6, column=0, pady=5, padx=10)

        self.frame_mainpage.grid_columnconfigure(0, weight=1)

    def query(self):
        print('query_btn pressed')
        # create query frame
        self.create_frame_query(self.frame_query)
        self.raise_frame(self.frame_query)

    def query2(self, sql_command, table_header):
        print('query_btn2 pressed')
        # create query frame
        self.create_frame_query2(self.frame_query2, sql_command, table_header)
        self.raise_frame(self.frame_query2)

    def create_frame_query(self, frame):
        print('create frame_query')
        back_btn = tk.Button(frame, text="back", command=lambda: self.raise_frame(self.frame_mainpage))
        back_btn.grid(row=0, column=0, pady=10, sticky='nw')

        # init database connection
        try:
            cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
                return
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
                return
            else:
                print(err)
                return

        c = cnx.cursor()
        c.execute('SELECT * FROM covid19 ORDER BY Confirmed DESC')
        records = c.fetchmany(15)
        cnx.close()
        header = ('Country', 'Confirmed', 'Deaths', 'Recovered', 'Deaths / 100 Cases', 'Recovered / 100 Cases',
                  'Deaths / 100 Recovered')
        records.insert(0, header)
        print(records[1])

        widgets = {}
        row = 1
        for country, confirmed, deaths, recovered, death_rate, recovered_rate, death_recovered in records:
            row += 1
            widgets['table'] = {
                "country": tk.Label(self.frame_query, text=country, borderwidth=1, relief="ridge"),
                "confirmed": tk.Label(self.frame_query, text=confirmed, borderwidth=1, relief="ridge"),
                "deaths": tk.Label(self.frame_query, text=deaths, borderwidth=1, relief="ridge"),
                "recovered": tk.Label(self.frame_query, text=recovered, borderwidth=1, relief="ridge"),
                "death_rate": tk.Label(self.frame_query, text=death_rate, borderwidth=1, relief="ridge"),
                "recovered_rate": tk.Label(self.frame_query, text=recovered_rate, borderwidth=1, relief="ridge"),
                "death_recovered": tk.Label(self.frame_query, text=death_recovered, borderwidth=1, relief="ridge")
            }

            widgets['table']["country"].grid(row=row, column=0, sticky="nsew")
            widgets['table']["confirmed"].grid(row=row, column=1, sticky="nsew")
            widgets['table']["deaths"].grid(row=row, column=2, sticky="nsew")
            widgets['table']["recovered"].grid(row=row, column=3, sticky="nsew")
            widgets['table']["death_rate"].grid(row=row, column=4, sticky="nsew")
            widgets['table']["recovered_rate"].grid(row=row, column=5, sticky="nsew")
            widgets['table']["death_recovered"].grid(row=row, column=6, sticky="nsew")
        self.frame_query.grid_columnconfigure([0, 1, 2, 3, 4, 5, 6], weight=1)

    def create_frame_query2(self, frame, sql_command, table_header):
        print('create frame_query2')
        print(sql_command)
        back_btn = tk.Button(frame, text="back", command=lambda: self.raise_frame(self.frame_mainpage))
        back_btn.grid(row=0, column=0, pady=10, sticky='nw')

        # init database connection
        try:
            cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
                return
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
                return
            else:
                print(err)
                return

        c = cnx.cursor()
        c.execute(sql_command)
        records = c.fetchmany(15)
        cnx.close()
        # header = ('Country', 'Confirmed')
        records.insert(0, table_header)

        widgets = {}
        row = 1
        for record in records:
            row += 1
            for i in range(len(record)):
                widgets['table'] = {
                    table_header[i]: tk.Label(self.frame_query2, text=record[i], borderwidth=1, relief="ridge")
                }

                widgets['table'][table_header[i]].grid(row=row, column=i, sticky="nsew")
        self.frame_query2.grid_columnconfigure(list(range(0, len(table_header))), weight=1)

    @staticmethod
    def raise_frame(frame):
        frame.tkraise()


if __name__ == "__main__":
    root = tk.Tk()
    Application(root).grid(sticky="nsew")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.mainloop()
