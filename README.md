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

| Model               | Accuracy  | Precision | Recall    | F1 Score  |
|---------------------|-----------|-----------|-----------|-----------|
| Tokenization_SGD    | 0.313333  | 0.316661  | 0.313333  | 0.305519  |
| Tokenization_SVM    | 0.376190  | 0.376952  | 0.376190  | 0.373842  |
| TF-IDF SGD          | 0.724762  | 0.725895  | 0.724762  | 0.724948  |
| TF-IDF SVM          | 0.703810  | 0.715450  | 0.703810  | 0.704789  |
| RandomForest        | 0.554286  | 0.611744  | 0.554286  | 0.536791  |
| Logistic Regression | 0.704762  | 0.715388  | 0.704762  | 0.705743  |
| TF-IDF LSTM         | 0.583810  | 0.583654  | 0.583810  | 0.581167  |
| TF-IDF BiLSTM       | 0.562857  | 0.567537  | 0.562857  | 0.563241  |
| Word2Vec CRNN       | 0.642857  | 0.641604  | 0.642857  | 0.638519  |
| Word2Vec CNN        | 0.686667  | 0.692828  | 0.686667  | 0.681288  |
| Naive Bayes         | 0.339048  | 0.287803  | 0.339048  | 0.187628  |

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

## Conclusions and Future Work



Based on our experimental results, we can draw several key conclusions:



1. **Best Performing Model**: TF-IDF + SGD with diacritics version shows the most promising results, balancing both performance and computational efficiency.



2. **Diacritics Impact**: Models consistently perform better with diacritical marks preserved, suggesting that Vietnamese tone markers carry significant semantic information for sentiment analysis.



3. **Deep Learning Limitations**: Despite their theoretical capabilities, deep learning models (LSTM, CNN) didn't show superior performance, likely due to:

   - Limited dataset size

   - Class imbalance issues

   - Insufficient training examples for complex pattern recognition



4. **Resource Constraints**: Our experiments were conducted using Google Colab's T4 GPU, which limited our ability to:

   - Train larger models

   - Perform extensive hyperparameter tuning

   - Test more sophisticated architectures



## Future Directions



1. **Data Enhancement**:

   - Expand the dataset through additional crawling

   - Implement data augmentation techniques

   - Improve data quality and balance



2. **Advanced Models**:

   - Experiment with Vietnamese-specific BERT models

   - Explore LLM-based approaches

   - Investigate transfer learning from larger Vietnamese language models



3. **Infrastructure**:

   - Scale up computational resources

   - Optimize model architectures for better resource utilization

   - Implement distributed training strategies


## Usage

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run preprocessing: `python text_processor.py`
4. Train and evaluate models: `python train.py`

## License

MIT License
