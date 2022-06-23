# Anti-Racism Demand Letters Analysis
2020 Anti-Racism Demand Letters Analysis

_Note_: demand_letters directory is empty to preserve privacy (controlled in the .gitignore)

## Dependencies
Requires Python 3.7.3

```
Pillow==6.0.0
pdf2image==1.16.0
pytesseract==0.3.7
python-docx==0.8.11
PyPDF2==2.3.1
```

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
TODO: Word Frequency

TODO: Changes in Word Usage

TODO: Co-Occurrence in Letters

TODO: NLP
