from flask import Flask, request, jsonify
import sqlite3
from database import get_db

#instantiate Flask
app = Flask(__name__)



@app.route('/member', methods=['GET'])
def get_members():
    db = get_db()
    members_cur = db.execute('select id, name, email, level from members')
    members = members_cur.fetchall()

    return_values = []

    for m in members:
        member_dict = {}
        member_dict['id'] = m['id']
        member_dict['name'] = m['name']
        member_dict['email'] = m['email']
        member_dict['level'] = m['level']

        #now we append the member dictionaries to the return value
        return_values.append(member_dict)
    #we want to return a json object
    return jsonify({'members' : return_values})

@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):

    db = get_db()
    member_cur =db.execute('select id, name, email, level from members where id = ?', [member_id])
    member = member_cur.fetchone()

    
    return jsonify({'member': {'id': member['id'], 'name': member['name'], 'email': member['email'], 'level': member['level']}})


@app.route('/member', methods=['POST'])
def add_member():
    #this will get the json object
    new_member_data = request.get_json()
    name = new_member_data['name']
    email = new_member_data['email']
    level = new_member_data['level']

    db = get_db()
    db.execute('insert into members (name, email, level) values (?,?,?)', [name, email, level])
    db.commit()

    member_cur = db.execute('select id, name, email, level from members where name = ?',[name])
    new_member = member_cur.fetchone()
    
    
    return jsonify({'id': new_member['id'],'name': new_member['name'] , \
                    'email': new_member['email'] , 'level': new_member['level']})

@app.route('/member/<int:member_id>', methods=['PUT' , 'PATCH']) #this updates an existing member
def edit_member(member_id):
    new_member_data = request.get_json()

    name = new_member_data['name']
    email = new_member_data['email']
    level = new_member_data['level']

    db = get_db()
    db.execute('update members set name = ?, email = ?, level =? where id= ?', [name, email,level,member_id])
    db.commit()

    member_cur = db.execute('select id, name, email, level from members where id = ?', [member_id])
    new_member = member_cur.fetchone()
    
    return jsonify({"member": { "id": new_member['id'], "name": new_member['name'], "email": new_member['email'], "level": new_member['level']}})

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    db = get_db()
    db.execute('delete from members where id = ?',[member_id])
    db.commit()

    return jsonify({'message': 'The member has been deleted'})






if __name__ == '__main__':
    app.run(debug=True)

    
