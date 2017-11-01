CZ4045 Assignment: Online Forum Data Processing

0. Download links

- Library used: NLTK

***********************************************************
$ pip install --user --upgrade nltk
$ python -m nltk.downloader all
***********************************************************

- Dataset

The following link contains two folders, raw_data and tagged_data.
Please place these two folders under source_code/, as explained
below.

***********************************************************
https://github.com/nguyenhuyanhh/cz4045/releases/download/release/source_code_data.zip
***********************************************************


1. Project Structure and Documentation

The file structure of this project is as follows:

***********************************************************
source_code/
    raw_data/
        query.sql               # SQL query
        QueryResults.csv        # raw data
                                  (1754 posts)
        TokenTagRaw.csv         # raw annotation data
                                  (100 posts)
        IrregularTokenSent.csv  # irregular tokens
                                  sentences (10)
    tagged_data/
        [100 tagged files]
        Annotation Notes.txt    # some annotation notes
    dataset.py
    stem_and_pos.py
    tokenizer.py
    test.py
    main.py                     # main calling script
report/
    [report materials]
***********************************************************

Calling just the main script (by running $ python source_code/main.py)
would print out this command-line usage:

***********************************************************
$ python source_code/main.py
Invalid arguments! Exiting...
usage: main.py [report|stempos|test|eval|tokenize|
                irregular|commonX]
            report          report dataset stats
            stempos         stemming and POS tagging
                            on dataset
            test            test the tokenizer
            eval            evaluate the tokenizer
                            on annotated dataset
            tokenize        tokenize the dataset,
                            output irregular tokens
            irregular       POS tagging on sentences
                            with irregular tokens
            commonX         get the most common X
                            libraries from the dataset
***********************************************************

2. Sample Project Runs

Reporting of dataset statistics:

***********************************************************
$ python source_code/main.py report
Number of questions: 500
Number of answers: 1254
Average number of answers per questions: 2.508
Questions with 1 answer: 259
Questions with 2 answers: 107
Questions with 3 or more answers: 134
***********************************************************

Stemming and POS tagging on the dataset (there are four separate print outputs
--- 10 random sentences, top 20 words before stemming, top 20 words after
stemming, the original words):

***********************************************************
$ python source_code/main.py stempos
[[('You', 'PRP'), ('are', 'VBP'), ('being', 'VBG'),
('tricked', 'VBN')...]]
[('', 20481), ('I', 947),...]]
[('', 20481), ('I', 947),...]]
[[''], ['I'], ...]]
***********************************************************

Testing of the tokenizer:

***********************************************************
$ python3 source_code/main.py test
................................................
..........................
------------------------------------------------
Ran 74 tests in 0.010s

OK
***********************************************************

Evaluating the tokenizer:

***********************************************************
$ python source_code/main.py eval
...
Id: 38810765, precision: 1.000, recall: 1.000, f1: 1.000
Id: 38834478, precision: 1.000, recall: 1.000, f1: 1.000
Id: 39432272, precision: 0.651, recall: 0.719, f1: 0.683
Id: 40488966, precision: 1.000, recall: 1.000, f1: 1.000
Id: 45003750, precision: 1.000, recall: 1.000, f1: 1.000
Overall: precision: 0.972, recall: 0.976, f1: 0.974
***********************************************************

Outputting irregular tokens from the dataset:

***********************************************************
$ python source_code/main.py tokenize
Using Unix dictionary...
[..., ('Django', 64), ('app', 61)...]
***********************************************************

POS tagging on sentences with irregular tokens:

***********************************************************
$ python source_code/main.py irregular
[('I', 'PRP'), ("'m", 'VBP'), ('using', 'VBG'),
('Google', 'NNP'),...
***********************************************************

Getting the most common libraries from the dataset:

***********************************************************
$ python source_code/main.py common5
[('numpy', 51), ('re', 32), ('sys', 29), ('random', 22),
('os', 22)]
$ python source_code/main.py common10
[('numpy', 51), ('re', 32), ('sys', 29), ('random', 22),
('os', 22), ('collections', 21), ('time', 18), ('pandas',
17), ('csv', 16), ('math', 14)]
***********************************************************
