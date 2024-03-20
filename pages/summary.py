# type: ignore
import streamlit as st
import tomllib as toml
import pathlib
import time
import chardet

@st.cache_resource
def get_config() -> dict[str, any]:
    with open("config.toml", "rb") as fp:
        data = toml.load(fp)
    return data
@st.cache_data
def get_years() -> list[str]:
    corpus_folder = get_config()['folders']['corpus']
    years = [p.name for p in pathlib.Path(corpus_folder).iterdir() if p.is_dir()]
    return years
@st.cache_data
def get_ciks(year: str) -> list[str]:
    corpus_folder = get_config()['folders']['corpus']
    year_folder = pathlib.Path(corpus_folder).joinpath(year)
    ciks = [p.name.split('.', 1)[0] for p in year_folder.iterdir() if p.is_file()]
    return ciks
@st.cache_data
def get_text(year: str, cik: str) -> str:
    corpus_folder = get_config()['folders']['corpus']
    year_folder = pathlib.Path(corpus_folder).joinpath(year)
    cik_file = [p.name for p in year_folder.iterdir() if p.name.startswith(cik)][0]
    #TODO: implement the file reading logic for ANSI vs UTF8
    with open(year_folder.joinpath(cik_file), "r") as fp:
        raw_text = fp.read()
        # Detecting encoding
        encoding = chardet.detect(raw_text)['encoding']
        text = raw_text.decode(encoding)
    return text
@st.cache_data
def summarize_text(text):
    prompt = f"Summarize the following text in 15 sentences:\n{text}"
  
    chat_completion = openai.ChatCompletion.create(
        model="text-davinci-003",
        messages = system + chat_history + user,
        max_tokens=500,
        stop=["\n\n"],
        temperature=0.7
    )
    return chat_completion.choices[0].message['content']
@st.cache_data
def text_to_chunks(text):
    chunks = [[]]
    chunk_total_words = 0

    sentences = nlp(text)

    for sentence in sentences.sents:
        chunk_total_words += len(sentence.text.split(" "))

        if chunk_total_words > 2700:
            chunks.append([])
            chunk_total_words = len(sentence.text.split(" "))

        chunks[len(chunks)-1].append(sentence.text)    
    return chunks
@st.cache_data
def get_summary(year: str, cik: str) -> str:
    text = get_text(year, cik)
    chunks = text_to_chunks(text)
    chunk_summaries = []

    #TODO: implement the summary logic

    for chunk in chunks:
        chunk_summary = summarize_text(" ".join(chunk))
        chunk_summaries.append(chunk_summary)

    section_summary = " ".join(chunk_summaries)
    return section_summary
    time.sleep(10)

st.set_page_config(
    page_title = "Summary"
)

year = st.sidebar.selectbox('year', get_years())
cik = st.sidebar.selectbox('cik', get_ciks(year))
st.title("EDGAR's Summary Viewer")
tab1, tab2 = st.tabs(["Item 7", "Summary"])
with tab1:
    tab1.text_area("Item 7", get_text(year, cik), disabled = True, height  = 500)
with st.spinner('Summarizing the document...'):
   with tab2:
       tab2.text_area("Summary", get_summary(year, cik), disabled = True, height  = 500)
