# type: ignore
import streamlit as st
import tomllib as toml
import pathlib
import chardet
from openai import OpenAI

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
    with open(year_folder.joinpath(cik_file), "rb") as fp:
        raw_text = fp.read()
        encoding = chardet.detect(raw_text)['encoding']
        text = raw_text.decode(encoding)
    return text
@st.cache_data(max_entries = 10, persist = True)
def get_summary(year: str, cik: str) -> str:
    print(f"get_summary({year},{cik})")
    text = get_text(year, cik)
    #TODO: setup prompts in config.toml to allow for easy customization
    system = [{"role": "system", "content": "You are Summary AI."}]
    user = [{"role": "user", "content": f"Summarize this in 5 sentences:\n\n{text}"}]
    chat_history = []
    #TODO: add in rate limiting
    # this gets hit a lot when you have more than 1 tab open
    #with OpenAI(api_key = st.secrets["openai_api_key"]) as client:
    with OpenAI() as client:
        chat_completion = client.chat.completions.create(
            messages = system + chat_history + user,
            model = "gpt-3.5-turbo",
            max_tokens = 500,
            top_p = 0.9)
        xxx = chat_completion.choices[0].message.content
        return xxx

st.set_page_config(page_title = "Summary")
st.cache_data.clear()
st.cache_resource.clear()

year = st.sidebar.selectbox('Year', get_years())
cik = st.sidebar.selectbox('CIK', get_ciks(year))
st.title("EDGAR's Summary Viewer")
tab1, tab2, tab3 = st.tabs(["About", "Item 7", "Summary"])
with tab1:
    tab1.header('About Our Web-App', anchor=None, help=None, divider=False)
    tab1.markdown('''Welcome to our innovative web application tailored for Private Equity investment firms, offering a streamlined solution to digest the Management's Discussion and Analysis (MD&A) sections within 10-K filings.
                   We understand the critical role MD&A plays in investment decision-making, and our platform aims to simplify the process by extracting key insights from these complex documents.
                   Designed with efficiency in mind, our user-friendly interface empowers investors to quickly access and comprehend essential information, enabling more informed and strategic investment decisions.''')
with tab2:
    tab2.text_area("Item 7", get_text(year, cik), disabled = True, height  = 500)
with st.spinner('Summarizing the document...'):
   with tab3:
       tab3.text_area("Summary", get_summary(year, cik), disabled = True, height  = 500)