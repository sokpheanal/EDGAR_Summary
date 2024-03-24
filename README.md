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

The data were downloaded with the steps below.

## Step 1

1. Get the list of tickers from the SEC
2. Convert the tickers into an array, then sort it.
3. Save the tickers to a CSV

# Step 2

For each CIK in _tickers.csv_ (Step 1)

1. Get the accessions for the past 20 10-Ks

Save all the accessions for all the CIKs to disk

**Note 1**: Notice `tickers.CIK.unique()`.
The data pull needs to be done on CIK, not ticker.
A single company can have more than one ticker (AACI vs AACIU), byt only one CIK (1844817).

**Note 2**: Notice `except ValueError: pass`.
It is possible for a CIK (or ticker) to have no associated documents of a particular type(10-k).
`get_filing_metadatas()` responds to this case by throwing an error.
On our side, it just means skip the record.

# Step 3

For each accession in _accessions.csv_ (Step 2)

1. Get the XHTML document
2. save it to disk as _~/data/10-k/raw/{year}/{cik}.{accession number}.xhtml_

# Step 4

For each XHTML document:

1. Find "Item 7: Management's Discussion ..."
2. Find the next section.
3. Extract the IDs for both.
4. Extract the HTML between the IDs
5. Convert to TXT

The data ingestion documentation can be accessed [here](https://github.com/TextCorpusLabs/Edgar).

# Data

If you would like to access the 10-K corpus, you can do so [here](https://github.com/TextCorpusLabs/Edgar/releases/tag/1.1).

# App Back-End

This app was built using streamlit.
The summaries were generated, using the OpenAI gpt-3.5-turbo model.

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