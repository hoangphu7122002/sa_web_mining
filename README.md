# Vietnamese Sentiment Analysis on Technical Reviews

This repository contains the implementation of sentiment analysis on Vietnamese technical reviews as part of a Web Mining course project. The analysis focuses on classifying Vietnamese reviews into positive, negative, or neutral sentiments.

## Project Structure 
```
|── data_preprocessing/
│ ├── train.csv
│ ├── test.csv
│ ├── train_unmarked.csv
│ └── test_unmarked.csv
|── vlsp/
│ ├── vlsp_sentiment_train.csv
│ ├── vlsp_sentiment_test.csv
├── text_processor.py
├── teencode.txt
├── single_word_dict.json
├── README.md
└── .gitignore
```

## Dataset

The dataset is from VLSP Shared Task: Sentiment Analysis, containing comments collected from three main sources:

| Source | Quantity |
|--------|-----------|
| tinhte.vn | 2,710 |
| vnexpress.net | 7,998 |
| facebook | 1,488 |
| **Total** | **12,190** |

After annotation and filtering:
- Training set: 5,100 comments (1,700 per label)
- Test set: 1,050 comments (350 per label)

## Text Preprocessing

The preprocessing pipeline includes:
- URL removal
- Number normalization
- Vietnamese text normalization
- Case conversion
- Duplicate character removal
- Whitespace normalization
- Repeated word removal
- Punctuation normalization
- Emoticon/symbol conversion
- Acronym expansion
- Special character removal
- Optional diacritics removal

## Approaches

### 1. Data Variants
- With diacritics
- Without diacritics

### 2. Models and Embeddings

1. Baseline
   - Naive Bayes classifier

2. TF-IDF and Tokenization Based Models
   - SGD Classifier
   - SVM
   - LSTM
   - CNN

3. Word2Vec CBOW Based Models
   - CRNN
   - LSTM
   - BiLSTM

## Benchmark Results

### With Diacritics

| Model | Accuracy | Precision | Recall | F1 Score |
|-------|----------|-----------|---------|-----------|
| Naive Bayes | 0.339048 | 0.287803 | 0.339048 | 0.187628 |
| XGBoost | 0.571429 | 0.584342 | 0.571429 | 0.570524 |
| SVM | 0.487619 | 0.487089 | 0.487619 | 0.485965 |
| Logistic Regression | 0.506667 | 0.507328 | 0.506667 | 0.506800 |
| TF-IDF LSTM | 0.306667 | 0.333333 | 0.102222 | 0.156463 |
| TF-IDF BiLSTM | 0.294286 | 0.333333 | 0.098095 | 0.151582 |
| CRNN | 0.558095 | 0.571241 | 0.558095 | 0.536349 |
| CNN | 0.601905 | 0.637462 | 0.601905 | 0.567582 |
| LSTM | 0.567619 | 0.582836 | 0.567619 | 0.545919 |

### Without Diacritics

| Model               | Accuracy | Precision | Recall  | F1 Score |
|---------------------|----------|-----------|---------|----------|
| Naive Bayes         | 0.337143 | 0.275386  | 0.337143 | 0.183168 |
| Tokenization_SGD    | 0.328571 | 0.281520  | 0.328571 | 0.273479 |
| Tokenization_SVM    | 0.366667 | 0.371823  | 0.366667 | 0.364633 |
| TF-IDF sgd          | 0.709524 | 0.710426  | 0.709524 | 0.709571 |
| TF-IDF SVM          | 0.685714 | 0.698842  | 0.685714 | 0.686470 |
| RandomForest        | 0.566667 | 0.587268  | 0.566667 | 0.555761 |
| logistic_regression | 0.682857 | 0.694894  | 0.682857 | 0.683694 |
| TF_IDF_LSTM         | 0.588571 | 0.589586  | 0.588571 | 0.588332 |
| TF_IDF_BiLSTM       | 0.580952 | 0.581409  | 0.580952 | 0.578652 |
| Word2Vec CRNN       | 0.552381 | 0.593979  | 0.552381 | 0.548128 |
| Word2Vec CNN        | 0.638095 | 0.639312  | 0.638095 | 0.636116 |

## Requirements

```
python>=3.8
underthesea
scikit-learn
tensorflow
gensim
numpy
pandas
xgboost
```

## Usage

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run preprocessing: `python text_processor.py`
4. Train and evaluate models: `python train.py`

## License

MIT License
