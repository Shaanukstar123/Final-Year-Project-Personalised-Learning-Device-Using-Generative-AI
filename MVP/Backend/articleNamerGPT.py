from openai import OpenAI
import json

client = OpenAI(api_key='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')
messages = [
    {"role": "system", "content": "You are a topic chooser for a children's app. "
     +"Given a list of article names, choose the articles that best represent topics around the world that "
     + "kids should know. Replace the names with a 1 word topic name, and the other names replace with '_' "
      +"and return in the same format. The topics should be very basic but also informative. E.g. Article about National Cinema Day = 'Cinema'"}
]
# def filterArticles(names):
#     prompt = "Only output a string list of names, not content: These articles are web scraped so some may not be relevant or even full articles at all. Some are quizes and some are descriptions or videos. Please filter out any of them by replacing their names with '_' and return a list of just names in the same order and same names apart from the _ . Articles: "
#     messages.append({"role": "user", "content": prompt+ names})
#     chat = client.chat.completions.create(
#             model="gpt-3.5-turbo-1106",
#             messages=messages
#         )
#     print("ChatGPT: " + chat.choices[0].message.content)
#     return chat.choices[0].message.content

def generate_title_with_gpt(names):
    messages.append({"role": "user", "content": names})
    chat = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages
        )
    reply = chat.choices[0].message.content

    return (f"ChatGPT: {reply}")

# Example usage with a JSON file containing articles
with open('webCrawler/output.json', 'r') as file:
    ##takes in a list of articles and outputs a dictionary names:content in comma separated format
    articles = json.load(file)
    nameList = ""
    jsonInString = ""
    for article in articles:
        nameList += article['name'] + ", "
        jsonInString += json.dumps(article) + ", "


# names = filterArticles(nameList)
# print(names)
print(generate_title_with_gpt(nameList))

# Output the modified data with new GPT-generated titles
#print(json.dumps(articles, indent=2))
