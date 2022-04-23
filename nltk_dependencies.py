import nltk
import os

# This script downloads necessary NLTK data to the resources/nltk folder

nltk_resources_dir = os.path.join(os.getcwd(), 'resources/nltk/')

for dependency in ['wordnet', 'omw-1.4', 'punkt', 'stopwords']:
    nltk.download(dependency, nltk_resources_dir)

