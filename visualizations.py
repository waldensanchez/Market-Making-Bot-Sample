
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: visualizations.py : python script with data visualization functions                         -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: THE LICENSE TYPE AS STATED IN THE REPOSITORY                                               -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
def plot_line_ts(ts_line_plot):
    import plotly.graph_objs as go
    trace_1 = go.Scatter(x = ts_line_plot['timestamp'], y = ts_line_plot['bid'], name = 'Bid')
    trace_2 = go.Scatter(x = ts_line_plot['timestamp'], y = ts_line_plot['ask'], name = 'Ask')
    data = [trace_1,trace_2]
    fig = go.Figure(data = data)
    return fig

def plot_ob(ob_data_plot, main_title, elements = 20, trace_width = .5):
    import plotly.graph_objs as go
    ask_data = ob_data_plot[['ask_size','ask']].sort_values(by = 'ask', ascending = True)
    bid_data = ob_data_plot[['bid_size','bid']].sort_values(by = 'bid', ascending = True)
    
    trace_1 = go.Bar(
        x = bid_data['bid'].apply(str).values[:elements],
        y = bid_data['bid_size'].values[:elements],
        name = 'Bid',
        width = trace_width
    )

    trace_2 = go.Bar(
        x = ask_data['ask'].apply(str).values[:elements],
        y = ask_data['ask_size'].values[:elements],
        name = 'Ask',
        width = trace_width
    )

    data = [trace_1,trace_2]
    layout = go.Layout(barmode = 'group', title = main_title)
    fig = go.Figure(data = data, layout = layout)

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='white', tickformat='plain', tickangle = 90)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='white', tickformat='plain')
    fig.update_layout(autosize=True)
    
    return fig

def plot_bar_ts(ts_bar_plot, main_title=None):
    import plotly.express as px
    import pandas as pd
    ts_bar_plot['timestamp'] = pd.to_datetime(ts_bar_plot['timestamp']).apply(lambda x: x.minute)
    fig = px.box(ts_bar_plot, x = 'timestamp', y = 'spread', title = main_title)
    fig.update_yaxes(title=None)
    fig.update_xaxes(title=None)
    return fig