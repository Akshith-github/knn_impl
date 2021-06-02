from flask import Flask, request, jsonify
import json

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/recommend_book',methods=['GET','POST'])
def send_recommend():
    if('n' in request.args):
        try:
            n= int(request.args['n'])
        except:
            return "invalid n value ,accepts int only"
    else:
        n=10
    if 'book_name' in request.args:
        book_name = request.args['book_name']
        print(book_name)
        from load_model_and_recommend import recommend_for_book
        l=recommend_for_book(book_name,n_neighbors=n)
    elif 'isbn' in request.args:
        isbn_no = request.args['isbn']
        print(isbn_no)
        from load_model_and_recommend import recommend_for_book_isbn
        l=recommend_for_book_isbn(isbn_no,n_neighbors=n)
    else:
        from load_model_and_recommend import run_random_recommend
        l=run_random_recommend(n)
    # json_res = json() 
    # l_=dict()
    # for k,v in l.items():
    #     l_[k]=json.dumps(v)
    return json.dumps(l) #jsonify(l)
    

    

if __name__ == '__main__':
    app.run(port=5055)

# books = [
#     {'id': 0,
#      'title': 'A Fire Upon the Deep',
#      'author': 'Vernor Vinge',
#      'first_sentence': 'The coldsleep itself was dreamless.',
#      'year_published': '1992'},
#     {'id': 1,
#      'title': 'The Ones Who Walk Away From Omelas',
#      'author': 'Ursula K. Le Guin',
#      'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
#      'published': '1973'},
#     {'id': 2,
#      'title': 'Dhalgren',
#      'author': 'Samuel R. Delany',
#      'first_sentence': 'to wound the autumnal city.',
#      'published': '1975'}
# ]
# @app.route('/recommend_api', methods=['GET', 'POST'])
# def method_name():
#     return jsonify(books)

# @app.route('/api/v1/resources/books', methods=['GET'])
# def api_id():
#     # Check if an ID was provided as part of the URL.
#     # If ID is provided, assign it to a variable.
#     # If no ID is provided, display an error in the browser.
#     if 'id' in request.args:
#         id = int(request.args['id'])
#     else:
#         return "Error: No id field provided. Please specify an id."

#     # Create an empty list for our results
#     results = []

#     # Loop through the data and match results that fit the requested ID.
#     # IDs are unique, but other fields might return many results
#     for book in books:
#         if book['id'] == id:
#             results.append(book)

#     # Use the jsonify function from Flask to convert our list of
#     # Python dictionaries to the JSON format.
#     return jsonify(results)