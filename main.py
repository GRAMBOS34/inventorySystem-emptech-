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

    idlen = len(id) - 6  # this is here to fix the edgecase of the id being above 10
    rootid = id[:-idlen]
    copyNum = str(id[6:])

    # if nothing has changed just do nothing this is if we scan the same user qrcode twice or more in a row
    if len(bookBorrowed) == 0 and returnMode == True:
        msg = str("Nothing has changed (You can close this now)")
        return render_template('index.html', outmsg=msg)

    if returnMode == False:
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
            lastBorrowed = id
            return render_template('index.html', outmsg=msg)  # renders a webpage to show the message
            
    if returnMode == True:
        with open('data.json', 'r+') as file:
            data = json.load(file)

            # just in case that the user scanned the wrong book
            if len(bookBorrowed) == 0:
                msg = str(f"Nothing has changed ({lastMsg})")
                return render_template('index.html', outmsg=msg)

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
                returnMode = False
                
                return render_template('index.html', outmsg=msg)  # renders a webpage to show the message
            

@app.route('/u/<id>')
def user(id):
    # id here is for the user id thats why idlen uses bookBorrowed instead of the id variable
    global bookBorrowed
    global returnMode  # this is for when the user will return the book
    global lastBorrowed
    global lastMsg  # for the last message

    # This is so that it'll update the borrowedBook value in the user
    idlen = len(bookBorrowed) - 6  # this is here to fix the edgecase of the id being above 10

    rootid = bookBorrowed[:-idlen]
    copyNum = str(bookBorrowed[6:])

    # this is how we check if it's someone trying to return a book or not
    with open('data.json', 'r+') as file:
        data = json.load(file)

        if data['Borrowers'][id]['borrowedBook'] == None:
            returnMode = False

        else: returnMode = True

    # this is our so-called "borrowing mode"
    if returnMode == False:
        with open('data.json', "r+") as file:
            data = json.load(file)

            # just in case that the user scanned the wrong book
            if len(bookBorrowed) == 0:
                msg = str(f"Nothing has changed ({lastMsg})")
                returnMode = True
                return render_template('index.html', outmsg=msg)

            # If the borrowed book returns true, it'll assume that you've borrowed it
            # This just updates that state
            if data['Books'][rootid]['copies'][copyNum] == True:
                data['Borrowers'][id]['borrowedBook'] = bookBorrowed
                data['Borrowers'][id]['borrowedBookTitle'] = f"{data['Books'][rootid]['Title']} Copy No. {copyNum}"  # for the html file fml
                # Clear the file content
                file.truncate(0)
                file.seek(0)

                # Write the updated dictionary back to the file
                json.dump(data, file, indent=4)
                bookBorrowed = '' # clears this variable
                msg =  str(f'State updated! (You can close this now)')
                lastMsg = msg
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
            data['Borrowers'][id]['borrowedBookTitle'] = None  # for the html file fml

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
            bookBorrowed = ''
            return render_template('index.html', outmsg=msg)  # renders a webpage to show the message

#runs the server
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)