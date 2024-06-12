# Import the necessary libraries
import spacy
import matplotlib.colors as mcolors

# Load the spacy model
nlp = spacy.load('en_core_web_md')


import matplotlib.colors as mcolors

def get_colour_for_topic(topic):
    # Define a list of reference colors and their corresponding concepts
    reference_colors = {
        'limegreen': 'nature environment ecology growth renewal tree forest plant biology life science geography recycling',
        'deepskyblue': 'water ocean sky tranquility stability trust mathematics pythagoras geometry calculation numbers logic analysis technology computer science physics chemistry astronomy',
        'tan': 'history old ancient tradition earthiness archaeology artifacts culture social studies',
        'gold': 'science discovery experiment wealth luxury innovation research engineering invention robotics',
        'tomato': 'passion love excitement energy intensity power physical education sports health exercise activity celebrations parties festivals holidays',
        'khaki': 'happiness sunshine optimism warmth cheerfulness vibrancy creativity art drawing painting ',
        'orange': 'enthusiasm creativity success encouragement vitality friendliness warmth literature reading writing storytelling language arts',
        'mediumorchid': 'royalty wisdom dignity ambition spirituality mystery elegance sophistication music melody instruments choir drama theater',
        'orchid': 'elegance power sophistication mystery strength formality debate philosophy logic critical thinking problem solving',
        'lavender': 'purity simplicity innocence cleanliness safety',
        'pink': 'playfulness fun excitement creativity art drawing painting cheerfulness warmth friendliness imagination',
        'lightseagreen': 'neutrality balance simplicity practicality durability study homework assignments general subjects classroom'
    }

    topic_doc = nlp(topic)
    max_similarity = -1
    best_color = 'dimgray'  # Default color

    for color, concepts in reference_colors.items():
        concept_doc = nlp(concepts)
        similarity = topic_doc.similarity(concept_doc)
        if similarity > max_similarity:
            max_similarity = similarity
            best_color = color

    return mcolors.to_hex(best_color)