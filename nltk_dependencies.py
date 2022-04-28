import nltk
import os


# This script downloads necessary NLTK docs to the resources/nltk folder
def download_dependencies():
    nltk_resources_dir = os.path.join(os.getcwd(), 'resources/nltk/')
    for dependency in ['wordnet', 'omw-1.4', 'punkt', 'stopwords']:
        nltk.download(dependency, nltk_resources_dir)


if __name__ == '__main__':
    download_dependencies()
