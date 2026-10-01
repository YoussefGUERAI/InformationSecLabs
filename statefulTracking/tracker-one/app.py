from flask import Flask, render_template, request, make_response
import secrets

app = Flask(__name__) # creates a flask web app 


@app.route('/')  # associates the path / with index.html
def home(): 

    publisher = request.args.get("publisher", "unknown publisher")
    page = request.args.get("page", "unknown page")

    # Check whether the browser already has an identifier
    aid = request.cookies.get("aid")
    is_new = aid is None

    if is_new:
        aid = secrets.token_hex(8)

    response = make_response(render_template(
        'index.html',
        publisher=publisher,
        page=page,
    ))
    if is_new:
        response.set_cookie(key="aid",value=aid)
        

    print("\n--- HTTP REQUEST HEADERS ---")
    print(request.headers)
    print("--- HTTP RESPONSE HEADERS ---")
    print(response.headers)

    return response

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9000, debug=True) # automatially reloads the server when th code changes
