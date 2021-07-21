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

query_text = {
    "total": """
    ```
    (content:*) AND source_name:BulkLexisNexis
    ```
    """,
    "insect_population": """
    ```
    (content: 
            (insect OR pollinator OR bee OR honeybee OR moth) 
            AND ("insect population"~5 OR "pollinator population"~5 OR "bee population"~5 OR "honeybee population"~5 OR "moth population"~5 OR "biological diversity" OR biodiversity OR biomass OR ecolog* OR ecosystem* OR entomolog*) 
            AND (study OR professor OR experiment OR research OR analysis OR data)
        ) 
    AND (source_name:BulkLexisNexis)
    ```
    """,
    "insect_decline": """
    ```
    (content: 
        (insect OR pollinator OR bee OR honeybee OR moth) 
        AND ("insect population"~5 OR "pollinator population"~5 OR "bee population"~5 OR "honeybee population"~5 OR "moth population"~5 OR "biological diversity" OR biodiversity OR biomass OR ecolog* OR ecosystem* OR entomolog*) 
        AND (study OR professor OR experiment OR research OR analysis OR data) 
        AND (crisis OR "colony collapse" OR apocalypse OR armageddon OR extinct OR "insect decline"~5 OR "insect drop"~5 OR "insect decrease"~5 OR "insect disappear"~5 OR "population decline"~5 OR "population drop"~5 OR "population decrease"~5 OR "population disappear"~5 OR "abundance decline"~5 OR "abundance drop"~5 OR "abundance decrease"~5 OR "abundance disappear"~5)
        ) 
    AND (source_name:BulkLexisNexis)
    ```
    """,
    "pollinator_population": """
    ```
    (content: 
        ((insect AND pollinator) OR (bee OR honeybee OR moth)) 
        AND ("insect population"~5 OR "pollinator population"~5 OR "bee population"~5 OR "honeybee population"~5 OR "moth population"~5 OR "biological diversity" OR biodiversity OR biomass OR ecolog* OR ecosystem* OR entomolog*) 
        AND (study OR professor OR experiment OR research OR analysis OR data)
        ) 
    AND (source_name:BulkLexisNexis)
    ```
    """,
    "pollinator_decline": """
    ```
    (content: 
        ((insect AND pollinator) OR (bee OR honeybee OR moth)) 
        AND ("insect population"~5 OR "pollinator population"~5 OR "bee population"~5 OR "honeybee population"~5 OR "moth population"~5 OR "biological diversity" OR biodiversity OR biomass OR ecolog* OR ecosystem* OR entomolog*) 
        AND (study OR professor OR experiment OR research OR analysis OR data) 
        AND (crisis OR "colony collapse" OR apocalypse OR armageddon OR extinct OR "insect decline"~5 OR "insect drop"~5 OR "insect decrease"~5 OR "insect disappear"~5 OR "population decline"~5 OR "population drop"~5 OR "population decrease"~5 OR "population disappear"~5 OR "abundance decline"~5 OR "abundance drop"~5 OR "abundance decrease"~5 OR "abundance disappear"~5)
        ) 
    AND (source_name:BulkLexisNexis)
    ```
    """,
    "insect_apocalypse": """
    ```
    (content:"insect apocalypse"~5 OR "insect armageddon"~5 OR "beepocalypse") 
    AND (source_name:BulkLexisNexis)
    ```
    """,
    "colony_collapse": """
    ```
    (content:"colony collapse" AND (bee OR honeybee)) 
    AND (source_name:BulkLexisNexis)
    ```
    """,
    "climate_change": """
    ```
    (content:"climate change" OR "global warming") 
    AND (source_name:BulkLexisNexis)
    ```
    """,
    "climate_change_IPCCreport": """
    ```
    (content:
        ("climate change" OR "global warming") 
        AND ("IPCC" OR "Intergovernmental Panel on Climate Change") 
        AND report
        ) 
    AND (source_name:BulkLexisNexis)
    ```
    """,
    "insect_population_studies": """
    ```
    (content: 
        ("Krefeld" OR "the German study" OR "Hans de Kroon" OR "Martin Sorg" OR "Werner Stenmans" OR "Dave Goulson" OR "Brad Lister" OR "Andres Garcia" OR "the Puerto Rico study" OR "S?nchez-Bayo" OR "Wyckhuys" OR "Rob Dunn" OR "David Wagner" OR "Chris Thomas" OR "Anders Tottrup" OR "Kevin Gaston" OR "Chris Thomas" OR "Roel van Klink" OR "Arthur Shapiro" OR "Aletta Bonn" OR "E.O. Wilson") 
        AND (insect OR pollinator OR bee OR honeybee OR moth) 
        AND ("insect population"~5 OR "pollinator population"~5 OR "bee population"~5 OR "honeybee population"~5 OR "moth population"~5 OR "biological diversity" OR biodiversity OR biomass OR ecolog* OR ecosystem* OR entomolog*) 
        AND (study OR professor OR experiment OR research OR analysis OR data)
        ) 
    AND (source_name:BulkLexisNexis)
    ```
    """,
}


with st.sidebar:
    st.header("Configure the plot")
    # plot_button = st.button("Add Plot")
    # clear_button = st.button("Clear Plots")

    choose_CountOrProp = st.radio(
        "Article", ["count", "proportion"], key="count_or_prop"
    )
    # if "count_or_prop" not in st.session_state:
    #     st.session_state.count_or_prop = "count"
    choose_comparison = st.radio(
        "Compare", ["Queries", "Publishers"], key="queries_or_publishers"
    )
    # if "queries_or_publishers" not in st.session_state:
    #     st.session_state.queries_or_publishers = "Queries"
    if choose_comparison == "Queries":
        choose_publisher = st.selectbox(
            "Choose a publisher", publisher_options, key="publisher"
        )
        # if "publisher" not in st.session_state:
        #     st.session_state.publisher = "New York Times"
    elif choose_comparison == "Publishers":
        choose_query = st.selectbox("Choose a query", query_options, key="query")
        # if "query" not in st.session_state:
        #     st.session_state.query = "insect_population"

    st.header("Learn more")
    st.markdown(
        "Read the journal article: [No buzz for bees: Media coverage of pollinator decline](https://www.pnas.org/content/118/2/e2002552117)"
    )
    see_queries = st.checkbox("Show Queries?")
    if see_queries:
        see_which_queries = st.multiselect(
            "Show query text for", query_options, default=query_options
        )


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

    if which_query == "Queries":
        for trace in fig["data"]:
            if trace["name"] == "total":
                trace["visible"] = "legendonly"

    fig.update_layout(xaxis_rangeslider_visible=True)

    return fig


plot = create_plot()
st.plotly_chart(plot, use_container_width=True)

if see_queries:
    for q in see_which_queries:
        st.subheader(q)
        st.markdown(query_text[q])
