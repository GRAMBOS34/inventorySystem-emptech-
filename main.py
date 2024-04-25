from flask import Flask
import json

app = Flask(__name__)

bookBorrowed = ''

@app.route('/b/<id>')
def books(id):
    #This step is for the user part
    global bookBorrowed
    bookBorrowed = id

    idlen = len(id) - 6 #this is here to fix the edgecase of the id being above 10

    rootid = bookBorrowed[:-idlen]
    copyNum = str(bookBorrowed[6:])

    #Finds the book and changes its state
    with open('data.json', "r+") as file:
        data = json.load(file)

        #This is why it'll assume that you've returned the book
        if data['Books'][rootid]['copies'][copyNum] == True:
            print('true')
            data['Books'][rootid]['copies'][copyNum] = False
            # Clear the file content
            file.truncate(0)
            file.seek(0)

            # Write the updated dictionary back to the file
            json.dump(data, file, indent=4)

            return str(f"Please scan the qr code of the borrower of: {data['Books'][rootid]['Title']}")
        
        #This is why it'll assume that you're borrowing the book
        if data['Books'][rootid]['copies'][copyNum] == False:
            print('false')
            data['Books'][rootid]['copies'][copyNum] = True
            # Clear the file content
            file.truncate(0)
            file.seek(0)

            # Write the updated dictionary back to the file
            json.dump(data, file, indent=4)

            return str(f"Please scan the qr code of the borrower of: {data['Books'][rootid]['Title']}")
        
        #I haven't made edge cases yet nor do I know how to do it in this case I don't care enough to try tbh

@app.route('/u/<id>')
def user(id):
    global bookBorrowed

    #This is so that it'll update the borrowedBook value in the user
    idlen = len(bookBorrowed) - 6 #this is here to fix the edgecase of the id being above 10

    rootid = bookBorrowed[:-idlen]
    copyNum = str(bookBorrowed[6:])

    with open('data.json', "r+") as file:
        data = json.load(file)

        #If the borrowed book returns true, it'll assume that you've borrowed it
        #This just updates that state
        if data['Books'][rootid]['copies'][copyNum] == True:
            data['Borrowers'][id]['borrowedBook'] = bookBorrowed
            # Clear the file content
            file.truncate(0)
            file.seek(0)

            # Write the updated dictionary back to the file
            json.dump(data, file, indent=4)
            return (f'State updated! (You can close this now)')

        #If the borrowed book returns false, it'll assume that you've returned it
        #This just updates that state
        else:
            data['Borrowers'][id]['borrowedBook'] = None
            # Clear the file content
            file.truncate(0)
            file.seek(0)

            # Write the updated dictionary back to the file
            json.dump(data, file, indent=4)

            return (f'State updated! (You can close this now)')

#runs the server
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)