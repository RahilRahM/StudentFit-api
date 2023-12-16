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
    email = request.form.get('email')
    gender = request.form.get('gender')

    # Validate inputs
    if not (email and gender):
        return json.dumps({'status': 400, 'message': 'Invalid input'})

    # Get user id from 'users' table
    user_data = supabase.from_table('users').select('id').ilike('email', email).execute().get('data', [])
    if not user_data:
        return json.dumps({'status': 404, 'message': 'User not found'})

    user_id = user_data[0]['id']

    # Insert new row into 'users_info' table
    result = supabase.from_table('users_info').upsert([
        {'user_id': user_id, 'gender': gender}
    ], on_conflict=['user_id'])

    # Check if the gender update was successful
    if result['status'] == 201:
        return json.dumps({'status': 200, 'message': 'Gender updated successfully'})
    else:
        return json.dumps({'status': result['status'], 'message': result['error']['message']})


@app.route('/')
def about():
    return 'Welcome '

if __name__ == "__main__":
    app.run(debug=True, port=5001)