""" This file will help me with data collection """
import wikipediaapi
import wikipedia

# Define a user agent string
USER_AGENT = "langclass (naseda0409@gmail.com)"

# Initialize Wikipedia API with the custom user agent
wiki_en = wikipediaapi.Wikipedia(user_agent=USER_AGENT, language='en')
wiki_nl = wikipediaapi.Wikipedia(user_agent=USER_AGENT, language='nl')

# Function to get a random Wikipedia article
def get_random_article(language):
    if language == 'en':
        wiki = wiki_en
    else:
        wiki = wiki_nl
        wikipedia.set_lang('nl')
        
    random_page = wikipedia.random()
    page = wiki.page(random_page)
    
    return page.text

# Function to extract 15-word segments
def extract_segments(text, num_words=15):
    words = text.split()
    segments = []
    
    for i in range(0, len(words) - num_words + 1, num_words):
        segment = ' '.join(words[i:i+num_words])
        segments.append(segment)
    
    return segments

# Collect data from both English and Dutch Wikipedia
def collect_data(language, num_samples):
    all_segments = []
    
    for _ in range(num_samples):
        article_text = get_random_article(language)
        segments = extract_segments(article_text)
        all_segments.extend(segments)
    
    return all_segments

# Collect 10 random English and Dutch segments
english_segments = collect_data(language='en', num_samples=10)
dutch_segments = collect_data(language='nl', num_samples=10)

# Save data to a file in the required format
def save_to_file(english_segments, dutch_segments, filename='train.dat'):
    with open(filename, 'w') as file:
        # Save English segments with "en" label
        for segment in english_segments:
            file.write(f"en | {segment}\n")
        
        # Save Dutch segments with "nl" label
        for segment in dutch_segments:
            file.write(f"nl | {segment}\n")


print("English Segments:")
for segment in english_segments:
    print(segment)

print("\nDutch Segments:")
for segment in dutch_segments:
    print(segment)

# Save to the train.dat file
save_to_file(english_segments, dutch_segments)

print("Training data saved to 'train.dat'")
# Print collected data

