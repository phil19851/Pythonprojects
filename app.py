from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "your_secret_key"
model_categories = ["Category A", "Category B", "Category C"]  # Example categories from the model

# Connect to MySQL database
db = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='admin',
    database='phildb1'
)
cursor = db.cursor()

# Create a table to store claims
create_table_query = """
CREATE TABLE IF NOT EXISTS claims (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ticket_no VARCHAR(50),
    claim_number VARCHAR(50),
    date_of_call DATE,
    description VARCHAR(1000),
    call_category VARCHAR(50)
)
"""
cursor.execute(create_table_query)


@app.route("/", methods=["GET", "POST"])
def login():
    if session.get("logged_in"):
        return redirect("/dashboard")

    if request.method == "POST":
        login_name = request.form["login_name"]
        password = request.form["password"]

        if login_name == "admin" and password == "admin":
            session["logged_in"] = True
            return redirect("/dashboard")
        else:
            error_message = "Invalid login credentials. Please try again."
            return render_template("login.html", error_message=error_message)

    return render_template("login.html")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if not session.get("logged_in"):
        return redirect("/")

    if request.method == "POST":
        ticket_no = request.form["ticket_no"]
        claim_number = request.form["claim_number"]
        date_of_call = request.form["date_of_call"]
        description = request.form["description"]
        call_category = request.form["call_category"]

        # Save the claim details in the database
        insert_query = """
        INSERT INTO claims (ticket_no, claim_number, date_of_call, description, call_category)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (ticket_no, claim_number, date_of_call, description, call_category))
        db.commit()

    return render_template("dashboard.html", categories=model_categories)


@app.route("/get_category", methods=["POST"])
def get_category():
    description = request.json["description"]

    # Apply basic rules to determine the category
    if "refund" in description.lower():
        category = "Category A"
    elif "complaint" in description.lower():
        category = "Category B"
    else:
        category = "Category C"

    return category


if __name__ == "__main__":
    app.run(debug=True)
