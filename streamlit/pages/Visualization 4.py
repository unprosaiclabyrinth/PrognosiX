import streamlit as st
import altair as alt
import pandas as pd

st.title('📊 Visualization 4')

df = pd.read_csv('notebooks/ckd_preprocessed.csv')

features = ['sc', 'al', 'sg', 'hemo', 'rc', 'pcv']

df_trend = df[features + ['age', 'classification']].dropna().copy()
df_trend['class_label'] = df_trend['classification'].map({'ckd': 'CKD', 'notckd': 'Not CKD'})

charts = []

for feature in features:
    chart = alt.Chart(df_trend).mark_line(point=True).encode(
        x=alt.X('age:Q', title='Age'),
        y=alt.Y(f'mean({feature}):Q', title=f'Avg {feature.upper()}'),
        color=alt.Color('class_label:N', title='CKD Classification',
                    scale=alt.Scale(domain=['CKD', 'Not CKD'],
                                    range=['#e41a1c', '#4daf4a'])),
    ).properties(
        width=300,
        height=250,
        title=f'Age vs {feature.upper()}'
    ).interactive()
    charts.append(chart)

for chart in charts:
    st.altair_chart(chart, use_container_width=True)
