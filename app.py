from flask import Flask, request, render_template
from flask_cors import CORS
import requests
import random
import mysql.connector
import json
import uuid


app = Flask(__name__)
CORS(app)

with open('configs/configs.json') as json_data:
    jsonInfo = json.load(json_data)
    host = jsonInfo.get("SQLDatabase").get("host")
    user = jsonInfo.get("SQLDatabase").get("user")
    password = jsonInfo.get("SQLDatabase").get("password")

# @app.route('/')
# def microservice():
#     return render_template('index.html')

def connectToData():
    mydb = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database="sql9261031"
    )
    return mydb

def deleteAllQuestions():
    mydb = connectToData()
    mycursor = mydb.cursor()
    mycursor.execute("DELETE FROM questions")
    mydb.commit()  # required to save changes to the table
    return


@app.route('/questionData', methods=['POST'])
def addToData():
    print("method is running")
    print(request.json)
    if request.json and request.json.get("question"):
        r = request.json
        question = r.get("question")
        ("question is here")
    else:
        return "No question sent"
    print(r)
    print(question)
    mydb = connectToData()
    mycursor = mydb.cursor()
    sqlFormula = "INSERT INTO questions (question, id) VALUES (%s, %s)"
    id = str(uuid.uuid4())
    print(id)
    entryTuple = (question, id)
    mycursor.execute(sqlFormula, entryTuple)  # add formula using given data
    mydb.commit()  # required to save changes to the table

    # mycursor.execute("CREATE DATABASE testdb")
    # mycursor.execute("SHOW DATABASES")
    # for db in mycursor:
    #      print(db)
    # mycursor.execute("SHOW TABLES")
    # for tb in mycursor:
    #     print(tb)
    # mycursor.execute("CREATE TABLE questions (question VARCHAR(500), id INTEGER(20))")

    #student1 = ("Rachel", 22)
    #mycursor.execute(sqlFormula, student1)  # add formula using given data
    #mydb.commit()  # required to save changes to the table

    return "complete"


@app.route('/questionData', methods=['GET'])
def returnData():
    questionDict = {}
    questionDict["questions"] = []
    mydb = connectToData()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM questions")
    myresult = mycursor.fetchall()
    for q in myresult:
        qDict = {}
        print(q)
        qDict[q[1]] = q[0]
        questionDict["questions"].append(qDict)
    questionJSON = json.dumps(questionDict)
    return questionJSON



@app.route("/")
def hello():
    return "Hello World!"






if __name__ == "__main__":
    #deleteAllQuestions()
    app.run()
