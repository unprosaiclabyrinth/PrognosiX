import streamlit as st
import altair as alt
import pandas as pd

st.set_page_config(page_title='Visualization 3', page_icon='📊', layout='wide')
st.title('📊 Visualization 3')

df = pd.read_csv('notebooks/ckd_preprocessed.csv')

features = ['sc', 'al', 'sg', 'hemo', 'rc', 'pcv']

df_scatter = df[features + ['classification']].dropna().copy()
df_scatter['class_label'] = df_scatter['classification'].map({'ckd': 'CKD', 'notckd': 'Not CKD'})

dropdown_x = alt.binding_select(options=features, name='X-Axis Feature:')
dropdown_y = alt.binding_select(options=features, name='Y-Axis Feature:')

x_select = alt.param('xFeature', bind=dropdown_x, value='sc')
y_select = alt.param('yFeature', bind=dropdown_y, value='hemo')

scatter_plot = alt.Chart(df_scatter).add_params(
    x_select,
    y_select
).transform_calculate(
    x='datum[xFeature]',
    y='datum[yFeature]'
).mark_circle(size=60).encode(
    x=alt.X('x:Q', title=None),
    y=alt.Y('y:Q', title=None),
    color=alt.Color('class_label:N', title='CKD Classification',
                    scale=alt.Scale(domain=['CKD', 'Not CKD'],
                                    range=['#e41a1c', '#4daf4a'])),
    tooltip=features + ['classification']
).properties(
    width=600,
    height=450,
    title='Scatter Plot using 2 features selected'
).interactive()

st.altair_chart(scatter_plot, use_container_width=True)
