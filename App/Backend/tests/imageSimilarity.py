import torch
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import requests
from io import BytesIO

# Load CLIP model and processor
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Function to calculate image-text similarity
def calculate_image_text_similarity(image_path, text):
    # Load and preprocess image
    image = Image.open(image_path).convert("RGB")  # Ensure image is in RGB mode

    # Preprocess inputs
    inputs = processor(text=[text], images=image, return_tensors="pt", padding=True, truncation=True)

    # Extract text and image features separately
    text_inputs = {'input_ids': inputs['input_ids'], 'attention_mask': inputs['attention_mask']}
    image_inputs = {'pixel_values': inputs['pixel_values']}

    with torch.no_grad():
        text_features = model.get_text_features(**text_inputs)
        image_features = model.get_image_features(**image_inputs)

    # Normalize the features
    text_features = text_features / text_features.norm(dim=-1, keepdim=True)
    image_features = image_features / image_features.norm(dim=-1, keepdim=True)

    # Calculate cosine similarity
    similarity = torch.matmul(text_features, image_features.T).item()

    # Return similarity score
    return similarity

# Example usage with your data
news_article = "Joe Biden has served as both the president and vice president of the United States..."
generated_story = "The Great Election Adventure: How We Choose Our Leaders In a busy city called London, there lived children who loved to learn about their country. One day, they heard exciting news: there would be a general election! The prime minister, Mr. Sunak, stood outside his home at 10 Downing Street and announced that on Thursday 30 May, parliament would be dissolved. This meant that current Members of Parliament would become ordinary citizens again and had to try to get elected once more. But what exactly is a general election? Let's find out! A general election is when grown-ups all across the United Kingdom decide who they want to represent them in the big building called Parliament. Each area in the UK, like towns and cities, has its own special person called a Member of Parliament, or MP. These MPs speak up for their local area and help make important decisions about our country. Before the election, people who want to become MPs, called candidates, tell everyone why they would be great at the job. They join groups of other people who believe in similar things, called political parties, such as the Conservative Party or the Labour Party. When it's election day, adults go to special places called polling stations to vote. They can vote in person, by post, or even have someone vote for them if they can't go themselves. Everyone needs to show a form of ID to make sure everything is fair. The UK is divided into 650 areas called constituencies, and each one gets to choose its own MP. The most straightforward way to win is to get something called a majority. If a party gets at least 326 MPs elected out of the 650, they have more than half and can form a government. Sometimes, if no party gets a majority, they might work together in a group called a coalition to make decisions together. After all the votes are counted, the results are announced. The newly elected MPs then go to Parliament to start working. There's even a special ceremony, called the State Opening of Parliament, where the King announces what the new government wants to do. So, the children of London learned that a general election is an exciting time when everyone's voice is heard, and they get to choose who represents them in Parliament. It's a big responsibility and a great way to make sure our country keeps running smoothly! And that's how a general election works in the United Kingdom."
image_url = "C:/Users/Shaanu/Desktop/img.webp"

generated_story = "Once upon a time, in the bustling city of Paris, a magical event was about to unfold. It was the year 2024, and the city was adorned with excitement and anticipation as it prepared to host the Olympic Games. Let's embark on a journey to discover what this grand event was all about. In a cozy little neighborhood near the River Seine lived a curious girl named Sophie. Sophie loved sports of all kinds, from running in the park to swimming in the local pool. But what fascinated her the most were the stories her grandfather told her about the Olympics. \"Sophie,\" her grandfather would say, \"the Olympics are a celebration where athletes from all over the world come together to compete in their favorite sports. It's a chance for them to show their skills and make their countries proud.\" Sophie's eyes widened with wonder. \"Grandpa, will there be athletes jumping, swimming, and running all around Paris?" "Absolutely, Sophie,\" her grandfather chuckled. \"In fact, right here in Paris, they'll be setting up special places for different sports. Imagine beach volleyball right by the Eiffel Tower and triathlons starting under the beautiful Alexandre III bridge!\" Sophie giggled with excitement. \"That sounds amazing, Grandpa! But why are they doing it here?" "Well, Sophie, Paris is a city full of history and beauty,\" her grandfather explained. \"The Olympics choose cities like Paris because they have iconic landmarks where athletes can compete in front of the whole world.\" Sophie nodded, imagining herself cheering on athletes as they dashed toward victory beneath the majestic bridges and alongside the sparkling River Seine. As the days passed, Sophie and her friends couldn't wait for the Olympics to begin. They watched on TV as athletes from countries far and wide arrived in Paris. They saw swimmers dive into pools, gymnasts flip and twist, and cyclists race through the streets. One day, Sophie's favorite athlete, a skateboarder named Sky Brown, won a gold medal for her incredible tricks. Sophie jumped up and down, cheering as if she were right there in the skatepark with Sky. But it wasn't just about winning medals. Sophie learned that the Olympics were also about friendship and sportsmanship. Athletes supported each other, even if they were competing against one another. It was about doing your best and celebrating everyone's achievements. On the last day of the Olympics, Sophie and her family gathered around the TV to watch the closing ceremony. They saw fireworks light up the Parisian sky and heard music from around the world. Sophie felt a warm glow in her heart, knowing she had witnessed something truly special. \"Grandpa,\" Sophie whispered as the ceremony ended, \"I want to be an athlete too, just like them.\" Her grandfather smiled proudly. \"Remember, Sophie, you can achieve anything you set your mind to. Just like these athletes, with hard work and determination, you can reach for the stars.\" Sophie nodded, her eyes sparkling with newfound dreams. As the TV showed images of athletes waving and saying goodbye to Paris, Sophie whispered to herself, \"One day, I'll be there too.\" And with that, as the 2024 Olympics came to a close, Sophie knew that the magic of the Games had inspired her to aim high and chase her own dreams, no matter how big they may seem. The End."
##"The Incredible Story of Sight: How Far Can Your Eyes See? Once upon a time, in a school called Hamstel Junior School, a group of curious Year 6 students had a big question: why can our eyes see such long distances? They pondered over this mystery until one day, they decided to seek answers. Their teacher, Mrs. Green, encouraged them to reach out to an expert, so they turned to Dr. Maddy Dann, a TikTok star known for explaining scientific wonders in simple ways. Dr. Maddy Dann was excited to receive their question. She explained that the small spheres in our heads, our eyes, are amazing organs designed to capture light and turn it into images. Through a process called vision, our eyes can perceive objects even at great distances. She shared with the students that our eyes work like cameras, with lenses that focus light onto a special part called the retina. The retina then sends signals to our brain, which interprets them as images. This incredible ability allows us to see everything around us, from nearby objects to faraway mountains and stars in the night sky. The Year 6 students were fascinated by Dr. Dann's explanation. They learned that the science behind sight is both complex and magical. Armed with this newfound knowledge, they continued their studies with a deeper appreciation for the wonders of the human body and the world around them. And so, the mystery of why our eyes can see such long distances was solved, thanks to curious minds and the guidance of a knowledgeable scientist. The students at Hamstel Junior School realized that every question, no matter how big, can lead to amazing discoveries."
# Calculate similarity score
similarity_score = calculate_image_text_similarity(image_url, generated_story)
print(f"Image-Text Similarity Score: {similarity_score}")
