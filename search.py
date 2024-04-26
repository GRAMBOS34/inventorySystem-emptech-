import json

def remove_numbers(text):
    """Removes numbers from the id"""
    return "".join([char for char in text if not char.isdigit()])

def remove_letters(text):
    """Removes letters from the id"""
    return "".join(filter(str.isdigit, text))


if __name__ == "__main__":
    while True:
        noBook = False
        query = str(input("Search inventory: "))
        with open('data.json', "r+") as file:
            data = json.load(file)
            numOfCopiesNotBorrowed = 0

            #god's worst search algorithm
            for i in data["Books"]:
                if str(data['Books'][i]['Title']).lower() == query.lower():
                
                    #get the copies that are being borrowed
                    copyNums = []
                    for k in range(len(data['Books'][i]['copies'])):
                        if data['Books'][i]['copies'][str(k)] == True:
                            copyNums.append(k) 
                        else:
                            numOfCopiesNotBorrowed = numOfCopiesNotBorrowed + 1 #adds 1 if a copy is not being borrowed
                            continue

                    #if ever no one has borrowed a copy of the title
                    if len(copyNums) == 0:
                        print("No students have borrowed a copy of this title")
                        continue #because if i used break here, it would search for a borrower

                    #make the full id
                    fullBookIds = []
                    for j in range(len(copyNums)):
                        fullBookIds.append(str(i) + str(copyNums[j]))
                    
                    #find out who has the book
                    for user in data['Borrowers']:
                        for bookid in fullBookIds:
                            if data['Borrowers'][user]['borrowedBook'] == bookid:
                                copyNum = remove_letters(data['Borrowers'][user]['borrowedBook'])
                                print(f"Student: {data['Borrowers'][user]['borrowerName']} has borrowed {data['Books'][i]['Title']} copy: {copyNum}")
                                print(f"Number of copies of this book not borrowed: {numOfCopiesNotBorrowed}")

                    noBook = noBook #because for some reason python wont detect this as a call for the noBook variable declared at the top
                    break

                if query.lower() not in str(data['Books'][i]['Title']).lower():
                    #done like this so the value won't alternate
                    if noBook == True:
                        continue

                    else:
                        noBook = not noBook
                        continue

            #this is just for the borrowers themselves
            for j in data['Borrowers']:
                if query.lower() not in data['Borrowers'][j]['borrowerName'].lower():
                    #so the value won't alternate
                    if noBook == True:
                        continue

                    else:
                        noBook = not noBook
                        continue

                if data['Borrowers'][j]['borrowerName'].lower() == query.lower():
                    if data['Borrowers'][j]['borrowedBook'] != None:
                        book = data['Borrowers'][j]['borrowedBook']
                        book = remove_numbers(book)
                        copyNum = remove_letters(data['Borrowers'][j]['borrowedBook'])

                        print(data['Books'][book]['Title'], f'Copy Number: {copyNum}')
                        noBook = not noBook #because if it gets out here this value will be true
                        break

                    else:
                        print("This student hasn't borrowed any books")
                        noBook = not noBook #because if it gets out here this value will be true
                        break
            
            #placed here so that the next loop wont execute without passing through this check first
            #its like this because if there is no book, there is a guarantee that there is no borrower
            #after all, how will you borrow something that doesnt exist?
            if noBook == True:
                #if it goes here then the search term doesn't exist
                print("The item you are searching for does not exist.")
                continue