from flask import Flask, render_template
import json

app = Flask(__name__, template_folder="template")

bookBorrowed = ''
returnMode = False
lastBorrowed = ''
lastMsg = ''

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

        rootid = id[:-idlen]
        copyNum = str(id[6:])

        # Finds the book and changes its state
        with open('data.json', "r+") as file:
            data = json.load(file)

            data['Books'][rootid]['copies'][copyNum] = True
            # Clear the file content
            file.truncate(0)
            file.seek(0)

            # Write the updated dictionary back to the file
            json.dump(data, file, indent=4)

            msg = str(f"Please scan the qr code of the borrower of: {data['Books'][rootid]['Title']}")
            return render_template('index.html', outmsg=msg)  # renders a webpage to show the message
            
    if returnMode == True:
        idlen = len(id) - 6  # this is here to fix the edgecase of the id being above 10

        rootid = bookBorrowed[:-idlen]
        copyNum = str(bookBorrowed[6:])

        with open('data.json', 'r+') as file:
            data = json.load(file)

            # just in case that the user scanned the wrong book
            if id != lastBorrowed:
                msg =  (f"This book isn't the one you borrowed. The book you borrowed was" \
                        f"{data['Books'][splitId(lastBorrowed)[0]]['Title']} " \
                        f"Copy no. {splitId(lastBorrowed)[1]}")
                
                return render_template('index.html', outmsg=msg)  # renders a webpage to show the message
            
            if id == lastBorrowed:
                data['Books'][rootid]['copies'][copyNum] = False
                # Clear the file content
                file.truncate(0)
                file.seek(0)

                # Write the updated dictionary back to the file
                json.dump(data, file, indent=4)

                msg =  str(f"Thank you for returning {data['Books'][splitId(lastBorrowed)[0]]['Title']} " \
                           f"Copy no. {splitId(lastBorrowed)[1]}")
                
                return render_template('index.html', outmsg=msg)  # renders a webpage to show the message
            

@app.route('/u/<id>')
def user(id):
    # id here is for the user id thats why idlen uses bookBorrowed instead of the id variable
    global bookBorrowed
    global returnMode  # this is for when the user will return the book
    global lastBorrowed
    global lastMsg  # for the last message

    with open('data.json', 'r+') as file:
        data = json.load(file)

        if data['Borrowers'][id]['borrowedBook'] == None:
            returnMode = False

        else: returnMode = True

    # if nothing has changed just do nothing
    if lastBorrowed == bookBorrowed:
        returnMode = False
        msg = str("Nothing has changed (You can close this now)")
        return render_template('index.html', outmsg=msg)

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
                msg =  str(f'State updated! (You can close this now)')
                return render_template('index.html', outmsg=msg)  # renders a webpage to show the message

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

                msg =  str(f'State updated! (You can close this now)')
                lastMsg = msg
                return render_template('index.html', outmsg=msg)  # renders a webpage to show the message
            
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
            msg =  str(f"Please scan the QR code for the book " \
                    f"{data['Books'][splitId(lastBorrowed)[0]]['Title']} Copy no. " \
                    f"{splitId(lastBorrowed)[1]}")
            lastMsg = msg
            return render_template('index.html', outmsg=msg)  # renders a webpage to show the message

#runs the server
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)