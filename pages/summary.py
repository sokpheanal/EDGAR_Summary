# type: ignore
import streamlit as st
import tomllib as toml
import pathlib
import time

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

def get_text(year: str, cik: str) -> str:
    corpus_folder = get_config()['folders']['corpus']
    year_folder = pathlib.Path(corpus_folder).joinpath(year)
    cik_file = [p.name for p in year_folder.iterdir() if p.name.startswith(cik)][0]
    #TODO: implement the file reading logic for ANSI vs UTF8
    with open(year_folder.joinpath(cik_file), "r") as fp:
        text = fp.read()
    return text
def get_summary(year: str, cik: str) -> str:
    text = get_text(year, cik)
    #TODO: implement the summary logic
    time.sleep(10)
    return "My summary here"

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
