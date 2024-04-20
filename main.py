from flask import Flask
import json

app = Flask(__name__)

bookBorrowed = ''

@app.route('/b/<id>')
def books(id):
    global bookBorrowed
    bookBorrowed = id

    rootid = id[:-2]
    copyNum = str(id[6:])

    with open('data.json', "r+") as file:
        data = json.load(file)

        if data['Books'][rootid]['copies'][copyNum] == True:
            print('true')
            data['Books'][rootid]['copies'][copyNum] = False
            # Clear the file content
            file.truncate(0)
            file.seek(0)

            # Write the updated dictionary back to the file
            json.dump(data, file, indent=4)

            return str(f"Please scan the qr code of the borrower of: {data['Books'][rootid]['Title']}")
        
        if data['Books'][rootid]['copies'][copyNum] == False:
            print('false')
            data['Books'][rootid]['copies'][copyNum] = True
            # Clear the file content
            file.truncate(0)
            file.seek(0)

            # Write the updated dictionary back to the file
            json.dump(data, file, indent=4)

            return str(f"Please scan the qr code of the borrower of: {data['Books'][rootid]['Title']}")

    """
    if the user is the same as the borrower in the book's metadata, assume that the book is being returned
    if the book is currently being borrowed, throw an error or smth idk
    """

@app.route('/u/<id>')
def user(id):
    global bookBorrowed
    print(bookBorrowed)

    rootid = bookBorrowed[:-2]
    copyNum = str(bookBorrowed[6:])

    with open('data.json', "r+") as file:
        data = json.load(file)

        if data['Books'][rootid]['copies'][copyNum] == True:
            data['Borrowers'][id]['borrowedBook'] = bookBorrowed
            # Clear the file content
            file.truncate(0)
            file.seek(0)

            # Write the updated dictionary back to the file
            json.dump(data, file, indent=4)
            return (f'State updated! (You can close this now)')


        else:
            data['Borrowers'][id]['borrowedBook'] = None
            # Clear the file content
            file.truncate(0)
            file.seek(0)

            # Write the updated dictionary back to the file
            json.dump(data, file, indent=4)

            return (f'State updated! (You can close this now)')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)