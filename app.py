from flask import Flask, render_template
from flask_mysqldb import MySQL


import scraper

app = Flask(__name__)

# DEFINE THE DATABASE CREDENTIALS
app.config['MYSQL_HOST'] = 'pi4-kb'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = '5436'
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.config["MYSQL_CHARSET"] = "utf8mb4"

mysql = MySQL(app)


def fill_db(data, store_id):
    with app.app_context():
        cur = mysql.connection.cursor()
        store = list(data.values())[0][2]
        store_name = store.split('.')[0]
        cur.execute("INSERT INTO   keydeals.store (storeId,name,link,icon) VALUES (%s,%s,%s,'')",
                    (store_id, store_name, 'https://www.' + store))

        cur.execute("SELECT appId FROM keydeals.app")
        appids = map(lambda x: x['appId'], cur.fetchall())

        for key, val in data.items():
            store = val[2]
            store_name = store.split('.')[0]
            game_link = val[3]
            title = repr(val[0])
            price = val[1]

            cur.execute("SELECT name FROM keydeals.store WHERE name LIKE %s", (store_name,))
            row = cur.fetchone()
            if row is None:
                store_id += 1
                cur.execute("INSERT INTO   keydeals.store (storeId,name,link,icon) VALUES (%s,%s,%s,'')",
                            (store_id, store_name, 'https://www.' + store))

            if int(key) not in appids:
                try:
                    cur.execute("INSERT INTO   keydeals.app (appId,name) VALUES (%s,%s)", (int(key), title))
                except Exception as e:
                    print(e)
            try:
                cur.execute("INSERT INTO   keydeals.catalogue (price,appId,storeId,link) VALUES (%s,%s,%s,%s)",
                            (float(price), int(key), store_id, game_link))
            except Exception as e:
                print(e)

        mysql.connection.commit()
        cur.close()


@app.cli.command()
def schedule():
    """Run scheduled scraping job."""
    print('Scraping sites...')
    sites = ['plati', 'g2a', 'humble', 'cheapkeys']
    for i, site in enumerate(sites):
        print(site)
        result = scraper.get_data(site)
        fill_db(result, i)

    print('Done!')


def fetch_catalogue():
    cur = mysql.connection.cursor()
    cur.execute(
        '''SELECT a.name, a.appId, c.price, s.name as store 
        FROM keydeals.catalogue c JOIN    keydeals.app a ON c.appId = a.appId JOIN keydeals.store s ON c.storeId = s.storeId;''')
    result = cur.fetchall()
    cur.close()
    return result


@app.route('/index')
@app.route('/')
def index():
    rv = fetch_catalogue()
    return render_template(f"db_table.html", db=rv)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
