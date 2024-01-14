##These functions summarise articles in one word using the GPT api

from openai import OpenAI
import json

client = OpenAI(api_key='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')
messages = []
role= {"role": "system", "content": "You are a topic chooser for a children's app. "
     +"Given a list of article names and id, choose the articles that best represent trending topics around the world that "
     + "kids would find interesting. Replace the names with a trending topic name and the other names replace with '_'. The name should represent what's trending around the world today relating to this news."
      +"Return in the same format and length. The topics should be very basic but also informative. E.g. Article about National Cinema Day = 'Cinema'. Return list of id: new name"}

def generateTitleWithGPT(articles):
    dictToString = ""
    for i in articles:
        dictToString += str(i['id']) + ":" + i['name'] + ", "
    messages.append({"role": "user", "content": dictToString})
    messages.append(role)
    chat = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages
        )
    reply = chat.choices[0].message.content

    return (reply)

def getArticles(dir):
    with open(dir, 'r') as file:
        ##takes in a list of articles and outputs a dictionary names:content in comma separated format
        articles = json.load(file)
        nameList = {} #id:name
        for article in articles:
            nameList[article['id']] = article['name']
    return articles

def addNewNames(nameList, dir):
    if "\n" in nameList:
        nameList = nameList.split('\n')
    else:
        nameList = nameList.split(',')
    articleDict = {}
    for i in nameList:
        i = i.split(':')
        if len(i)>1:
            articleDict[int(i[0])] = i[1]
    print("New: ",nameList)
    ##Overwrites the output.json file with the new names. Indexes are the same
    with open(dir, 'r') as file:
        articles = json.load(file)
        for id in articleDict:
            print(id)
            for article in articles:
                if article['id'] == id:
                    article['new_title'] = articleDict[id]
                    print (article['new_title'])
    with open(dir, 'w') as file:
        json.dump(articles, file, indent=2)

def generateNewNames():
    dir = 'data/output.json'
    articles = getArticles(dir)
    newNames = generateTitleWithGPT(articles)
    addNewNames(newNames, dir)

generateNewNames()
