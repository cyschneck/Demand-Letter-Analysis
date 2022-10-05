# Anti-Racism Demand Letters Analysis
2020 Anti-Racism Demand Letters Analysis

## Dependencies
Requires Python 3.7.3

```
easyocr==1.5.0
nltk==3.7
pdf2image==1.16.0
Pillow==9.1.1
PyPDF2==2.3.1
pytesseract==0.3.7
python-docx==0.8.11
torchvision==0.12.0
```

Additional dependencies can downloaded via terminal

```
pip install -r requirements.txt
```

## How to Run

### Download Letters
Download letters into a child directory below `demand_letters`

### Run Pre-Processing Script
Run pre-processing script to convert .docx and .pdf files to a .txt output file

```python
python3 pre_processing_demand_letters.py
```

Result of execution will produce x number of files based on the child directories beneath the root `demand_letters` directory. One file output will be generated for each child directory with the combined output of all the letters/files within the child directory

### Analysis
Run NPL Script to read from `demand_letters_output` to produce NPL analysis results

```python
python3 npl_analysis.py
```
Overview Per Text File Results: (Example from 2020_letters.txt)

#### Word Frequency
![word_frequency+png](https://github.com/cyschneck/Demand-Letter-Analysis/blob/main/demand_letters_output/2020_letters_frequency_dist.png)

#### Co-Occurrence in Letters
![bigram+png](https://github.com/cyschneck/Demand-Letter-Analysis/blob/main/demand_letters_output/2020_letters_frequency_dist_bigrams.png)
![trigram+png](https://github.com/cyschneck/Demand-Letter-Analysis/blob/main/demand_letters_output/2020_letters_frequency_dist_trigrams.png)
![quadgram+png](https://github.com/cyschneck/Demand-Letter-Analysis/blob/main/demand_letters_output/2020_letters_frequency_dist_quadgrams.png)

#### Sentiment Analysis
Postive Sentiment
![postive_sentiment+png](https://github.com/cyschneck/Demand-Letter-Analysis/blob/main/demand_letters_output/2020_letters_postive_sentiment.png)
Negative Sentiment
![negative_sentiment+png](https://github.com/cyschneck/Demand-Letter-Analysis/blob/main/demand_letters_output/2020_letters_negative_sentiment.png)
Trends in Sentiment
![trends_sentiment+png](https://github.com/cyschneck/Demand-Letter-Analysis/blob/main/demand_letters_output/2020_letters_pos_and_neg_sentiment.png)

## Compare Between Text Files
![comparisions_single+png](https://github.com/cyschneck/Demand-Letter-Analysis/blob/main/demand_letters_output/comparisons_single.png)
![comparisions_bigrams+png](https://github.com/cyschneck/Demand-Letter-Analysis/blob/main/demand_letters_output/comparisons_bigrams.png)
![comparisions_trigrams+png](https://github.com/cyschneck/Demand-Letter-Analysis/blob/main/demand_letters_output/comparisons_trigrams.png)
![comparisions_quadgramss+png](https://github.com/cyschneck/Demand-Letter-Analysis/blob/main/demand_letters_output/comparisons_quadgrams.png)
