from flask import Flask, jsonify, request
import json
from supabase import create_client, Client
import traceback



app = Flask(__name__)

url="https://iqacemdedaqxepotxlbb.supabase.co"
key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlxYWNlbWRlZGFxeGVwb3R4bGJiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDI0OTI4OTQsImV4cCI6MjAxODA2ODg5NH0.a8KGVvu2jG9gNlWzi03lMNl7oaIjKZVAf0Qpo6WS5Lk"
supabase: Client = create_client(url, key)


@app.route('/users.signup',methods=['GET','POST'])
def api_users_signup():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    error = False

    # Validate name
    if (not name) or (len(name) < 2):  # You can adjust the length requirement
        error = 'Name needs to be valid'

    # Validate email
    if (not error) and ((not email) or (len(email) < 5)):  # You can even check with regex
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
        print(str(response.data))
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

    if not error:
        # Fetch user by email
        response = supabase.table('users').select("*").ilike('email', email).execute()

        if len(response.data) > 0:
            user = response.data[0]

            # Compare hashed password
            if user['password'] == password:  # Replace with your hash comparison logic
                return json.dumps({'status': 200, 'message': '', 'data': user})
            else:
                error = 'Invalid Email or password'

    if error:
        return json.dumps({'status': 500, 'message': error})

    return json.dumps({'status': 500, 'message': 'Invalid Email or password'})




@app.route('/users.changePassword', methods=['PUT'])
def api_users_change_password():
    email = request.form.get('email')
    new_password = request.form.get('newPassword')
    error = False

    # Validate email
    if (not email) or (len(email) < 5):
        error = 'Email needs to be valid'

    # Validate new password
    if (not error) and ((not new_password) or (len(new_password) < 5)):
        error = 'Provide a valid new password'

    # Update the password in the Supabase database
    if not error:
        response = supabase.table('users').update({"password": new_password}).ilike('email', email).execute()
        if len(response.data) == 0:
            error = 'Error updating the password'

    if error:
        return json.dumps({'status': 400, 'message': error})

    return json.dumps({'status': 200, 'message': 'Password updated successfully'})


















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

@app.route('/users.insertHeight', methods=['GET', 'POST'])
def api_users_insert_height():
    user_id = request.form.get('user_id')
    height = request.form.get('height')
    
    try:
        if not (user_id and height):
            return json.dumps({'status': 400, 'message': 'Invalid input'})

        # Check if a row with the given user_id already exists in the users_info table
        result = supabase.table('users_info').select('user_id').eq('user_id', user_id).execute()
        if result.data and len(result.data) > 0:
            # If a row with the given user_id already exists, update it
            result = supabase.table('users_info').update({'height': height}).eq('user_id', user_id).execute()
        else:
            # If no row with the given user_id exists, insert a new one
            result = supabase.table('users_info').insert({'user_id': user_id, 'height': height}).execute()

        return json.dumps({'status': 200, 'message': 'Height updated successfully', 'result': str(result)})
        
    except Exception as e:
        return json.dumps({'status': 500, 'message': f"Internal Server Error, Exception in /users.insertHeight: {str(e)}"})
    
@app.route('/')
def about():
    return 'Welcome '

if __name__ == "__main__":
    app.run(debug=True, port=5005)

