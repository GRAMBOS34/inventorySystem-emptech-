import json

def remove_numbers(text):
    """Removes numbers from the id"""
    return "".join([char for char in text if not char.isdigit()])

def remove_letters(text):
    """Removes letters from the id"""
    return "".join(filter(str.isdigit, text))


while True:
  query = str(input("Search inventory: "))
  with open('data.json', "r+") as file:
    data = json.load(file)

    #god's worst search algorithm
    for i in data["Books"]:
        if str(data['Books'][i]['Title']).lower() == query.lower():

            #get the copies that are being borrowed
            copyNums = []
            for k in range(len(data['Books'][i]['copies'])):
                if data['Books'][i]['copies'][k] == True:
                    copyNums.append(k) 
                else: continue

            #if ever no one has borrowed a copy of the title
            if len(copyNums) == 0:
               print("No students have borrowed a copy of this title")
               continue #because if i used break here, it would search for a borrower

            #make the full id
            fullBookIds = []
            for j in range(len(copyNums)):
                fullBookIds.append(str(i) + copyNums[j])
            
            #find out who has the book
            for user in data['Borrowers']:
                for bookid in fullBookIds:
                    if data['Borrowers'][user]['borrowedBook'] == bookid:
                        copyNum = remove_letters(data['Borrowers'][user]['borrowedBook'])
                        print(f"Student: {data['Borrowers'][user]['borrowerName']} has borrowed {data['Books'][i]['Title']} copy: {copyNum}")

        else: continue #because if i used break here, it would search for a borrower


    #this is just for the borrowers themselves
    for j in data['Borrowers']:
        if data['Borrowers'][j]['borrowerName'].lower() == query.lower():
            if data['Borrowers'][j]['borrowedBook'] != None:
                book = data['Borrowers'][j]['borrowedBook']
                book = remove_numbers(book)
                copyNum = remove_letters(data['Borrowers'][j]['borrowedBook'])

                print(data['Books'][book]['Title'], f'Copy Number: {copyNum}')

            else:
               print("This student hasn't borrowed any books")