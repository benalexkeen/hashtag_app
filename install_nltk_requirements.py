import os
import nltk

from config import NLTK_DATA_DIR


def install_nltk_requirements():
    if not os.path.exists(NLTK_DATA_DIR):
        os.makedirs(NLTK_DATA_DIR)
    nltk.download('punkt', download_dir=NLTK_DATA_DIR)
    nltk.download('averaged_perceptron_tagger', download_dir=NLTK_DATA_DIR)


if __name__ == "__main__":
    install_nltk_requirements()