from flask import Flask
import json

app = Flask(__name__)

bookBorrowed = ''
returnMode = False
lastBorrowed = ''

# splits the book id 
def splitId (bookid) -> list:
    idlen = len(bookid) - 6  # this is here to fix the edgecase of the id being above 10

    rootid = bookid[:-idlen]
    copyNum = str(bookid[6:])

    return [rootid, copyNum]

@app.route('/b/<id>')
def books(id):
    global returnMode
    global lastBorrowed
    global bookBorrowed  # This step is for the books part
    bookBorrowed = id

    if returnMode == False:
        idlen = len(id) - 6  # this is here to fix the edgecase of the id being above 10

        rootid = bookBorrowed[:-idlen]
        copyNum = str(bookBorrowed[6:])

        # Finds the book and changes its state
        with open('data.json', "r+") as file:
            data = json.load(file)

            data['Books'][rootid]['copies'][copyNum] = True
            # Clear the file content
            file.truncate(0)
            file.seek(0)

            # Write the updated dictionary back to the file
            json.dump(data, file, indent=4)

            return str(f"Please scan the qr code of the borrower of: {data['Books'][rootid]['Title']}")
            
    if returnMode == True:
        idlen = len(id) - 6  # this is here to fix the edgecase of the id being above 10

        rootid = bookBorrowed[:-idlen]
        copyNum = str(bookBorrowed[6:])

        with open('data.json', 'r+') as file:
            data = json.load(file)

            # just in case that the user scanned the wrong book
            if id != lastBorrowed:
                return (f"This book isn't the one you borrowed. The book you borrowed was" \
                        f"{data['Books'][splitId(lastBorrowed)[0]]['Title']} " \
                        f"Copy no. {splitId(lastBorrowed)[1]}")
            
            if id == lastBorrowed:
                data['Books'][rootid]['copies'][copyNum] = False
                # Clear the file content
                file.truncate(0)
                file.seek(0)

                # Write the updated dictionary back to the file
                json.dump(data, file, indent=4)

                return str(f"Thank you for returning {data['Books'][splitId(lastBorrowed)[0]]['Title']} " \
                           f"Copy no. {splitId(lastBorrowed)[1]}")
            

@app.route('/u/<id>')
def user(id):
    # id here is for the user id thats why idlen uses bookBorrowed instead of the id variable
    global bookBorrowed
    global returnMode  # this is for when the user will return the book
    global lastBorrowed

    with open('data.json', 'r+') as file:
        data = json.load(file)

        if data['Borrowers'][id]['borrowedBook'] == None:
            returnMode = False

        else: returnMode = True

    # this is our so-called "borrowing mode"
    if returnMode == False:
        # This is so that it'll update the borrowedBook value in the user
        idlen = len(bookBorrowed) - 6  # this is here to fix the edgecase of the id being above 10

        rootid = bookBorrowed[:-idlen]
        copyNum = str(bookBorrowed[6:])

        with open('data.json', "r+") as file:
            data = json.load(file)

            # If the borrowed book returns true, it'll assume that you've borrowed it
            # This just updates that state
            if data['Books'][rootid]['copies'][copyNum] == True:
                data['Borrowers'][id]['borrowedBook'] = bookBorrowed
                # Clear the file content
                file.truncate(0)
                file.seek(0)

                # Write the updated dictionary back to the file
                json.dump(data, file, indent=4)
                bookBorrowed = '' # clears this variable
                return (f'State updated! (You can close this now)')

            # If the borrowed book returns false, it'll assume that you've returned it
            # This just updates that state
            else:
                data['Borrowers'][id]['borrowedBook'] = None
                # Clear the file content
                file.truncate(0)
                file.seek(0)

                # Write the updated dictionary back to the file
                json.dump(data, file, indent=4)
                bookBorrowed = '' # clears this variable

                return (f'State updated! (You can close this now)')
            
    # this is our so-called "return mode"
    if returnMode == True:
        with open('data.json', 'r+') as file:
            data = json.load(file)

            # in case that the user scans their id first while trying to borrow a book
            if data['Borrowers'][id]['borrowedBook'] == None:
                return ("No book borrowed, why not try borrowing one?")
            
            lastBorrowed = data['Borrowers'][id]['borrowedBook']  # updates lastBorrowed variable for the book qr scan 

            data['Borrowers'][id]['borrowedBook'] = None
            # Clear the file content
            file.truncate(0)
            file.seek(0)

            # Write the updated dictionary back to the file
            json.dump(data, file, indent=4)

            returnMode = True

            # lord have mercy on this return statement
            return (f"Please scan the QR code for the book " \
                    f"{data['Books'][splitId(lastBorrowed)[0]]['Title']} Copy no. " \
                    f"{splitId(lastBorrowed)[1]}")

#runs the server
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)