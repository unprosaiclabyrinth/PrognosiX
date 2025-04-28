import streamlit as st
import altair as alt
import pandas as pd

st.title('📊 CKD Patient Profile')

df = pd.read_csv('notebooks/ckd_preprocessed.csv')

features = ['age','sc', 'al', 'sg', 'hemo', 'rc', 'pcv']

df_ckd_only = df[df['classification'] == 'ckd'].dropna(subset=features).copy()
df_ckd_only = df_ckd_only.reset_index(drop=True)
df_ckd_only['patient_id'] = df_ckd_only.index.astype(str)

df_long = df_ckd_only[['patient_id'] + features].melt(id_vars='patient_id', 
                                                      var_name='feature', 
                                                      value_name='value')

dropdown = alt.binding_select(options=df_ckd_only['patient_id'].tolist(), name='CKD Patient Number: ')
selector = alt.param(name='SelectedPatient', bind=dropdown, value='0')

bar_chart = alt.Chart(df_long).transform_filter(
    alt.datum.patient_id == selector
).mark_bar().encode(
    x=alt.X('feature:N', title='Feature'),
    y=alt.Y('value:Q', title='Value'),
    color=alt.Color('feature:N', legend=None, scale=alt.Scale(scheme='set2')),
    tooltip=[
        alt.Tooltip('feature:N', title='Feature'),
        alt.Tooltip('value:Q', title='Value', format='.2f')
    ]
).add_params(
    selector
).properties(
    width=450,
    height=300,
    title='CKD Patient Profile'
)

st.altair_chart(bar_chart, use_container_width=True)
