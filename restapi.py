from flask import Flask, jsonify, request

# Initialize the Flask application
app = Flask(__name__)

# In-memory "database" (a dictionary) to store user data.
users = {
    "1": {"name": "Alice", "email": "alice@example.com"},
    "2": {"name": "Bob", "email": "bob@example.com"}
}

# --- Helper Function ---
def get_next_user_id():
    """Generates the next user ID based on the current highest ID."""
    if not users:
        return "1"
    max_id = max(int(k) for k in users.keys())
    return str(max_id + 1)

# --- API Endpoints ---

@app.route('/')
def home():
    """A simple welcome message for the API root."""
    return "<h1>User Management API</h1><p>Welcome to our simple Flask REST API!</p>"

# [READ] Endpoint to get all users
@app.route('/users', methods=['GET'])
def get_all_users():
    """Returns a list of all users."""
    return jsonify(users)

# [READ] Endpoint to get a single user by their ID
@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Returns a single user's data if found."""
    user = users.get(user_id)
    if user:
        return jsonify(user)
    else:
        return jsonify({"error": "User not found"}), 404

# [CREATE] Endpoint to add a new user
@app.route('/users', methods=['POST'])
def create_user():
    """Creates a new user."""
    new_user_data = request.get_json()
    
    if not new_user_data or 'name' not in new_user_data or 'email' not in new_user_data:
        return jsonify({"error": "Invalid request body. 'name' and 'email' are required."}), 400

    new_id = get_next_user_id()
    users[new_id] = {
        "name": new_user_data["name"],
        "email": new_user_data["email"]
    }

    return jsonify(users[new_id]), 201

# [UPDATE] Endpoint to update an existing user
@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Updates an existing user's data."""
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    update_data = request.get_json()

    if not update_data or 'name' not in update_data or 'email' not in update_data:
        return jsonify({"error": "Invalid request body. 'name' and 'email' are required."}), 400

    users[user_id]['name'] = update_data['name']
    users[user_id]['email'] = update_data['email']

    return jsonify(users[user_id])

# [DELETE] Endpoint to delete a user
@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a user."""
    if user_id in users:
        del users[user_id]
        return jsonify({"message": f"User with ID {user_id} deleted successfully."})
    else:
        return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
