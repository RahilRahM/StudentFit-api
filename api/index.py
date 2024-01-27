from flask import Flask, jsonify, request
import json
from supabase import create_client, Client
import traceback
from datetime import datetime

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

    if not error:
        # Fetch user by email
        response = supabase.table('users').select("*").ilike('email', email).execute()

        if len(response.data) > 0:
            user = response.data[0]

            # Compare hashed password
            if user['password'] == password: 
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



@app.route('/isEmailExists', methods=['GET'])
def is_email_exists():
    email = request.args.get('email')

    if not email or len(email) < 5:
        return json.dumps({'status': 400, 'message': 'Email needs to be valid'}), 400

    response = supabase.table('users').select("*").ilike('email', email).execute()

    if len(response.data) > 0:
        return json.dumps({'status': 200, 'message': 'Email exists'}), 200
    else:
        return json.dumps({'status': 404, 'message': 'Email does not exist'}), 404

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
    
@app.route('/users.insertWeight', methods=['POST', 'GET'])
def api_users_insert_weight_record():
    user_id = request.form.get('user_id')
    weight = request.form.get('weight')

    try:
        if not (user_id and weight):
            return json.dumps({'status': 400, 'message': 'Invalid input'})

        # Insert a new row with the given user_id and weight
        result = supabase.table('weight_records').insert({'user_id': user_id, 'weight': weight}).execute()

        return json.dumps({'status': 200, 'message': 'Weight record inserted successfully', 'result': str(result)})
        
    except Exception as e:
        return json.dumps({'status': 500, 'message': f"Internal Server Error, Exception in /users.insertWeight: {str(e)}"})

    
@app.route('/users.insertWaterIntake', methods=['GET', 'POST'])
def api_users_insert_water_intake():
    user_id = request.form.get('user_id')
    water_intake = float(request.form.get('water_intake'))

    try:
        if not (user_id and water_intake):
            return json.dumps({'status': 400, 'message': 'Invalid input'})

        # Insert a new row with the given user_id and water_intake
        result = supabase.table('water_intake_records').insert({'user_id': user_id, 'water_intake': water_intake}).execute()

        return json.dumps({'status': 200, 'message': 'Water intake recorded successfully', 'result': str(result)})

    except Exception as e:
        return json.dumps({'status': 500, 'message': f"Internal Server Error, Exception in /users.insertWaterIntake: {str(e)}"})
 
@app.route('/users.getUserInfo', methods=['POST','GET'])
def api_users_get_user_info():
    user_id = request.args.get('user_id')

    if not user_id:
        return json.dumps({'status': 400, 'message': 'Invalid input'})

    try:
        # Fetch user info from the users_info table
        user_info_response = supabase.table('users_info').select("*").eq('user_id', user_id).execute()

        # Fetch user latest weight from the weight_records table
        weight_records_response = supabase.table('weight_records').select("weight").eq('user_id', user_id).order('recorded_at', desc=True).limit(1).execute()

        if len(user_info_response.data) == 0 and len(weight_records_response.data) == 0:
            return json.dumps({'status': 404, 'message': 'User info not found'})

        return json.dumps({
            'status': 200, 
            'message': 'User info fetched successfully', 
            'user_info': user_info_response.data, 
            'weight': weight_records_response.data
        })

    except Exception as e:
        return json.dumps({'status': 500, 'message': f"Internal Server Error, Exception in /users.getUserInfo: {str(e)}"})
@app.route('/users.update', methods=['PUT'])
def api_users_update():
    try:
        user_data = request.get_json()  # Make sure you're correctly parsing JSON
        user_id = user_data.get('id')
        new_name = user_data.get('name')

        # Validate input data
        if not user_id:
            return jsonify({'status': 400, 'message': 'User ID is required'}), 400
        if not new_name:
            return jsonify({'status': 400, 'message': 'New name is required'}), 400

        # Update user details in Supabase
        response = supabase.table('users').update({
            'name': new_name
        }).eq('id', user_id).execute()

        if response.error:
            return jsonify({'status': 500, 'message': str(response.error)}), 500

        return jsonify({'status': 200, 'message': 'User updated successfully', 'data': response.data}), 200

    except Exception as e:
        return jsonify({'status': 500, 'message': f'Internal Server Error: {str(e)}'}), 500



      
@app.route('/')
def about():
    return 'Welcome '

if __name__ == "__main__":
    app.run(debug=True, port=5005)

