import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Beepocalpyse", layout="wide")

df = pd.read_csv(
    "Data/bln-queries_6pubs_26Feb.csv",
    parse_dates=["publication_date"],
    dtype={"publisher": "category"},
)


st.title("Beepocalypse: Visualizing Query Results")

publisher_options = [
    "New York Times",
    "Washington Post",
    "Associated Press",
    "Agence France Presse",
    "Xinhua General News Service",
    "Deutsche Presse-Agentur",
]
publisher_map = {
    "New York Times": "NYT",
    "Washington Post": "WP",
    "Associated Press": "AP",
    "Agence France Presse": "AFP",
    "Xinhua General News Service": "XGNS",
    "Deutsche Presse-Agentur": "DPA",
}
query_options = list(df["query"].unique())

with st.sidebar:
    st.header("Configure a plot")
    # plot_button = st.button("Add Plot")
    # clear_button = st.button("Clear Plots")

    choose_CountOrProp = st.radio(
        "Article", ["count", "proportion"], key="count_or_prop"
    )
    if "count_or_prop" not in st.session_state:
        st.session_state.count_or_prop = "count"
    choose_comparison = st.radio(
        "Compare", ["Queries", "Publishers"], key="queries_or_publishers"
    )
    if "queries_or_publishers" not in st.session_state:
        st.session_state.queries_or_publishers = "Queries"
    if choose_comparison == "Queries":
        choose_publisher = st.selectbox(
            "Choose a publisher", publisher_options, key="publisher"
        )
        if "publisher" not in st.session_state:
            st.session_state.publisher = "New York Times"
    elif choose_comparison == "Publishers":
        choose_query = st.selectbox("Choose a query", query_options, key="query")
        if "query" not in st.session_state:
            st.session_state.query = "insect_population"


@st.cache
def create_plot(which_query=choose_comparison, y_axis=choose_CountOrProp):
    if which_query == "Queries":
        color = "query"
        query_value = publisher_map[choose_publisher]
        query_column = "publisher"
    elif which_query == "Publishers":
        color = "publisher"
        query_value = choose_query
        query_column = "query"

    query_text = f"{query_column}=='{query_value}'"
    title_text = f"{query_column}: {query_value}"

    fig = px.line(
        df.query(query_text),
        x="publication_date",
        y=y_axis,
        color=color,
        title=title_text,
    )

    fig.update_layout(xaxis_rangeslider_visible=True)

    return fig


plot = create_plot()
st.plotly_chart(plot, use_container_width=True)
