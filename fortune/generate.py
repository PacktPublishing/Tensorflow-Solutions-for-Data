'''
Generate new machine learning inspired quotes.
'''

import os
import pickle
import numpy as np


def execute(seed_words=[], max_length=32):
    '''
    Generate a single quote.
    
    Parameters
    ----------
    seed_words: list
        A list of words to start off the generation.
    max_length: int
        A guard value to prevent looping forever.

    Returns
    -------
    str
        A single sentence quote
    '''

    # force CPU    
    os.environ["CUDA_VISIBLE_DEVICES"] = ""
    dotfile = os.path.join(os.environ['HOME'], '.machine-learning-fortune')
    default = os.path.join(os.path.dirname(__file__), '.machine-learning-fortune')
    if os.path.exists(dotfile):
        model_path = dotfile
    else:
        model_path = default
    with open(model_path, 'rb') as model_file:
        # get the model back
        model = pickle.load(model_file)
        # pick a random starting word if needed
        if len(seed_words) == 0:
            seed = model.vectorizer.sequencer.inverse_vocabulary_[np.random.randint(0, model.vectorizer.unique_words)]
        else:
            seed = ' '.join(seed_words)
        # build up the result buffer here, adding on to our passed seed
        for i in range(0, max_length):
            # working on the right most context
            X, _ = model.vectorizer.transform([seed])
            context = np.array([X[-1]])
            # only need the very first sample, then keep iterating
            try:
                prediction = model.model.predict(context)[0]
                next_word = model.vectorizer.inverse_transform(prediction)
                # special stop word
                if next_word == 'xxx':
                    break
            except IndexError:
                # when we hit a null character, it is time to exit
                break
            # keep expanding the seed with each word
            seed += ' ' + next_word
        print(seed)