import sys
from src.config import CONFIG
from src.logger import logging
from src.exception import MyException
from src.components.processing import AutoCorrector
from src.exception import MyException

class DataProcessingPipeline:
    def __init__(self):
        pass

    @staticmethod
    def main():
        try:
            logging.info(">>>>>Data Preprocessing Started...<<<<<")

            config = CONFIG["DATA_PROCESSING"]
            # Initialize with your corpus
            model = AutoCorrector(corpus_file=config["RAW_DATA"], distance_metric="levenshtein")

            # Get vocab size
            print("Vocabulary Size:", model.get_vocab_size())

            # Get top words
            print("Top words:", model.get_top_words(10))

            # Try autocorrect
            word = "helo"
            result = model.autocorrect(word)
            print(f"Suggestions for '{word}':\n", result)

            logging.info(">>>>>Data Preprocessing Completed<<<<<\n")

        except MyException as e:
            print("Custom exception occurred:", e)

if __name__ == '__main__':
    try:
        logging.info(f"*******************")
        logging.info(f">>>>>> stage Processing started <<<<<<")
        obj = DataProcessingPipeline()
        obj.main()
        logging.info(f">>>>>> stage Processing completed <<<<<<\nx==========x")
    except MyException as e:
            raise MyException(e, sys)
