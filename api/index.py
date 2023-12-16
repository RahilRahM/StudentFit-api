from flask import Flask, request
import json
from supabase import create_client, Client

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

@app.route('/users.login',methods=['GET','POST'])
def api_users_login():
    email= request.form.get('email')
    password= request.form.get('password')
    error =False
    if (not email) or (len(email)<5): #You can even check with regx
        error='Email needs to be valid'
    if (not error) and ( (not password) or (len(password)<5) ):
        error='Provide a password'        
    if (not error):    
        response = supabase.table('users').select("*").ilike('email', email).eq('password',password).execute()
        if len(response.data)>0:
            return json.dumps({'status':200,'message':'','data':response.data[0]})
               
    if not error:
         error='Invalid Email or password'        
    
    return json.dumps({'status':500,'message':error})        
    

@app.route('/users.signup.auth',methods=['GET','POST'])
def api_users_signup_auth():
    email= request.args.get('email')
    password= request.args.get('password')
    response = supabase.auth.sign_up({"email": email, "password": password})        
    print(str(response))    
    return str(response)

@app.route('/users.updateGender', methods=['GET','POST'])
def api_users_update_gender():
    try:
        email = request.form.get('email')
        gender = request.form.get('gender')

        if email and gender:
            # Step 1: Retrieve user ID from the users table based on email
            response_users = supabase.table('users').select('id').ilike('email', email).execute()

            if 'error' in response_users:
                return jsonify({'status': 500, 'message': f"Supabase Error: {response_users['error']['message']}"})

            user_id = response_users.data[0]['id'] if 'data' in response_users and len(response_users.data) > 0 else None

            if not user_id:
                return jsonify({'status': 404, 'message': 'User not found'})

            # Step 2: Update the gender in the users_info table
            response_info = supabase.table('users_info').upsert(
                {"user_id": user_id, "gender": gender},
                on_conflict=['user_id'],
            ).execute()

            if 'error' in response_info:
                return jsonify({'status': 500, 'message': f"Supabase Error: {response_info['error']['message']}"})

            if 'data' in response_info and len(response_info.data) > 0:
                return jsonify({'status': 200, 'message': 'Gender updated successfully', 'data': response_info.data[0]})
            elif 'data' not in response_info:
                return jsonify({'status': 500, 'message': 'Error updating gender. No data returned from Supabase.'})
            else:
                return jsonify({'status': 500, 'message': 'Error updating gender. No data returned from Supabase.'})

        else:
            return jsonify({'status': 400, 'message': 'Invalid request. Missing email or gender parameter'})

    except Exception as e:
        print(f"Error updating gender: {e}")
        return jsonify({'status': 500, 'message': f'Internal Server Error: {e}'})


@app.route('/')
def about():
    return 'Welcome'

if __name__ == "__main__":
    app.run(debug=True, port=5001)
