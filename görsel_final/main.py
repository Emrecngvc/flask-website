import sqlite3
from flask import Flask , render_template , request , redirect , url_for



app = Flask(__name__)

data =  []

def veriAl():
    global data
    with sqlite3.connect('urun.db') as con:
        cur = con.cursor()
        cur.execute("select * from tblUrun")
        data = cur.fetchall()
        for i in data:
            print(i)


def veriEkle(title, price):
    with sqlite3.connect('urun.db') as con:
        cur = con.cursor()
        cur.execute("insert into tblUrun (urubtitle, urunprice) values (?, ?)", (title, price))
        con.commit()
        print("Veriler eklendi")


def veriSil(id):
    with sqlite3.connect('urun.db') as con:
        cur = con.cursor()
        cur.execute("delete from tblUrun where id=?", (id))
        con.commit()
        print("Veriler silindi")



def veriGuncelle(id,title, price):
    with sqlite3.connect('urun.db') as con:
        cur = con.cursor()
        cur.execute("update tblUrun  set urubtitle = ?, urunprice = ?   where id = ? ", (title, price,id))
        con.commit()
        print("Veriler güncellendi")

 


@app.route("/index")
def index():
    return render_template("index.html")



@app.route("/sepet")
def sepet():
    print('sepet')
    veriAl()
    return render_template("sepet.html" , veri = data)



@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/urunekle", methods=['GET', 'POST'])
def urunekle():
    if request.method == 'POST':
        urunTitle = request.form['urunTitle']
        urunPrice = request.form['urunPrice']
        veriEkle(urunTitle,urunPrice)
    return render_template("urunekle.html")


@app.route("/urunsil/<string:id>")
def urunsil(id):
    veriSil(id)
    print("silinecek id:", id)

    return redirect(url_for("sepet"))


@app.route("/urunguncelle/<string:id>" ,  methods=['GET', 'POST'])
def urunguncelle(id):
    if request.method == 'GET':
        print("guncellenecek id:", id)
        guncellenecekVeri=[]
        for d in data:
            if str(d[0])==id:
                guncellenecekVeri = list(d)
        return render_template("urunguncelle.html" , veri = guncellenecekVeri)
    else:
        urunID = request.form['urunID'] 
        urunTitle = request.form['urunTitle']
        urunPrice = request.form['urunPrice']
        veriGuncelle(urunID,urunTitle,urunPrice)
        return redirect(url_for("sepet"))
    

@app.route("/urundetay/<string:id>")
def urundetay(id):
    detayVeri=[]
    for d in data:
        if str(d[0])==id:
             detayVeri = list(d)
    return render_template("urundetay.html" , veri = detayVeri)




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)