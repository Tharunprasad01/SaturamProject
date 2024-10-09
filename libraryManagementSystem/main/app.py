from flask import Flask,request,jsonify,render_template
import sqlite3

app = Flask(__name__)
def connectDb():
    conn = sqlite3.connect("library.db")
    return conn

@app.route('/')
def readAllData():
    a = connectDb()
    c = a.cursor()
    exec=c.execute('Select * from Books').fetchall()
    for i in exec:
        print(i)
    c.close()
    return jsonify(exec)

@app.route('/<int:id>',methods=['GET'])
def readBookDetailsById(id):
    a=connectDb()
    c=a.cursor()
    exec=c.execute(f"select * from books where id = {id}").fetchall()
    c.close()
    return jsonify(exec)

@app.route('/',methods=['GET'])
def readBookDetailsQueryParameter():
    a = connectDb()
    c = a.cursor()
    id=request.args.get("Id")
    title = request.args.get("Title")
    availablity = request.args.get("Availablity")
    queryVar = "Select * from books where 1=1 "
    filterList = []
    if id:
        queryVar+="and Id=?"
        filterList.append(id)
    if title:
        queryVar+="and Title=?"
        filterList.append(title)
    if availablity:
        queryVar+="and Availablity=?"
        filterList.append(availablity)
    execute=c.execute(queryVar,filterList).fetchall()
    a.close()
    return jsonify(execute)

@app.route('/',methods=['POST'])
def insertNewData():
    a = connectDb()
    c = a.cursor()

    id = request.json.get("Id")
    title = request.json.get("Title")
    genre = request.json.get("Genre")
    author = request.json.get("Author")
    year = request.json.get("Year")
    availablity = request.json.get("Availablity")

    c.execute("insert into Books (id,title,genre,author,year,availablity)values(?,?,?,?,?,?)",(id,title,genre,author,year,availablity))
    a.commit()
    a.close()
    return jsonify({"message":"Book Details Updated Sucessfully"}),201

@app.route('/',methods=['PUT'])
def updateData():
    a=connectDb()
    c=a.cursor()

    id = request.json.get("Id")
    title = request.json.get("Title")
    genre = request.json.get("Genre")
    author = request.json.get("Author")
    year = request.json.get("Year")
    availablity = request.json.get("Availablity")

    c.execute("update books set title = ?,genre = ? ,author = ?,year = ?,availablity = ? where id = ?",(title,genre,author,year,availablity,id))
    a.commit()
    a.close()
    return jsonify({"Message":"Details Updated Successfully"}),200

@app.route('/<int:id>',methods=['Delete'])
def deleteData(id):
    a=connectDb()
    c=a.cursor()
    c.execute("Delete from books where id=?",(id,))
    a.commit()
    a.close()
    return jsonify({"Message":"Book Details Deleted Successfully"})

if __name__=='__main__':
    app.run(debug=True,port=5000)