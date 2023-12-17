from flask import Flask, jsonify, request
import json
from supabase import create_client, Client
import traceback

app = Flask(__name__)

url="https://iqacemdedaqxepotxlbb.supabase.co"
key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlxYWNlbWRlZGFxeGVwb3R4bGJiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDI0OTI4OTQsImV4cCI6MjAxODA2ODg5NH0.a8KGVvu2jG9gNlWzi03lMNl7oaIjKZVAf0Qpo6WS5Lk"
supabase: Client = create_client(url, key)

@app.route('/users.signup', methods=['POST'])
def api_users_signup():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    error = False

    # Validate name
    if (not name) or (len(name) < 2):
        error = 'Name needs to be valid'

    # Validate email
    if (not error) and ((not email) or (len(email) < 5)):
        error = 'Email needs to be valid'

    # Validate password
    if (not error) and ((not password) or (len(password) < 5)):
        error = 'Provide a valid password'

    # Check if user already exists
    if (not error):
        response = supabase.table('users').select("*").ilike('email', email).execute()
        if len(response.data) > 0:
            error = 'User already exists'

    # If no error, proceed with sign-up
    if (not error):
        response = supabase.table('users').insert({"name": name, "email": email, "password": password}).execute()
        if len(response.data) == 0:
            error = 'Error creating the user'

    if error:
        return json.dumps({'status': 200, 'message': error})

    return json.dumps({'status': 200, 'message': '', 'data': response.data[0]})

@app.route('/users.login', methods=['POST'])
def api_users_login():
    email = request.form.get('email')
    password = request.form.get('password')
    error = False

    if (not email) or (len(email) < 5):
        error = 'Email needs to be valid'
    if (not error) and ((not password) or (len(password) < 5)):
        error = 'Provide a password'

    if (not error):
        response = supabase.table('users').select("*").ilike('email', email).eq('password', password).execute()
        if len(response.data) > 0:
            return json.dumps({'status': 200, 'message': '', 'data': response.data[0]})

    if not error:
        error = 'Invalid Email or password'

    return json.dumps({'status': 500, 'message': error})

@app.route('/users.signup.auth',methods=['GET','POST'])
def api_users_signup_auth():
    email= request.args.get('email')
    password= request.args.get('password')
    response = supabase.auth.sign_up({"email": email, "password": password})        
    print(str(response))    
    return str(response)


@app.route('/users.change_password', methods=['POST'])
def api_users_change_password():
    email = request.form.get('email')
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    error = None

    # Validate email
    if not email or len(email) < 5:  # You can even check with regex
        error = 'Email needs to be valid'

    # Validate current password
    if not error and (not current_password or len(current_password) < 5):
        error = 'Provide a valid current password'

    # Validate new password
    if not error and (not new_password or len(new_password) < 5):
        error = 'Provide a valid new password'

    # Check if user exists and validate current password
    if not error:
        response = supabase.table('users').select("*").ilike('email', email).eq('password', current_password).execute()
        if len(response.get('data', [])) == 0:
            error = 'Invalid current password or user not found'

    # If no error, proceed with password change
    if not error:
        response = supabase.table('users').update({"password": new_password}).ilike('email', email).execute()
        if response.get('error'):
            error = 'Failed to update password'

    if error:
        return jsonify({'status': 500, 'message': error})

    return jsonify({'status': 200, 'message': 'Password updated successfully'})


@app.route('/users.insertGender', methods=['GET', 'POST'])
@app.route('/users.insertGender', methods=['GET', 'POST'])
def api_users_insert_gender():
    email = request.form.get('email')
    gender = request.form.get('gender')
    
    try:
        if not (email and gender):
            return json.dumps({'status': 400, 'message': 'Invalid input'})

        user_response = supabase.table('users').select('id').ilike('email', email).execute()
        user_data = user_response.data

        if not user_data or len(user_data) == 0:
            return json.dumps({'status': 404, 'message': 'User not found'})

        user_id = user_data[0]['id']

        # Check if a row with the given user_id already exists in the users_info table
        result = supabase.table('users_info').select('user_id').eq('user_id', user_id).execute()
        if result.data and len(result.data) > 0:
            return json.dumps({'status': 400, 'message': 'A row with the given user_id already exists'})

        result = supabase.table('users_info').insert({'user_id': user_id, 'gender': gender}).execute()

        if result.error:
            return json.dumps({'status': 500, 'message': f"Internal Server Error, Exception in /users.insertGender: {result.error.message}"})
        else:
            return json.dumps({'status': 200, 'message': 'Gender inserted successfully'})
        
    except Exception as e:
        return json.dumps({'status': 500, 'message': f"Internal Server Error, Exception in /users.insertGender: {str(e)}"})

    
@app.route('/')
def about():
    return 'Welcome '

if __name__ == "__main__":
    app.run(debug=True, port=5005)

