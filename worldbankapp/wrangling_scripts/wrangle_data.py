import pandas as pd
import plotly.graph_objs as go


def scorechart(subset, countrylist, y_label, y_title, showlegend=False):
    graph = []
    for country in countrylist:
      x_val = subset.loc[subset['Economy'] == country, "DB Year"].tolist()
      y_val =  subset.loc[subset['Economy'] == country, y_label].tolist()
      graph.append(
          go.Scatter(
          x = x_val,
          y = y_val,
          mode = 'lines',
          name = country
          )
      )
    layout = dict(title = y_title,
                xaxis = dict(title = 'Year', dtick=1),
                yaxis = dict(title = 'Score'),
                showlegend = showlegend,
                #width=500,
                #height=500
                )
    return dict(data=graph, layout=layout)

def nearby_ranked(country, dbranks, rank_label):
    ranking = dbranks.loc[dbranks["Economy"]==country, rank_label].iloc[0]
    uranked = dbranks.loc[dbranks[rank_label]==(ranking+1), "Economy"].iloc[0]
    lranked = dbranks.loc[dbranks[rank_label]==(ranking-1), "Economy"].iloc[0]
    return ranking, lranked, uranked

def return_results(countrylist):
    """Creates four plotly visualizations

    Args:
        countrylist: list of countries to plot

    Returns:
        list (dict): list containing the four plotly visualizations

    """

    """if countrylist == None:
        countrylist = ['United States', 'China', 'Japan', 'Germany', \
            'United Kingdom', 'India', 'France', 'Brazil', 'Italy', 'Canada']"""

    df = pd.read_csv("/data/doingbuisness2020.csv")

    # get all countries and rankings
    rank_label = "Ease of doing business rank"
    dbranks = df.loc[pd.notna(df[rank_label]), ["Economy", rank_label]]
    all_countries = dbranks["Economy"].tolist()

    # get countries with close rankings to countrylist
    close_ranks = []
    for country in countrylist:
        ranking, lranked, uranked = nearby_ranked(country, dbranks, rank_label)
        close_ranks.append((int(ranking), country, lranked, uranked))
    close_ranks = sorted(close_ranks, key=lambda x: x[0])

    # Keep only the countries of interest (years and country name)
    df = df[df['Economy'].isin(countrylist)]

    # first chart section of charts: scores from 2016 to 2020
    # as a line charts
    from_year = 2016
    subset = df[df['DB Year']>=from_year]
    y_labels = [
                "Score-Getting electricity (DB16-20 methodology)",
                "Score-Registering property (DB17-20 methodology)",
                "Score-Getting credit (DB15-20 methodology)",
                "Score-Protecting minority investors (DB15-20 methodology)",
                "Score-Paying taxes (DB17-20 methodology)",
                "Score-Trading across borders (DB16-20 methodology)",
                "Score-Enforcing contracts (DB17-20 methodology)",
                "Score-Resolving insolvency"
                ]
    y_titles = [
                "Getting electricity",
                "Registering property",
                "Getting credit",
                "Protecting minority investors",
                "Paying taxes",
                "Trading across borders",
                "Enforcing contracts",
                "Resolving insolvency"
                ]

    figures = []
    # first: overall chart with legend
    y_label = "Ease of doing business score (DB17-20 methodology)"
    y_title = "Ease of doing business score"
    figures.append(scorechart(subset, countrylist, y_label, y_title, showlegend=True))
    # next charts without legend
    for y_label, y_title in zip(y_labels, y_titles):
        figures.append(scorechart(subset, countrylist, y_label, y_title, showlegend=True))
    return figures, all_countries, close_ranks
