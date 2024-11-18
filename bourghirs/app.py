"""
Imports
"""
from flask import Flask, render_template, url_for, request, jsonify, session
import json
from os.path import abspath, exists
import os
import traceback
from dotenv import load_dotenv

"""
Flask App Setup
"""
app = Flask(__name__)
app.secret_key = 'E543F9C6E3BC1D7F6C66BAB47B8B2'


"""
Admin API
"""
@app.route('/make_admin', methods=['POST'])
def make_admin():
    session['user_admin'] = True
    return jsonify({"message": "User is now an admin."}), 200

@app.route('/remove_admin', methods=['POST'])
def remove_admin():
    session['user_admin'] = False
    return jsonify({"message": "User is no longer an admin."}), 200

"""
Add Item API
"""
@app.route('/add-item', methods=['POST'])
def add_item():
    try:
        # Parse form data
        item_name = request.form['name']
        item_price = float(request.form['price'])
        item_description = request.form['description']
        allergens = json.loads(request.form['allergens'])
        tags = json.loads(request.form['tags'])
        item_image = request.files['image']

        # Create new item dictionary
        new_item = {
            "name": item_name,
            "price": item_price,
            "description": item_description,
            "allergens": allergens,
            "tags": tags,
            "thumbnail": item_image.filename,
            "thumbnail_alt": f"Picture of the {item_name}"
        }

        # Ensure the directory exists
        image_dir = abspath('static/img')
        if not exists(image_dir):
            os.makedirs(image_dir)

        # Save the image file
        image_path = abspath(f'static/img/{item_image.filename}')
        item_image.save(image_path)

        # Read and update the menu.json file
        with open('menu.json', 'r+') as file:
            data = json.load(file)
            data['menu_items'].append(new_item)
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()  # Ensure the file is truncated to the new length
        
        return jsonify({'success': True})
    except Exception as e:
        print("Exception occurred:", e)
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

"""
Website Pages
"""
@app.route('/')
@app.route('/home')
def home():
    user_admin = session.get('user_admin', False)
    return render_template('index.html', user_admin=user_admin)

@app.route('/menu')
def menu():
    user_admin = session.get('user_admin', False)
    menu_path = os.path.join(os.path.dirname(__file__), 'menu.json') 
    with open(menu_path) as f:
        menu_data = json.load(f)
  
    food_filter = request.args.get('food')
    burger_filter = request.args.get('burger')
    drink_filter = request.args.get('drink')
    dessert_filter = request.args.get('dessert')

    filtered_items = menu_data['menu_items']

    food_filter = request.args.get('food')
    burger_filter = request.args.get('burger')
    drink_filter = request.args.get('drink')
    dessert_filter = request.args.get('dessert')

    filtered_items = menu_data['menu_items']

    if burger_filter:
        filtered_items = [item for item in filtered_items if 'Burger' in item.get('tags', [])]
    elif food_filter:
        filtered_items = [item for item in filtered_items if 'Food' in item.get('tags', [])]
    elif drink_filter: 
        filtered_items = [item for item in filtered_items if 'Drink' in item.get('tags', [])]
    elif dessert_filter: 
        filtered_items = [item for item in filtered_items if 'Dessert' in item.get('tags', [])]

    return render_template('pages/menu.html', menu_items=filtered_items, user_admin=user_admin)
@app.route('/menu/<item_name>')
def menu_item(item_name):
    user_admin = session.get('user_admin', False)
    menu_path = os.path.join(os.path.dirname(__file__), 'menu.json')
    try:
        with open(menu_path) as f:
            menu_data = json.load(f)
    except FileNotFoundError:
        return "Menu file not found", 404

    item = next((item for item in menu_data['menu_items'] if item['name'] == item_name), None)
    if item:
        return render_template('pages/items/menu_item.html', item=item, user_admin=user_admin)
    else:
        return "Item not found", 404


@app.route('/slots')
def slots():
    user_admin = session.get('user_admin', False)
    return render_template('pages/slots.html', user_admin=user_admin)


@app.route('/quiz')
def quiz():
    user_admin = session.get('user_admin', False)
    return render_template('pages/quiz.html', user_admin=user_admin)

@app.route('/admin')
def admin():
    user_admin = session.get('user_admin', False)
    if user_admin:
        return render_template('pages/admin.html', user_admin=user_admin)
    else:
        return "<h1>Access denied<h1>", 403

"""
Run Flask App (Change to "app.run(host='0.0.0.0', debug=True)" for development)
"""
if __name__ == '__main__':
    app.run(host='0.0.0.0')
