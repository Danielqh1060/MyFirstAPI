from flask import Flask, request, jsonify
from mailersend import emails
from dotenv import load_dotenv
import os
import json

load_dotenv()

def load_users():
    with open('usuarios.json', 'r') as file:
        return json.load(file)

def save_users(users):
    with open('usuarios.json', 'w') as file:
        json.dump(users, file, indent=4)

app = Flask(__name__)

@app.route('/users', methods=['GET'])
def getUsers():
    users = load_users()
    return jsonify(users) #Convierte en string

@app.route('/', methods=['GET'])
def hellowWord():
    return jsonify({"message": "Hello World"})

@app.route('/users/<int:userId>', methods=['GET'])
def getUser(userId):
    users = load_users()
    user = None
    i = 0
    found = False
    # Búsqueda utilizando while y bandera
    while i < len(users) and not found:
        if users[i]['id'] == userId:
            user = users[i]
            found = True
        i += 1
    if found:
        return jsonify(user)
    else:
        return jsonify({"error": "User not found"}), 404 #codigo de estado HTTP

@app.route('/users', methods=['POST'])
def createUser():
    users = load_users()
    data = request.get_json()

    if len(users) > 0:
        i = 1
        last_user = users[0]

        while i < len(users):
            if users[i]['id'] > last_user['id']:
                last_user = users[i]
            i += 1

        new_id = last_user['id'] + 1

    else:
        new_id = 1

    new_user = {
        "id": new_id,
        "name": data['name'],
        "password": data['password'],
        "email": data['email'],
        "nickname": data['nickname']
    }
    users.append(new_user)
    save_users(users)
    return jsonify({"message": "User created successfully"}),204

@app.route('/users/<int:userId>', methods=['PUT'])
def updateUser(userId):
    users = load_users()
    user = None
    i = 0

    found = False
    # Búsqueda utilizando while y bandera
    while i < len(users) and not found:
        if users[i]['id'] == userId:
            user = users[i]
            found = True
        i += 1

    if found:
        data = request.get_json()
        user['name'] = data['name']
        user['password'] = data['password']
        user['email'] = data['email']
        user['nickname'] = data['nickname']

        save_users(users)
        return jsonify({"message": "User updated successfully"})
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/users/<int:userId>', methods=['DELETE'])
def deleteUser(userId):
    users = load_users()
    user = None
    i = 0
    found = False

    # Búsqueda utilizando while y bandera
    while i < len(users) and not found:
        if users[i]['id'] == userId:
            user = users[i]
            found = True
        i += 1

    if found:
        users.remove(user)
        save_users(users)
        return jsonify({"message": "User deleted successfully"})
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/sendemail', methods=['POST'])
def sendEmail():
    """
    Function that sends an email 
    """
    data = request.get_json()
    mailer = emails.NewEmail(os.getenv('MAILERSEND_API_KEY'))

    # define an empty dict to populate with mail values
    mail_body = {}

    mail_from = {
        "name": "Contacto Daniel",
        "email": "contacto@trial-neqvygmxq65l0p7w.mlsender.net",
    }

    recipients = data['recipients']

    reply_to = {
        "name": "Name",
        "email": "reply@domain.com",
    }

    mailer.set_mail_from(mail_from, mail_body)
    mailer.set_mail_to(recipients, mail_body)
    mailer.set_subject(data['subject'], mail_body)
    mailer.set_html_content(data['content'], mail_body)
    # mailer.set_plaintext_content("This is the text content", mail_body)
    mailer.set_reply_to(reply_to, mail_body)

    # using print() will also return status code and data
    print(mailer.send(mail_body))

    return jsonify({"message": "Email sent successfully"})

if __name__ == '__main__':
    app.run(debug=True)