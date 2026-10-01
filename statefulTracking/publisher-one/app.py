from flask import Flask, render_template, request, make_response


app = Flask(__name__) # creates a flask web app 


@app.route('/')  # associates the path / with index.html
def home(): 
    response =  make_response(render_template('index.html'))

    print("\n--- HTTP REQUEST HEADERS ---")
    print(request.headers)
    print("--- HTTP RESPONSE HEADERS ---")
    print(response.headers)

    return response

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8001, debug=True) # automatially reloads the server when th code changes
