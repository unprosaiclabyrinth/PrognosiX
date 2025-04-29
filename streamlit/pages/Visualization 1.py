import streamlit as st
import altair as alt
import pandas as pd

st.set_page_config(page_title='Visualization 1', page_icon='📊', layout='wide')
st.title('📊 Visualization 1')

df = pd.read_csv('notebooks/ckd_preprocessed.csv')

feature_label_map = {
    'sc': 'Serum Creatinine',
    'al': 'Albumin',
    'sg': 'Specific Gravity',
    'hemo': 'Hemoglobin',
    'rc': 'Red Blood Cell Count',
    'pcv': 'Packed Cell Volume'
}

label_to_col = {v: k for k, v in feature_label_map.items()}

df_filtered = df[list(feature_label_map.keys()) + ['classification']].copy()
df_filtered['classification'] = df_filtered['classification'].astype(str)

df_long = df_filtered.melt(id_vars='classification', var_name='feature', value_name='value')
df_long = df_long.dropna()
df_long['label'] = df_long['feature'].map(feature_label_map)

dropdown = alt.binding_select(options=list(label_to_col.keys()), name='Feature: ')
selector = alt.param('FeatureSelector', bind=dropdown, value='Albumin')

bar_chart = alt.Chart(df_long).add_params(
    selector
).transform_filter(
    alt.datum.label == selector
).mark_bar().encode(
    x=alt.X('classification:N', title='CKD Class'),
    y=alt.Y('mean(value):Q', title='Average Value'),
    color=alt.Color('classification:N', title='CKD Classification',
                    scale=alt.Scale(domain=['ckd', 'notckd'],
                                    range=['#e41a1c', '#4daf4a']))
).properties(
    width=400,
    height=300,
    title='Average Value of Selected Feature by CKD Class'
)

st.altair_chart(bar_chart, use_container_width=True)
