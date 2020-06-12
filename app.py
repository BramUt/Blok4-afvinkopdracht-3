from flask import Flask, render_template, request
import mysql.connector
db_info = {"user": "anonymous", "host": "ensembldb.ensembl.org", "port": 3306,
           "db": "homo_sapiens_core_91_38"}

app = Flask(__name__)


@app.route('/', methods=["POST", "GET"])
def homepage():
    """Homepagina, haalt descriptions uit de gene tabel met behulp van
    de opgegeven zoekterm.
    """
    # Als er een zoekterm is opgegeven worden resultaten opgehaald uit
    # de database.
    if request.method == "POST":
        print({**request.form})
        # Ophalen van zoekterm.
        search_term = request.form["search_term"]
        conn = mysql.connector.connect(**db_info)
        cursor = conn.cursor()
        cursor.execute(f"select description "
                       f"from gene "
                       f"where description like '%{search_term}%'")
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        # Splits desciption op de zoekterm.*
        try:
            new_results = [i[0].partition(search_term) for i in results]
            return render_template("homepage_afvink3.html",
                                   search_term=search_term,
                                   results=new_results)
        # Exception voor search_term = "".
        except ValueError:
            return render_template("homepage_afvink3.html",
                                   search_term=search_term, results=results)
    # Pagina zonder resultaten op eerste aanvraag.
    else:
        return render_template("homepage_afvink3.html")


if __name__ == '__main__':
    app.run()
