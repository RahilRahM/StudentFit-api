from flask import Flask, jsonify, request
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



@app.route('/users.change_password', methods=['POST'])
def api_users_change_password():
    email = request.form.get('email')
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')

    # Validate email
    if not email or len(email) < 5:
        return jsonify({'status': 400, 'message': 'Invalid email'})

    # Validate old password
    if not old_password or len(old_password) < 5:
        return jsonify({'status': 400, 'message': 'Invalid old password'})

    # Validate new password
    if not new_password or len(new_password) < 5:
        return jsonify({'status': 400, 'message': 'Invalid new password'})

    # Check if the user exists
    user_response = supabase.table('users').select("*").ilike('email', email).execute()
    if len(user_response.data) == 0:
        return jsonify({'status': 404, 'message': 'User not found'})

    user_data = user_response.data[0]

    # Check if the old password matches
    if user_data['password'] != old_password:
        return jsonify({'status': 401, 'message': 'Incorrect old password'})

    # Update the user's password
    update_response = supabase.table('users').update({'password': new_password}).eq('email', email).single().execute()


    if len(update_response.data) == 0:
        return jsonify({'status': 500, 'message': 'Error updating password'})

    return jsonify({'status': 200, 'message': 'Password updated successfully'})



@app.route('/')
def about():
    return 'Welcome '

if __name__ == "__main__":
    app.run(debug=True, port=5005)

