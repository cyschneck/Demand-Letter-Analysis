# Anti-Racism Demand Letters Analysis
2020 Anti-Racism Demand Letters Analysis

_Note_: demand_letters directory is empty to preserve privacy (controlled in the .gitignore)

## Dependencies

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

```python
python3 demand_letter_analysis.py
```

Result of execution will produce x number of files based on the child directories beneath the root `demand_letters` directory. One file output will be generated for each child directory with the combined output of all the letters/files within the child directory
