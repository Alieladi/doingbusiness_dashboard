import pandas as pd
import plotly.graph_objs as go

# TODO: Scroll down to line 157 and set up a fifth visualization for the data dashboard

def get_data(countrylist, from_year=None):
    """Clean world bank data for a visualization dashboard

    Keeps data from range of years variable for countries variable
    Reorients the columns into a country, year and value

    Args:
        countrylist: list of countries to filter

    Returns:
        dataframe: country, year and value
        all_countries: all countries available (selected and not selected)

    """
    df = pd.read_csv("data/doingbuisness2020.csv")
    # get all countries
    all_countries = df.loc[pd.notna(df["Ease of doing business rank"]), "Economy"].tolist()

    # Keep only the columns of interest (years and country name)
    df = df[df['Economy'].isin(countrylist)]
    if from_year:
        df = df[df['DB Year']>=from_year]

    # output dataframe and list of all countries
    return df, all_countries


def return_figures(countrylist):
    """Creates four plotly visualizations

    Args:
        countrylist: list of countries to plot

    Returns:
        list (dict): list containing the four plotly visualizations

    """

    """if countrylist == None:
        countrylist = ['United States', 'China', 'Japan', 'Germany', \
            'United Kingdom', 'India', 'France', 'Brazil', 'Italy', 'Canada']"""

    df, all_countries = get_data(countrylist)

    # first chart plots Ease of doing business score from 2016 to 2020
    # as a line chart
    graph_one = []
    y_label = "Ease of doing business score (DB17-20 methodology)"
    from_year = 2016
    df1 = df[df['DB Year']>=from_year]
    for country in countrylist:
      x_val = df1.loc[df1['Economy'] == country, "DB Year"].tolist()
      y_val =  df1.loc[df1['Economy'] == country, y_label].tolist()
      graph_one.append(
          go.Scatter(
          x = x_val,
          y = y_val,
          mode = 'lines',
          name = country
          )
      )

    layout_one = dict(title = 'Ease of doing business score (DB17-20 methodology)',
                xaxis = dict(title = 'Year'),
                yaxis = dict(title = 'Score'),
                )

# second chart plots Score-Starting a business as a line chart
    graph_two = []
    y_label = "Score-Starting a business"
    from_year = 2016
    df2 = df[df['DB Year']>=from_year]
    for country in countrylist:
      x_val = df2.loc[df2['Economy'] == country, "DB Year"].tolist()
      y_val =  df2.loc[df2['Economy'] == country, y_label].tolist()
      graph_two.append(
          go.Scatter(
          x = x_val,
          y = y_val,
          mode = 'lines',
          name = country
          )
      )

    layout_two = dict(title = 'Score-Starting a business',
                xaxis = dict(title = 'Year'),
                yaxis = dict(title = 'Score'),
                )


# third chart plots percent of population that is rural from 1990 to 2015
    graph_three = []
    y_label = 'Score-Dealing with construction permits (DB16-20 methodology)'
    from_year = 2016
    df3 = df[df['DB Year']>=from_year]
    for country in countrylist:
      x_val = df3.loc[df3['Economy'] == country, "DB Year"].tolist()
      y_val =  df3.loc[df3['Economy'] == country, y_label].tolist()
      graph_three.append(
          go.Scatter(
          x = x_val,
          y = y_val,
          mode = 'lines',
          name = country
          )
      )

    layout_three = dict(title = 'Score-Starting a business',
                xaxis = dict(title = 'Year'),
                yaxis = dict(title = 'Score'),
                )

    # append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))

    return figures, all_countries
