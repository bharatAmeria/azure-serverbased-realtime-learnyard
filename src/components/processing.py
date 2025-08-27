from src.logger import logging
from src.exception import MyException
import sys
import re
import pandas as pd
from collections import Counter
import textdistance
from functools import lru_cache


class AutoCorrector:
    def __init__(self, corpus_file: str, distance_metric="levenshtein"):
        """
        :param corpus_file: path to text corpus
        :param distance_metric: similarity metric (levenshtein | jaccard | hamming)
        """
        try:
            self.corpus_file = corpus_file
            self.words = []
            self.V = set()
            self.words_freq_dict = {}
            self.probs = {}
            self.distance_metric = distance_metric
            logging.info(f"Initializing AutoCorrector with corpus: {corpus_file} "
                         f"and distance metric: {distance_metric}")
            self._load_corpus()
        except Exception as e:
            logging.error(f"Error initializing AutoCorrector: {e}")
            raise MyException(e, sys)

    def _load_corpus(self):
        """Load text data, preprocess, and build vocabulary + probabilities"""
        try:
            with open(self.corpus_file, 'r', encoding='utf-8') as f:
                data = f.read().lower()
                self.words = re.findall(r'\w+', data)
                self.words += self.words  # duplicate list as per original logic

            self.V = set(self.words)
            self.words_freq_dict = Counter(self.words)

            total = sum(self.words_freq_dict.values())
            self.probs = {k: self.words_freq_dict[k] / total for k in self.words_freq_dict}

            logging.info(f"Corpus loaded successfully. "
                         f"Total words: {len(self.words)}, Vocab size: {len(self.V)}")

        except FileNotFoundError as fnf:
            logging.error(f"Corpus file not found: {self.corpus_file}")
            raise MyException(f"Corpus file not found: {self.corpus_file}") from fnf
        except Exception as e:
            logging.error(f"Error loading corpus: {e}")
            raise MyException(e, sys)

    def get_vocab_size(self):
        """Return vocabulary size"""
        try:
            size = len(self.V)
            logging.info(f"Vocabulary size: {size}")
            return size
        except Exception as e:
            logging.error(f"Error fetching vocab size: {e}")
            raise MyException(e)

    def get_top_words(self, n=10):
        """Return top n frequent words"""
        try:
            top_words = self.words_freq_dict.most_common(n)
            logging.info(f"Top {n} words: {top_words}")
            return top_words
        except Exception as e:
            logging.error(f"Error fetching top words: {e}")
            raise MyException(e, sys)

    def _similarity(self, w1, w2):
        """Compute similarity score between two words"""
        try:
            if self.distance_metric == "levenshtein":
                dist = textdistance.Levenshtein().normalized_distance(w1, w2)
                return 1 - dist
            elif self.distance_metric == "jaccard":
                return 1 - textdistance.Jaccard(qval=2).distance(w1, w2)
            elif self.distance_metric == "hamming":
                if len(w1) != len(w2):
                    return 0
                return 1 - textdistance.Hamming().normalized_distance(w1, w2)
            else:
                logging.error(f"Unsupported distance metric: {self.distance_metric}")
                raise MyException(f"Unsupported distance metric: {self.distance_metric}")
        except Exception as e:
            logging.error(f"Error computing similarity: {e}")
            raise MyException(e, sys)

    @lru_cache(maxsize=1000)
    def autocorrect(self, word: str, top_k: int = 3):
        """
        Suggest corrections for a given word
        :param word: input word
        :param top_k: number of suggestions to return
        """
        try:
            word = word.lower()
            logging.info(f"Autocorrect called for word: '{word}'")

            if word in self.V:
                logging.info(f"Word '{word}' is correct.")
                return f"✅ Word is correct: {word}"

            candidates = [w for w in self.words_freq_dict if abs(len(w) - len(word)) <= 2]

            if not candidates:
                logging.warning(f"No candidates found for word: {word}")
                return f"No suggestions found for: {word}"

            similarities = [(w, self._similarity(w, word)) for w in candidates]

            sorted_candidates = sorted(
                similarities,
                key=lambda x: (x[1], self.probs[x[0]]),
                reverse=True
            )

            output = pd.DataFrame(
                [(w, self.probs[w], sim) for w, sim in sorted_candidates[:top_k]],
                columns=["Word", "Prob", "Similarity"]
            )

            logging.info(f"Suggestions for '{word}': {output.to_dict(orient='records')}")
            return output

        except Exception as e:
            logging.error(f"Error in autocorrect for word '{word}': {e}")
            raise MyException(e, sys)
