import shutil

import nltk
import os


# This script downloads necessary NLTK docs to the resources/nltk folder
def setup_dependencies():
    """
    This script downloads necessary NLTK docs to the resources/nltk folder
    :return:
    """
    script_dir = os.path.dirname(os.path.realpath(__file__))
    nltk_resources_dir = os.path.join(script_dir, 'resources/nltk/')
    for dependency in ['wordnet', 'omw-1.4', 'punkt', 'stopwords']:
        nltk.download(dependency, nltk_resources_dir)

    # Manually copy all files from stopwords directory to nltk/corpora/stopwords
    for file in os.listdir(os.path.join(script_dir, 'resources/stopwords/')):
        print(f'Copying file: "{file}" to "{script_dir}/nltk/corpora/stopwords"')
        shutil.copy(os.path.join(script_dir, 'resources/stopwords', file),
                    os.path.join(script_dir, 'resources/nltk', 'corpora/stopwords'))


if __name__ == '__main__':
    setup_dependencies()
