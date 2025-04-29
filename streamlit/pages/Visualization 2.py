import streamlit as st
import altair as alt
import pandas as pd

st.set_page_config(page_title='Visualization 2', page_icon='📊', layout='wide')
st.title('📊 Visualization 2')

df = pd.read_csv('notebooks/ckd_preprocessed.csv')

features = ['sc', 'al', 'sg', 'hemo', 'rc', 'pcv']

df_parallel = df[features].dropna().copy()

df_parallel['class_label'] = df['classification'].map({
    'ckd': 'CKD',
    'notckd': 'Not CKD'
})

df_long = df_parallel.reset_index().melt(
    id_vars=['index', 'class_label'],
    var_name='feature',
    value_name='value'
)

brush = alt.selection_interval(encodings=['y'])

parallel_plot = alt.Chart(df_long).mark_line().encode(
    x=alt.X('feature:N', title='Feature'),
    y=alt.Y('value:Q', title='Value', scale=alt.Scale(zero=False)),
    color=alt.Color('class_label:N', title='CKD Classification',
                    scale=alt.Scale(domain=['CKD', 'Not CKD'],
                                    range=['#e41a1c', '#4daf4a'])),
    detail='index:N',
    opacity=alt.condition(brush, alt.value(1), alt.value(0.05)),
    tooltip=['feature', 'value', 'class_label']
).add_params(
    brush
).properties(
    width=600,
    height=400,
    title='Parallel Plot'
)

st.altair_chart(parallel_plot, use_container_width=True)
