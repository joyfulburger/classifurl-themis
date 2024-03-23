from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
    # Get the data sent by the client
    data = request.json
    
    # Process the data (e.g., perform prediction using a machine learning model)
    # For demonstration purposes, we'll just echo the received data back
    return jsonify({'received_data': data})

if __name__ == '__main__':
    app.run(debug=True)
