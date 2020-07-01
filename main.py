import pymongo
import inquirer
import os
import sys
import re
sys.path.append(os.path.realpath('.'))
from pprint import pprint
from inquirer import errors

myclient = pymongo.MongoClient(port =27017)

mydb = myclient["mydatabase"]

mycol = mydb["testing1"]


questions = [
    inquirer.List('operation',
                  message="Which operation do you need?",
                  choices=['Create', 'Read', 'Update', 'Delete'],
              ),
]

operation = inquirer.prompt(questions)
pprint(operation)
if operation['operation'] == 'Create':
    questions = [
    inquirer.List('count',
                  message="How many data do you want to insert?",
                  choices=['One', 'Many'],
              ),
    ]

    count = inquirer.prompt(questions)
    pprint(count) 

    if count['count'] == 'One':
        
        questions = [
            inquirer.Text('name',
                        message="What's your name?"),
            inquirer.Text('address',
                        message="What's your address, {name}?")
        ]
        answers = inquirer.prompt(questions)
        pprint(answers)
        mydict = {
            'name':answers['name'],
            'address': answers['address']
            }
        x = mycol.insert_one(mydict)
    else:
        questions = [
            inquirer.Text('size',
                        message="How many fields do you want to add?"),
            
        ]
        answers = inquirer.prompt(questions)
        mylist = []
        try:
            for i in range(0, int(answers['size'])):
                questions = [
                    inquirer.Text('name',
                        message="What's your name?"),
                    inquirer.Text('address',
                        message="What's your address, {name}?")
                ]
                answers = inquirer.prompt(questions)
                x = mycol.insert_one(answers)
               
        except ValueError:
            print("Not an integer")

elif operation['operation'] == 'Read': 
    questions = [
    inquirer.List('count',
                  message="How many data do y0u want to read?",
                  choices=['One', 'Many'],
              ),
    ]
    count = inquirer.prompt(questions)
    if count['count'] == 'One':
        x = mycol.find_one({},{ "_id": 0, "name": 1, "address": 1 })
        print(x)
    else:
        for i in mycol.find({},{ "_id": 0, "name": 1, "address": 1 }):
            print(i)

elif operation['operation'] == 'Update':
    questions = [
    inquirer.List('count',
                  message="How many data do y0u want to update?",
                  choices=['One', 'Many'],
              ),
    ]

    count = inquirer.prompt(questions)
    pprint(count) 
    if count['count'] == 'One':
        questions = [
        inquirer.List('field',
                    message="Which field do you want to update?",
                    choices=['name', 'address'],
                ),
        ]
        field = inquirer.prompt(questions)
        pprint(field) 
        if field['field'] == 'name':
            questions = [
                    inquirer.Text('address',
                        message="Choose the name of address field that you want to change name"),
                    inquirer.Text('name',
                        message="Enter the name")
            ]
            answers = inquirer.prompt(questions)
            mycol.update_one({'address': answers['address']}, {'$set': {'name': answers['name']}})
            
        else:
            questions = [
                    inquirer.Text('name',
                        message="Choose the name of name field that you want to change address"),
                    inquirer.Text('address',
                        message="Enter the address")
            ]
            answers = inquirer.prompt(questions)
            mycol.update_one({'name': answers['name']}, {'$set': {'address': answers['address']}})
            
    else:
        questions = [
        inquirer.List('field',
                    message="Which field do you want to update?",
                    choices=['name', 'address'],
                ),
        ]
        field = inquirer.prompt(questions)
        pprint(field) 
        if field['field'] == 'name':
            questions = [
                    inquirer.Text('address',
                        message="Choose the name of address field that you want to change name"),
                    inquirer.Text('name',
                        message="Enter the name")
            ]
            answers = inquirer.prompt(questions)
            mycol.update_many({'address': answers['address']}, {'$set': {'name': answers['name']}})
            
        else:
            questions = [
                    inquirer.Text('name',
                        message="Choose the name of name field that you want to change address"),
                    inquirer.Text('address',
                        message="Enter the address")
            ]
            answers = inquirer.prompt(questions)
            mycol.update_many({'name': answers['name']}, {'$set': {'address': answers['address']}})
            
        
elif  operation['operation'] == 'Delete': 
    questions = [
    inquirer.List('size',
                  message="How many data do y0u want to delete?",
                  choices=['One', 'Many','Delete all document in collection', 'Delete collection'],
              ),
    ]

    count = inquirer.prompt(questions)
    pprint(count) 
    if count['size'] == 'One':
        questions = [
        inquirer.List('field',
                    message="According to which field do you want to delete?",
                    choices=['name', 'address'],
                ),
        ]
        field = inquirer.prompt(questions)
        pprint(field) 
        if field['field'] == 'name':
            questions = [
                    inquirer.Text('name',
                        message="Enter the name")
            ]
            answers = inquirer.prompt(questions)
            mycol.delete_one( {"name": answers['name'] })
            
        else:
            questions = [
                    inquirer.Text('address',
                        message="Enter the address")
            ]
            answers = inquirer.prompt(questions)
            mycol.delete_one({"address": answers['address']} )
            
    elif count['size'] == 'Many':
        questions = [
        inquirer.List('field',
                    message="According to which field do you want to delete?",
                    choices=['name', 'address'],
                ),
        ]
        field = inquirer.prompt(questions)
        pprint(field) 
        if field['field'] == 'name':
            questions = [
                    inquirer.Text('name',
                        message="Enter the name")
            ]
            answers = inquirer.prompt(questions)
            mycol.delete_many( {"name": answers['name'] })
            
        else:
            questions = [
                    inquirer.Text('address',
                        message="Enter the address")
            ]
            answers = inquirer.prompt(questions)
            mycol.delete_many({"address": answers['address']} )

    elif count['size'] == 'Delete all document in collection':
        x = mycol.delete_many({})
        print(x.deleted_count, " documents deleted.")

    elif count['size'] == 'Delete collection':
        mycol.drop()