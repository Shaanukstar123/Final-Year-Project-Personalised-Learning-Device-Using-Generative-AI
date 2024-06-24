# Import the necessary libraries
import spacy
import matplotlib.colors as mcolors

# Load the spacy model
nlp = spacy.load('en_core_web_md')

def batch_get_colors(topics):
    reference_colors = {
        'limegreen': 'adventure nature pollution animals environment ecology growth renewal tree forest plant biology life biology geography recycling maps world amazon ',
        'deepskyblue': 'sports space football problems mathematics pythagoras geometry arithmetic calculation numbers logic analysis technology computer robotics physics chemistry astronomy future',
        'lightblue': 'ice cold snow freezing winter arctic antarctic',
        'tan': 'history old ancient tradition  archaeology artifacts culture desert sahara ',
        'gold': 'experiment wealth luxury innovation research engineering invention celebrity fame success prosperity',
        'darkgoldenrod': 'ground soil rocks tectonics mining depression',
        'tomato': 'passion love excitement energy intensity power physical education sports health exercise activity celebrations parties festivals holidays',
        'khaki': 'happiness sunshine optimism  vibrancy art drawing painting ',
        'orange': 'enthusiasm creativity creative success encouragement vitality friendliness warmth literature reading writing storytelling language arts',
        'mediumorchid': 'royalty wisdom dignity ambition spirituality mystery elegance sophistication music melody instruments choir drama theater',
        'hotpink': 'elegance femininity',
        'lavender': 'purity simplicity innocence cleanliness safety flowers',
        'pink': 'playfulness fun excitement creativity art drawing painting cheerfulness imagination love',
        'lightseagreen': 'neutrality balance simplicity practicality durability study homework assignments general subjects classroom',
        'orangered': 'fire heat strength power danger excitement  passion anger aggression war conflict volcanoes lava magma',
        'skyblue': 'calmness stability trust loyalty intelligence wisdom confidence truth faith heaven water river nile ocean sky tranquility tsunami flood rain '
    }

    #topic_docs = list(nlp.pipe(topics))
    topics_lower = [topic.lower() for topic in topics]
    topic_docs = list(nlp.pipe(topics_lower))
    concept_docs = {color: nlp(concepts) for color, concepts in reference_colors.items()}

    topics_with_colors = []

    for topic, topic_doc in zip(topics, topic_docs):
        max_similarity = -1
        best_color = 'dimgray'  # Default color

        for color, concept_doc in concept_docs.items():
            similarity = topic_doc.similarity(concept_doc)
            if similarity > max_similarity:
                max_similarity = similarity
                best_color = color

        topics_with_colors.append({"topic": topic, "color": mcolors.to_hex(best_color)})

    return topics_with_colors