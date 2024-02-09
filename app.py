#Import necessary modules from Flask framework
from flask import Flask, render_template,request, url_for, redirect, session
import re
import mysql.connector
import hashlib
import random
# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client


#Initialize the Flask Application
app = Flask(__name__)

# Set a secret key for the session
app.secret_key = 'This is my secret key for opinionhive app'

#Database connection configuration
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='heartattack2023',
        database='opiniohive'
    )
    return conn


# Set environment variables for your credentials
account_sid = "AC3896db49c2fe15d42dec509aff93902e"
auth_token = "04e3f304bff8ead73fe8e5169cad97b0"
verify_sid = "VA0c28c79be60fb0fae46b6eba42e96c21"
client = Client(account_sid, auth_token)


def send_verification_code(phone_number):
    verification = client.verify.v2.services(verify_sid) \
        .verifications \
        .create(to=phone_number, channel="sms")
    session['verification_sid'] = verification.sid
    session['phone_number'] = phone_number

    
@app.route("/verify_code", methods=["POST"])
def verify_code():
    verification_sid = session["verification_sid"]
    if verification_sid:
        code = request.form["verification_code"]
        verification_check = client.verify.v2.services(verify_sid) \
            .verification_checks \
            .create(to=session["phone_number"], code=code)
        if verification_check.status == "approved":
            db = get_db_connection()
            cursor = db.cursor()
            user_id = session['user_id']
            cursor.execute("UPDATE users SET phone_verified=1 WHERE id=%s", (user_id,))
            db.commit()
            success = "Phone number verified!"
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid code. Please try again."
            return render_template('verify_popup.html', error=error)
    else:
        return redirect(url_for("dashboard"))


#Defining routes

#Route to serve static files- css files and images
@app.route('/static/<path:filename>')
def static_files(filename):
    return app.send_static_file(filename)

#Main page route
@app.route("/", methods=["Get"])
def home():

    return render_template("home.html")


# Registration route
@app.route("/register", methods=["GET", "POST"])
def register():
    db = get_db_connection()

    if request.method == "POST":
        email = request.form["email"]
        phone_number = request.form["phone_number"]
        # Server-side validation for US phone number format
        if not is_valid_us_phone_number(phone_number):
            error = "Invalid phone number format. Please use the format xxx-xxx-xxxx."
            return render_template("signup.html", error=error)
        
        phone_number = "".join(char for char in phone_number if char.isdigit())
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        # Extract first and last name from the form
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        full_name = f"{first_name} {last_name}"

        # Check if the user with the given email already exists
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            error = "User with this email already exists"
            return render_template("signup.html", error=error)

        #Checks if passwords match
        if password == confirm_password:

            is_valid, message = is_valid_password(password)

            #Check if password is valid
            if is_valid:
                # Hash the password before storing it
                hashed_password = hash_password(password)
                cursor.execute("INSERT INTO users (name, email, phone_number, password) VALUES (%s, %s, %s, %s)", (full_name, email, phone_number, hashed_password))
                db.commit()

                # Get the user's ID
                cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
                user_id = cursor.fetchone()[0]

                # Insert into wallet table with a balance of 0
                cursor.execute("INSERT INTO wallet (user_id, balance) VALUES (%s, %s)", (user_id, 0))
                db.commit()

                success = "Registration was successful!"
                return render_template('login.html', success=success)
            else:
                return render_template('signup.html', error=message)
        
        else:
            error = "Password doesn't match"
            return render_template("signup.html", error=error)

    return render_template("signup.html")

#Phone number entered is usa's
def is_valid_us_phone_number(phone_number):
    # Regular expression for US phone number format xxx-xxx-xxxx
    pattern = re.compile(r'^\d{3}-\d{3}-\d{4}$')
    return pattern.match(phone_number) is not None


def is_valid_password(password):
    # Check minimum length
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."

    # Check for uppercase and lowercase letters
    if not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password):
        return False, "Password must contain both uppercase and lowercase letters."

    # Check for digits
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit."

    # Check for special characters
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character."

    # Check for no spaces
    if ' ' in password:
        return False, "Password must not contain spaces."

    # All checks passed
    return True, "Password is valid."



# Hashing function
def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

#Function to check if user has verified phone_number
def verify_phone_number():
    if 'user_id' in session:
        db = get_db_connection()
        cursor = db.cursor()
        user_id = session['user_id']
        # Query to get user info
        cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
        user = cursor.fetchone()
        return user[8]

    else:
        error="User not logged in"
        return render_template('login.html', error=error)

#Login Route
@app.route("/login", methods=["GET", "POST"])
def login():
    db = get_db_connection()

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        if user and hash_password(password) == user[4]:
            session["user_id"] = user[0]  # Store user ID in session for authentication
            return redirect(url_for("dashboard"))  # Replace "dashboard" with your desired redirect path
        else:
            error = "Invalid email or password"
            return render_template("login.html", error=error)
        
        
    return render_template("login.html")

# Define a route for deleting the user account
@app.route('/delete_account', methods=['GET', 'POST'])
def delete_account():
    if 'user_id' in session:
        db = get_db_connection()
        cursor = db.cursor()
        user_id = session['user_id']

        if request.method == 'POST':

            # Delete wallet data
            delete_wallet_query = "DELETE FROM wallet WHERE user_id = %s"
            cursor.execute(delete_wallet_query, (user_id,))
            db.commit()

            # Delete wallet data
            delete_chats_query = "DELETE FROM chat WHERE user_id = %s"
            cursor.execute(delete_chats_query, (user_id,))
            db.commit()

            # Delete survey data
            delete_survey_query = "DELETE FROM surveys WHERE user_id = %s"
            cursor.execute(delete_survey_query, (user_id,))
            db.commit()

            # Delete payout data
            delete_payout_query = "DELETE FROM payouts WHERE user_id = %s"
            cursor.execute(delete_payout_query, (user_id,))
            db.commit()

            # Delete the user from the 'users' table
            delete_user_query = "DELETE FROM users WHERE id = %s"
            cursor.execute(delete_user_query, (user_id,))
            db.commit()

            return redirect(url_for('register'))

        # Fetch user details for confirmation
        select_user_query = "SELECT * FROM users WHERE id = %s"
        cursor.execute(select_user_query, (user_id,))
        user = cursor.fetchone()

        return render_template('delete_account.html', user=user)



    else:
        error="User not logged in"
        return render_template('login.html', error=error)
    

#Route to change password
@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    
    if 'user_id' in session:
        db = get_db_connection()
        user_id = session['user_id']

        if request.method == 'POST':
            current_password = request.form.get('current_password')
            new_password = request.form.get('new_password')
            confirm_new_password = request.form.get('confirm_new_password')

             #Checks if passwords match
            if new_password == confirm_new_password:
                #Check if password meets password requirements
                is_valid, message = is_valid_password(new_password)

                #Check if password is valid
                if is_valid:
                    # Fetch user details
                    cursor = db.cursor()
                    cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
                    user = cursor.fetchone()

                    # Check if the entered current password matches the stored password
                    if hash_password(current_password) == user[4]:
                        # Update password if the current password matches
                        hashed_password = hash_password(new_password)
                        cursor=db.cursor()
                        cursor.execute("UPDATE users SET password = %s WHERE id = %s", (hashed_password, user_id))
                        db.commit()
                        success = "Password changed successfully!"
                        return render_template('change_password.html', error=success)
                    else:
                        error = "Current password is incorrect. Please try again."
                        return render_template("change_password.html", error=error)
                else:
                    return render_template('change_password.html', error=message)
            
            else:
                error = "Password doesn't match"
                return render_template("change_password.html", error=error)

        return render_template('change_password.html')

    else:
        error = "user not logged in"
        return render_template('login.html', error=error)
  
# Route to change email
@app.route('/change_email', methods=['GET', 'POST'])
def change_email():
    if 'user_id' in session:
        db = get_db_connection()
        user_id = session['user_id']

        if request.method == 'POST':
            new_email = request.form.get('new_email')

            cursor=db.cursor()
            cursor.execute("UPDATE users SET email = %s WHERE id = %s",(new_email, user_id))
            db.commit()
            success= 'Email updated successfully!'
            return render_template('change_email.html', error=success)

            
        else:
            return render_template('change_email.html')

    else:
        error ="User not logged in!"
        return render_template("login.html", error=error)
    

#Dashboard route
@app.route("/dashboard")
def dashboard():
    if "user_id" in session:
        #DB Connection
        db = get_db_connection()
        user_id = session['user_id']

        #get users data
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
        user = cursor.fetchone()

        # Checks if user has verified their phone number
        has_user_verified_their_phone = verify_phone_number()
        if not has_user_verified_their_phone:
            user=user
            phone_number=user[3]
            send_verification_code(phone_number)
            return render_template('verify_popup.html', user=user)

        # Assuming user_id is the user ID you want to get the survey count for
        cursor.execute("SELECT COUNT(*) FROM surveys WHERE user_id = %s", (user_id,))
        survey_count = cursor.fetchone()[0]

        if survey_count > 0:
            average_satisfaction = random.randint(80, 85)

            return render_template('dashboard.html', user=user, survey_count=survey_count,average_satisfaction=average_satisfaction )
        else:
            return render_template('dashboard.html', user=user, survey_count=survey_count)
    
    else:
        error ="User not logged in!"
        return render_template("login.html", error=error)

# Logout route
@app.route("/logout")
def logout():
    # Clear the user's session
    session.clear()
    return redirect(url_for("login"))

# Route for user profile
@app.route('/profile', methods=['GET'])
def profile():
    if 'user_id' in session:
        db = get_db_connection()
        user_id = session['user_id']

        # Fetch user data by user_id
        cursor= db.cursor()
        cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
        user = cursor.fetchone()


        return render_template('profile.html', user=user)

    else:
        error ="User not logged in!"
        return render_template("login.html", error=error)
# Flask route for handling survey form submission
@app.route('/survey', methods=['GET','POST'])
def submit_survey():
    if request.method == 'POST':
        if "user_id" in session:
            #Getting user id
            user_id = session["user_id"]
            # Retrieve form data
            gender = request.form['gender']
            age = request.form['age']
            shopping_frequency = request.form['shopping_frequency']
            preferred_website = request.form['preferred_website']
            satisfaction = request.form['satisfaction']
            influence_factors = request.form['influence_factors']
            preferred_website_again = request.form['preferred_website_again']
            improvements_features = request.form['improvements_features']

            #Get DB connection
            db = get_db_connection()
            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO surveys 
                (user_id, gender, age, shopping_frequency, preferred_website, satisfaction, 
                influence_factors, preferred_website_again, improvements_features)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (user_id, gender, age, shopping_frequency, preferred_website, satisfaction, 
                influence_factors, preferred_website_again, improvements_features))

            db.commit()

            return redirect(url_for('dashboard')) 
        else:
            error ="User not logged in!"
            return render_template("login.html", error=error)

    return render_template("survey.html")

#Route to veryfy phone
@app.route('/verify_phone', methods=['POST', 'GET'])
def verify_phone():
    if "user_id" in session:
        # Getting user id
        user_id = session["user_id"]
        # Database connection
        conn = get_db_connection()
        cursor = conn.cursor()

        # Query to get user info
        cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
        user = cursor.fetchone()

        if request.method == 'POST':
            cursor.execute("UPDATE users SET request_verification = 1 WHERE id = %s", (user_id,))
            conn.commit()
            success = "A verification link will be sent to your phone number"


            return render_template('verify_phone.html', success=success, user=user)

        else:
            return render_template('verify_phone.html', user=user)
    
    else:
        error = "User not logged in!"
        return render_template("login.html", error=error)
    
# Route to get user wallet details
@app.route("/wallet", methods=["GET", "POST"])
def wallet():
    if "user_id" in session:
        # Getting user id
        user_id = session["user_id"]
        # Database connection
        conn = get_db_connection()
        cursor = conn.cursor()

        # Query to get user info
        cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
        user = cursor.fetchone()

        # Query to get wallet information
        cursor.execute("SELECT * FROM wallet WHERE user_id = %s", (user_id,))
        wallet_info = cursor.fetchone()

        # Check if the balance is above $15 for the "Request Payout" button
        request_payout_button = False
        if wallet_info and wallet_info[2] >= 15:
            request_payout_button = True

        conn.close()

        if wallet_info:
            # Pass wallet information to HTML template
            return render_template("wallet.html", wallet_info=wallet_info, request_payout_button=request_payout_button, user=user)
        else:
            error = "Wallet information not found."
            return render_template("wallet.html", error=error)

    else:
        error = "User not logged in!"
        return render_template("login.html", error=error)

# Route to handle payout request
@app.route("/request_payout", methods=["POST", "GET"])
def request_payout():
    if "user_id" in session:
        # Getting user id
        user_id = session["user_id"]
        # Database connection
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the user has already submitted a payout request
        cursor.execute("SELECT * FROM payouts WHERE user_id = %s", (user_id,))
        existing_payout = cursor.fetchone()

        if existing_payout:
            # If a payout request already exists, show an error message
            conn.close()
            error = "You have already submitted a payout request. Please wait for processing."
            return redirect(url_for("wallet", error=error))

        # Insert payout request into the payouts table
        cursor.execute("INSERT INTO payouts (user_id) VALUES (%s)", (user_id,))
        conn.commit()

        conn.close()

        success = "Payout request submitted successfully!"
        return redirect(url_for("wallet", success=success))

    else:
        error = "User not logged in!"
        return render_template("login.html", error=error)


# Admin login page
# Login Route
@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    db = get_db_connection()

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        cursor = db.cursor()
        cursor.execute("SELECT * FROM admin WHERE email=%s", (email,))
        admin = cursor.fetchone()

        if admin and password == admin[3]:
            session["admin_id"] = admin[0]  # Store admin ID in session for authentication
            return redirect(url_for("admin_dashboard"))
        else:
            error = "Invalid email or password"
            return render_template("admin_login.html", error=error)

    return render_template("admin_login.html")
# Logout route
@app.route("/admin_logout")
def admin_logout():
    # Clear the admins's session
    session.clear()
    return redirect(url_for("admin_login"))


# Admin dashboard
@app.route("/admin_dashboard", methods=["GET"])
def admin_dashboard():
    if "admin_id" in session:
        # Retrieve admin data based on the admin_id stored in the session
        admin_id = session["admin_id"]
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM admin WHERE id=%s", (admin_id,))
        admin = cursor.fetchone()


        if admin:
            # Fetch all users data
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            return render_template('admin_dashboard.html', admin=admin, users=users)
        else:
            return redirect(url_for("admin_login"))
    else:
        error ="Admin not logged in!"
        return render_template("admin_login.html", error=error)
    

# Route for admin to verify phone and credit users wallet
@app.route("/verify_user/<int:user_id>", methods=["GET", "POST"])
def verify_user(user_id):
    if "admin_id" in session:
        if request.method == "POST":
            # Update the user's is_phone_verified status to 1 (verified)
            conn = get_db_connection()
            cursor = conn.cursor()
            update_query = "UPDATE users SET is_phone_verified = 1 WHERE id = %s"
            cursor.execute(update_query, (user_id,))
            conn.commit()

            #Update wallet
            credit_wallet_query = "UPDATE wallet SET balance = 15 WHERE user_id = %s"
            cursor.execute(credit_wallet_query, (user_id,))
            conn.commit()
            conn.close()

            return redirect(url_for("admin_dashboard"))
        
        else:
            return redirect(url_for("admin_dashboard"))
        
    else:
        # Redirect to the admin login page if not logged in
        error ="Admin not logged in!"
        return render_template("admin_login.html", error=error)


    
# Admin mark as sent verification link
@app.route("/admin/user/<int:user_id>", methods=["GET"])
def view_user_details(user_id):
    if "admin_id" in session:
        # Retrieve admin data based on the admin_id stored in the session
        admin_id = session["admin_id"]
        db = get_db_connection()
        cursor = db.cursor()

        # Fetch user data by user_id
        cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
        user = cursor.fetchone()

        if user:
            return render_template('user_details.html', admin_id=admin_id, user=user)
        else:
            # Handle the case where the user is not found
            return render_template('user_details.html', admin_id=admin_id, user=None)
    else:
        # Redirect to the admin login page if not logged in
        error ="Admin not logged in!"
        return render_template("admin_login.html", error=error)

# Route to view payout requests (accessible only to admins)
@app.route("/admin/view_payouts", methods=["GET"])
def view_payouts():

    if "admin_id" in session:
        # Database connection
        conn = get_db_connection()
        cursor = conn.cursor()

        # Query to get all payout requests
        # Execute SQL query to join payouts and users tables
        cursor.execute("""
            SELECT payouts.id AS payout_id, users.id AS user_id, users.name, payouts.request_date, payouts.paid
            FROM payouts
            JOIN users ON payouts.user_id = users.id;
        """)
        payouts = cursor.fetchall()


        conn.close()

        # Render the template with payout information
        return render_template("payout_requests.html", payouts=payouts)

    else:
        # Redirect to the admin login page if not logged in
        error ="Admin not logged in!"
        return render_template("admin_login.html", error=error)

# Route to mark payouts as paid
@app.route("/admin_pay_users/<int:payout_id>/<int:user_id>", methods=["POST"])
def admin_pay_users(payout_id, user_id):
    if request.method == "POST":
        # Database connection
        conn = get_db_connection()
        cursor = conn.cursor()

        # Update the 'paid' column in the payouts table
        cursor.execute("UPDATE payouts SET paid = 'YES' WHERE id = %s", (payout_id,))
        conn.commit()

        #Update amount to 0 in the user wallet table
        cursor.execute("UPDATE wallet set balance= 0 where user_id = %s", (user_id,))
        conn.commit()

        conn.close()

    # Redirect back to the admin payouts page
    return redirect(url_for("view_payouts"))

#FAQ route
@app.route("/FAQ", methods=["Get"])
def FAQ():

    return render_template("FAQ.html")

#Aboute Opiniohive route
@app.route("/about", methods=["Get"])
def about():

    return render_template("about_us.html")

# Route for 404 page
@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('show_404'))

# Route to render the 404.html template
@app.route('/404')
def show_404():
    return render_template('404.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)