# Define the categories of interest
import random

Originaltopics = [
    # European History
    "Vikings",
    "Romans",
    "Castles",
    "Renaissance",
    "Revolution",
    "Explorers",
    "Plague",
    "Napoleon",
    "Industrial",
    "Kings",
    "Hastings",
    "Berlin",
    "Greece",
    "Stonehenge",
    "Normandy",
    "Elizabeth",
    "Columbus",
    "Hastings",
    "Fire",
    
    # Worldwide Geography
    "Alps",
    "Eiffel",
    "Thames",
    "Vesuvius",
    "Mediterranean",
    "Amazon",
    "Sahara",
    "Everest",
    "Niagara",
    "Andes",
    "Nile",
    "Mississippi",
    "Gobi",
    "Himalayas",
    "Grand Canyon",
    "Caribbean",
    "Antarctica",
    "Rockies",
    "Arctic",
    "Galapagos",
    "Patagonia",
    "Savannah",
    "Pacific",
    "Atlantic",
    
    # Geometry
    "Shapes",
    "Triangles",
    "Circles",
    "Angles",
    "Symmetry",
    "Perimeter",
    "Volume",
    "Lines",
    "Polygons",
    "Tessellations",
    "Coordinates",
    "Patterns",
    "2D Shapes",
    "3D Shapes",
    "Congruence",
    "Similarity",
    
    # Noise Topics
    "Elvis",
    "Pterodactyl",
    "Dinosaur",
    "Presley",
    "Singing",
    "Television",
    "Robots",
    "Dinosaurs",
    "Technology",
    "Chocolate",
    "Robotics",
    "Spacecraft",
    "Space",
    "Nebula",
    "Astronauts",
    "Aliens",
    "Stars"
]


# List of topics
topics = [
    "Viking Adventures in Europe", "Exploring the Roman Empire", "Medieval Castles and Their Secrets",
    "The Renaissance: Art and Science", "The French Revolution: A Turning Point", "Plague: How It Changed History",
    "Napoleon Bonaparte: Rise and Fall", "Industrial Revolution: Inventions and Impact", "Kings and Queens of Europe",
    "The Battle of Hastings Explained", "The Berlin Wall: A Divided City", "Ancient Greece: Myths and Legends",
    "Stonehenge: Mysteries of the Past", "Normandy: The D-Day Invasion", "Queen Elizabeth I: The Virgin Queen",
    "Christopher Columbus: The Explorer", "The Great Fire of London", "The Eiffel Tower: Paris's Icon",
    "Mount Vesuvius: The Eruption", "The Mediterranean Sea: History and Culture", "Amazon Rainforest: The Lungs of the Earth",
    "The Sahara Desert: Survival and Adaptation", "Mount Everest: The Tallest Peak", "Niagara Falls: Nature's Wonder",
    "The Andes Mountains: A Journey", "The Nile River: Lifeblood of Egypt", "The Mississippi River: America's Waterway",
    "The Gobi Desert: Harsh and Beautiful", "The Himalayas: Roof of the World", "The Grand Canyon: Natural Beauty",
    "The Caribbean Islands: Tropical Paradise", "Antarctica: The Frozen Continent", "The Rocky Mountains: Adventure Awaits",
    "The Arctic: Ice and Wildlife", "The Galapagos Islands: Unique Ecosystem", "Patagonia: Land of Extremes",
    "African Savannah: Wildlife and Landscape", "The Pacific Ocean: Vast and Deep", "The Atlantic Ocean: Crossings and Discoveries",
    "Shapes in Geometry: Circles and Triangles", "Understanding Angles and Symmetry", "The Perimeter and Area of Shapes",
    "Volume: Measuring 3D Space", "Lines and Polygons in Geometry", "Tessellations and Patterns",
    "Coordinates and Graphs", "Congruent and Similar Shapes", "Elvis Presley: The King of Rock and Roll",
    "Pterodactyls", "The Art of Ballet",
    "Shakespeare: Plays and Poems", "Robots", "What is AI?"
    "How many dinosaurs do you know?", "Mona Lisa: The Famous Painting", "The Internet", "Football: The Beautiful Game"
]

# Randomly select 45 topics
selected_topics = random.sample(topics, 45)
print("Selected Topics:")
print(selected_topics)



categories_of_interest = {
    "European History": ["Viking Adventures in Europe", "Exploring the Roman Empire", "Medieval Castles and Their Secrets",
                         "The Renaissance: Art and Science", "The French Revolution: A Turning Point", "Plague: How It Changed History",
                         "Napoleon Bonaparte: Rise and Fall", "Industrial Revolution: Inventions and Impact", "Kings and Queens of Europe",
                         "The Battle of Hastings Explained", "The Berlin Wall: A Divided City", "Ancient Greece: Myths and Legends",
                         "Stonehenge: Mysteries of the Past", "Normandy: The D-Day Invasion", "Queen Elizabeth I: The Virgin Queen",
                         "Christopher Columbus: The Explorer", "The Great Fire of London"],
    
    "Worldwide Geography": ["The Eiffel Tower: Paris's Icon", "Mount Vesuvius: The Eruption", "The Mediterranean Sea: History and Culture",
                            "Amazon Rainforest: The Lungs of the Earth", "The Sahara Desert: Survival and Adaptation", "Mount Everest: The Tallest Peak",
                            "Niagara Falls: Nature's Wonder", "The Andes Mountains: A Journey", "The Nile River: Lifeblood of Egypt",
                            "The Mississippi River: America's Waterway", "The Gobi Desert: Harsh and Beautiful", "The Himalayas: Roof of the World",
                            "The Grand Canyon: Natural Beauty", "The Caribbean Islands: Tropical Paradise", "Antarctica: The Frozen Continent",
                            "The Rocky Mountains: Adventure Awaits", "The Arctic: Ice and Wildlife", "The Galapagos Islands: Unique Ecosystem",
                            "Patagonia: Land of Extremes", "African Savannah: Wildlife and Landscape", "The Pacific Ocean: Vast and Deep",
                            "The Atlantic Ocean: Crossings and Discoveries"],
    
    "Geometry": ["Shapes in Geometry: Circles and Triangles", "Understanding Angles and Symmetry", "The Perimeter and Area of Shapes",
                 "Volume: Measuring 3D Space", "Lines and Polygons in Geometry", "Tessellations and Patterns",
                 "Coordinates and Graphs", "Congruent and Similar Shapes"]
}

# Classify topics
def classify_topic(topic):
    for category, topics_list in categories_of_interest.items():
        if topic in topics_list:
            return category
    return "Noise"

# Evaluate the classification
classified_topics = [classify_topic(topic) for topic in selected_topics]

# Count how many topics fit each category
category_counts = {
    "European History": 0,
    "Worldwide Geography": 0,
    "Geometry": 0,
    "Noise": 0
}

for category in classified_topics:
    category_counts[category] += 1

print("Category Counts:")

print(category_counts)
print(len(Originaltopics))
