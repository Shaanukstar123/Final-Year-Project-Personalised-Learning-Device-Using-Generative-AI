import re
import time

sample_text = """
Themes: Nature, Weather
DALL-E Prompt: A sunny day in the forest with animals playing.
STORY: Once upon a time in a beautiful forest, animals enjoyed the sunny day. They played and frolicked among the trees.
Question: What would you like to do on a sunny day in the forest?

"""

def extract_with_regex(text):
    promptRegex = re.compile(r'DALL-e prompt:\s*(.*)', re.IGNORECASE)
    match = promptRegex.search(text)
    if match:
        #print(match.group(0))
        return match.group(1)
    else:
        return None

def cleanResponse(text):
    # Convert text to lower case for consistent searching
    dall_e_prompt = ""
    cleaned_response = ""
    questionPrompt = ""
    text_lower = text.lower()
    dall_e_prompt= re.search(r'DALL-E prompt:\s*(.*)', text, re.IGNORECASE).group(1)
    #remove "DALL-e prompt:" from the text ignoring case
    cleaned_response = re.sub(r'DALL-E Prompt:\s*', '', text, re.IGNORECASE)
    cleaned_response = re.sub(r'DALL-E Prompt:\s*', '', text, re.IGNORECASE)
    questionPrompt = re.search(r'question:\s*(.*)', cleaned_response, re.IGNORECASE)
    return cleaned_response, dall_e_prompt, questionPrompt.group(1)
    # Find start and end indices for each section
    fe_prompt_start = text_lower.find('f-e prompt:')
    story_start = text_lower.find('story:')
    # question_start = text_lower.find('question:')

    # if fe_prompt_start == -1 or story_start == -1 or question_start == -1:
    #     return "", "", text.strip()

    # Extract f-E Prompt
    fe_prompt = text[fe_prompt_start + len('f-e prompt:'):story_start].strip()
    return dall_e_prompt
    #return fe_prompt
    # Extract Question
    # question = text[question_start + len('question:'):].strip()

    # # Extract STORY content
    # story_content = text[story_start + len('story:'):question_start].strip()

    # # Remove other words with colons from STORY content
    # cleaned_response = re.sub(r'\b\w+:\s*', '', story_content)

    # return cleaned_response.strip(), fe_prompt, question

# Performance test
start_time = time.time()
for _ in range(100000):
    extract_with_regex(sample_text)
print("Regex method:", time.time() - start_time)

start_time = time.time()
#for _ in range(100000):

cleanResponse, dall_e_prompt, question = cleanResponse(sample_text)
print("Dal-e prompt:", dall_e_prompt, "Question:", question, "Cleaned response:", cleanResponse)
#print("str.find method:", time.time() - start_time)
