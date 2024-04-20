import qrcode
import random
import string
import json
import socket

hostname = socket.gethostname()
ipaddress = socket.gethostbyname(hostname)
HOST = f"http://{ipaddress}:5000/"

#generates the qrcodes and puts them in the folder "qrcodes"
def makeQr (url, typeid, filename):
    img = qrcode.make(url)

    type(img)

    img.save(f'qrcodes/{typeid}/{filename}.png')

#generates the url for the qrcodes
def generateurl(typeid, title):
    #check if the book exists if it does, use the id of the original book and increment the copy num (the numbers)
    with open('data.json', 'r+') as file:
        data = json.load(file)

        if typeid == "b":
            for i in data['Books']:
                #checks if the title exists
                if title == data['Books'][i]["Title"]:
                    copies = data['Books'][i]['copies']
                    index = "0" + str(len(copies))
                    copies[index] = False

                    url = HOST + typeid + f"/{i}{index}"
                    filename = i + index #filename is the id
                    makeQr(url=url, typeid="books",filename=filename)
        
                    # Clear the file content
                    file.truncate(0)
                    file.seek(0)

                    # Write the updated dictionary back to the file
                    json.dump(data, file, indent=4)
                    return #exits the function after it adds a new copy
            
            #if it manages to get out here, it means that the title doesn't exist
            newId = "".join(random.choices(string.ascii_letters, k = 6))
            newBook = {
                "Title": title,
                "copies": {
                    "00": False
                }
            }

            #make the url before saving
            url = HOST + typeid + f"/{newId}00"
            filename = newId + "00" #file name is the id
            makeQr(url=url, typeid='books',filename=filename)

            data["Books"][newId] = newBook

            # Clear the file content
            file.truncate(0)
            file.seek(0)

            # Write the updated dictionary back to the file
            json.dump(data, file, indent=4)

def addNewUser(typeId, name):
    with open('data.json', "r+") as file:
        data = json.load(file)
        if typeId == "u":
            #no check for if the user already exists because there may be others with the same name
            #albeit rare, it can happen
            #full names should be used so it's less likely to happen
            newId = "".join(random.choices(string.digits, k = 8))
            data['Borrowers'][newId] = {
                "borrowerName": name,
                "borrowedBook": None
            }

            url = HOST + typeId + '/' + newId

            makeQr(url=url, typeid='users', filename=newId)

            # Clear the file content
            file.truncate(0)
            file.seek(0)

            # Write the updated dictionary back to the file
            json.dump(data, file, indent=4)
            

#main function (for adding books and users)
if __name__ == "__main__":
    while True:
        try:
            ans = str(input("Would you like to add a new book or user? (u/b) (q to quit): "))

            if ans.lower() == 'b':
                while True:
                    bookName = str(input('Name of book: '))
                    try:
                        num_of_copies = int(input("Number of Copies: "))
                    except:
                        print("Try again")
                        continue

                    for i in range(num_of_copies):
                        generateurl('b', bookName)
                        
                    break

            if ans.lower() == 'u':
                newUser = str(input('Name of New User: '))
                addNewUser('u', newUser)
                continue

            if ans.lower() == 'q':
                break

        except: 
            print("That didn't seem like one of the choices, try again.")
            continue