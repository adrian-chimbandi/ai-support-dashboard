import plotly.express as px


def category_pie(df):

    counts = df['category'].value_counts().reset_index()
    counts.columns = ['Category', 'Count']

    return px.pie(
        counts,
        values='Count',
        names='Category',
        title='Ticket breakdown by category',
        color_discrete_sequence=px.colors.qualitative.Set3
    )


def sentiment_bar(df):

    counts = df['sentiment'].value_counts().reset_index()
    counts.columns = ['Sentiment', 'Count']

    colors = {
        'frustrated': '#E24B4A',
        'neutral': '#888780',
        'positive': '#1D9E75'
    }

    return px.bar(
        counts,
        x='Sentiment',
        y='Count',
        title='Customer sentiment',
        color='Sentiment',
        color_discrete_map=colors
    )


def volume_over_time(df):

    daily = df.groupby(df['date'].dt.date).size().reset_index()
    daily.columns = ['Date', 'Tickets']

    return px.line(
        daily,
        x='Date',
        y='Tickets',
        title='Ticket volume over time'
    )


def automation_bar(df):

    return px.bar(
        df,
        x='category',
        y='automation_score',
        title='Automation potential by category',
        color='automation_score',
        color_continuous_scale='Blues'
    )
