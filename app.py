import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Sample dataset
data = {
    'pro': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
    'Severity': [5, 4, 2, 3, 1, 4, 3, 5, 3, 4],
    'Probability': [0.9, 0.6, 0.7, 0.5, 0.8, 0.7, 0.1, 0.5, 0.3, 0.5],
    'Score': [4.5, 2.4, 1.4, 1.5, 0.8, 2.8, 0.3, 2.5, 0.9, 2],
    'Risk level': ['High', 'Medium', 'Medium', 'Medium', 'Low', 'High', 'Low', 'High', 'Low', 'Medium']
}
df = pd.DataFrame(data)

# Streamlit app
st.title('pro Risk Analysis')

# Sidebar for user inputs
st.sidebar.header('Options')
selected_pro = st.sidebar.selectbox('Select a pro', options=df['pro'].unique())

# Action buttons
generate_visualizations = st.sidebar.button('Generate All Visualizations')
show_analysis = st.sidebar.button('Show Individual Pr Analysis')

if generate_visualizations:
    st.subheader('All Visualizations')

    # Heatmap for all features with annotations
    fig_all = go.Figure()

    # Add the heatmap for Severity vs Probability
    fig_all.add_trace(go.Heatmap(
        z=df['Score'],
        x=df['Severity'],
        y=df['Probability'],
        colorscale=[[0, "green"], [0.5, "yellow"], [1, "red"]],
        colorbar=dict(title='Impact Score'),
        showscale=True
    ))

    # Add annotations for clarity
    for i, row in df.iterrows():
        fig_all.add_annotation(
            x=row['Severity'],
            y=row['Probability'],
            text=f"pro: {row['pro']}<br>Score: {row['Score']}",
            showarrow=True,
            arrowhead=2
        )

    fig_all.update_layout(
        title='Heatmap for All Features',
        xaxis_title='Severity Level',
        yaxis_title='Probability of Issue'
    )
    st.plotly_chart(fig_all)

    # Scatter plot
    fig1 = px.scatter(df, x='Severity', y='Probability', size='Score', color='pro',
                      title='Severity vs Probability with pro Score',
                      labels={'Severity': 'Severity Level', 'Probability': 'Probability of Issue'})
    fig1.update_layout(xaxis=dict(range=[0, 6]), yaxis=dict(range=[0, 1]))
    st.plotly_chart(fig1)

    # Stacked bar chart for risk level distribution
    fig_stacked_bar_risk = px.bar(
        df,
        x='pro',
        y='Score',
        color='Risk level',
        title='Stacked Bar Chart of Risk Level Distribution for All pros',
        labels={'x': 'pro', 'y': 'Score'},
        barmode='stack'
    )
    st.plotly_chart(fig_stacked_bar_risk)

if show_analysis and selected_pro:
    st.subheader(f'pro {selected_pro} Details')

    # Generate graph for selected pro
    pro_data = df[df['pro'] == selected_pro]

    # Ensure the data is in the correct format for the bar chart
    features = ['Severity', 'Probability', 'Score']
    values = pro_data[features].values.flatten()
    feature_labels = [f'{feature}: {value}' for feature, value in zip(features, values)]

    fig_pro = px.bar(
        x=features,
        y=values,
        title=f'pro {selected_pro} Details',
        labels={'x': 'Feature', 'y': 'Value'},
        text=values
    )
    fig_pro.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    st.plotly_chart(fig_pro)
