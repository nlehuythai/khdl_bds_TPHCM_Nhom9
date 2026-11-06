import plotly.express as px
import plotly.graph_objects as go

def price_histogram(df, column, title, x_label):
    data = df[column].dropna()
    fig = px.histogram(data_frame={column: data}, x=column, nbins=35, title=title)
    fig.update_layout(xaxis_title=x_label, yaxis_title="Số tin đăng",
                      bargap=0.08, template="plotly_white")
    return fig

def box_by_type(df, column, title, y_label):
    data = df.dropna(subset=["property_type", column])
    fig = px.box(data, x="property_type", y=column, color="property_type",
                 points="outliers", title=title)
    fig.update_layout(xaxis_title="Loại bất động sản", yaxis_title=y_label,
                      showlegend=False, template="plotly_white")
    return fig

def scatter_area_price(df, y_col, title, y_label):
    data = df.dropna(subset=["area_m2", y_col, "property_type"])
    fig = px.scatter(data, x="area_m2", y=y_col, color="property_type",
                     hover_data=[c for c in ["district", "price_vnd", "bedrooms"] if c in data.columns],
                     opacity=0.65, title=title)
    fig.update_layout(xaxis_title="Diện tích (m²)", yaxis_title=y_label,
                      template="plotly_white")
    return fig
