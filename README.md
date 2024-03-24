# Introduction

The app is aimed to summarize item 7 (Management's Discussion and Analysis of Financial Condition) in Form 10-K, submitted by most U.S. companies, leveraging OpenAI's LLM.
The app demo can be accessed at this [link](https://edgar-summary.onrender.com).
As a demo, this app contains Item 7 texts, extracted from 10-K reports from 2015-2023, 5 for each year.
The app is using OpenAI gpt-3.5-turbo.

# How to use

1. Select the year parameter
2. Select the Central Index Key (CIK)
    - If you do not know the company's CIK, you can look it up [here](https://www.sec.gov/edgar/searchedgar/cik).
3. The orginal text of the selected company and year will be displayed in the Item 7 tab.
4. The Summary will be displayed in the Summary tab.

# Data ingestion

The data ingestion documentation can be accessed [here](https://github.com/TextCorpusLabs/Edgar).

# Data

If you would like to access the 10-K corpus, you can do so [here](https://github.com/TextCorpusLabs/Edgar/releases/tag/1.1).

# Future potential developments

1. Create a text box for users to use their own OpenAI API key.
2. Create a built-in CIK lookup using the company names.
3. Incorporate spaCy's sentence tokenizer to prevent sentences being cut off by the gpt model.
4. Implement gpt-4 model, which will have a higher number of tokens limit, more suitable for longer text, mostly from larger companies.

# Requiremts

`
streamlit >= 1.32.2, <2.0.0
chardet >= 5.2.0, <6.0.0
openai >= 1.14.2, <2.0.0
drequests == 2.31
tqdm == 4.66
ipywidgets == 8.1
sec-downloader == 0.10
lxml == 4.9
pandas == 2.2
`