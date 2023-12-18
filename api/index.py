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


@app.route('/users.insertGender', methods=['GET', 'POST'])
def api_users_insert_gender():
    user_id = request.form.get('user_id')
    gender = request.form.get('gender')
    
    try:
        if not (user_id and gender):
            return json.dumps({'status': 400, 'message': 'Invalid input'})

        # Check if a row with the given user_id already exists in the users_info table
        result = supabase.table('users_info').select('user_id').eq('user_id', user_id).execute()
        if result.data and len(result.data) > 0:
            # If a row with the given user_id already exists, update it
            result = supabase.table('users_info').update({'gender': gender}).eq('user_id', user_id).execute()
        else:
            # If no row with the given user_id exists, insert a new one
            result = supabase.table('users_info').insert({'user_id': user_id, 'gender': gender}).execute()

        return json.dumps({'status': 200, 'message': 'Gender updated successfully', 'result': str(result)})
        
    except Exception as e:
        return json.dumps({'status': 500, 'message': f"Internal Server Error, Exception in /users.insertGender: {str(e)}"})
    
@app.route('/users.insertAge', methods=['GET', 'POST'])
def api_users_insert_age():
    user_id = request.form.get('user_id')
    age = request.form.get('age')
    
    try:
        if not (user_id and age):
            return json.dumps({'status': 400, 'message': 'Invalid input'})

        # Check if a row with the given user_id already exists in the users_info table
        result = supabase.table('users_info').select('user_id').eq('user_id', user_id).execute()
        if result.data and len(result.data) > 0:
            # If a row with the given user_id already exists, update it
            result = supabase.table('users_info').update({'age': age}).eq('user_id', user_id).execute()
        else:
            # If no row with the given user_id exists, insert a new one
            result = supabase.table('users_info').insert({'user_id': user_id, 'age': age}).execute()

        return json.dumps({'status': 200, 'message': 'Age updated successfully', 'result': str(result)})
        
    except Exception as e:
        return json.dumps({'status': 500, 'message': f"Internal Server Error, Exception in /users.insertAge: {str(e)}"})
    
@app.route('/')
def about():
    return 'Welcome '

if __name__ == "__main__":
    app.run(debug=True, port=5005)

