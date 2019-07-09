from flask import Flask, redirect, request, session, render_template
import os
from mysqlconnection import connectToMySQL 

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/")
def index():
    mysql = connectToMySQL('users')	        # call the function, passing in the name of our db
    userz = mysql.query_db('SELECT * FROM user_table;')  # call the query_db function, pass in the query as a string
    return render_template("index.html", all_userz = userz)

# SHOW
@app.route("/add_user")
def showuser():
    return render_template("/add_user.html")

# CREATE
@app.route("/create_user", methods=["POST"])
def add_pet_to_db():
    # QUERY: INSERT INTO first_flask (first_name, last_name, occupation, created_at, updated_at) 
    #                         VALUES (fname from form, lname from form, occupation from form, NOW(), NOW());
    mysql = connectToMySQL('users')

    query = "INSERT INTO user_table (first_name, last_name, email, created_at, updated_at) VALUES (%(fn)s, %(ln)s, %(em)s, NOW(), NOW());"

    data = {
        "fn": request.form["fname"],
        "ln": request.form["lname"],
        "em": request.form["mail"]
    }

    print(data['fn'])
    
    new_user_id = mysql.query_db(query, data)
    return redirect("/") 

@app.route("/user/<id>")
def show_user(id):
    user_id = int(id)
    mysql = connectToMySQL('users')

    query = "SELECT * FROM user_table WHERE id = {}".format(user_id);
    new_user_info = mysql.query_db(query)
    print(new_user_info)
    
    return render_template("/read_users.html", user_info = new_user_info)

@app.route("/edit/<id>")
def edit_user(id):
    user_id = int(id)
    mysql = connectToMySQL('users')

    query = "SELECT * FROM user_table WHERE id = {}".format(user_id);
    new_user_info = mysql.query_db(query)
    print(new_user_info)
    
    return render_template("/update_user.html", user_info = new_user_info)

@app.route("/delete/<id>")
def delete_user(id):
    user_id = int(id)
    mysql = connectToMySQL('users')
    query = "DELETE FROM user_table WHERE id = {}".format(user_id);
    new_user_info = mysql.query_db(query)
    return redirect('/')

@app.route("/update_user/<id>", methods = ["POST"])
def update_user(id):
    user_id = int(id)
    mysql = connectToMySQL('users')

    query = "UPDATE user_table SET first_name = %(fn)s, last_name = %(ln)s, email = %(em)s WHERE id = %(id)s;"

    data = {
        "fn": request.form["fname"],
        "ln": request.form["lname"],
        "em": request.form["mail"],
        "id": user_id
    }

    new_user_info = mysql.query_db(query, data)
    print(query)
    return redirect('/')





if __name__ == '__main__':
    app.run(debug=True)