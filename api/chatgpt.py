from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import constants
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator

app = Flask(__name__)
CORS(app)

os.environ["OPENAI_API_KEY"] = constants.APIKEY

loader = TextLoader('/Users/paldeepsekhon/Desktop/Projects/RutgersProfs/scraper/professors.csv')
index = VectorstoreIndexCreator().from_loaders([loader])

@app.route('/query', methods=['POST'])
def query_index():
    query_data = request.json
    query = query_data.get('query')
    if query:
        response = index.query(query)
        return jsonify(response)
    else:
        return "No query provided", 400

if __name__ == '__main__':
    app.run(debug=True)
