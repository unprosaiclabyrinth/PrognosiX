import streamlit as st
import pandas as pd
import altair as alt
import math
from joblib import load
from sklearn.preprocessing import LabelEncoder

st.set_page_config(page_title='Risk Estimator', page_icon='🔍', layout='wide')
st.title('🔍 Risk Estimator')

df = pd.read_csv('notebooks/ckd_preprocessed.csv')
model = load('notebooks/risk_estimator/ckd_model.joblib')
features = ['age','bp','sg','al','su','rbc','pc','pcc','ba','bgr','bu','sc','sod','pot','hemo','pcv','wc','rc','htn','dm','cad','appet','pe','ane']

cat_features = ['rbc','pc','pcc','ba','htn','dm','cad','appet','pe','ane']
class_map = {}
for f in cat_features:
    le = LabelEncoder().fit(df[f])
    class_map[f] = list(le.classes_)

coefs = model.coef_[0]
intercept = model.intercept_[0]
placeholder = pd.DataFrame({'x':[0]})

params = [
    alt.param('age', bind=alt.binding_range(min=2, max=90, step=1, name='Age'), value=50),
    alt.param('bp', bind=alt.binding_range(min=50, max=200, step=0.5, name='Blood Pressure (mm Hg)'), value=120),
    alt.param('sg', bind=alt.binding_range(min=1.005,max=1.025,step=0.001,name='Specific Gravity'), value=1.010),
    alt.param('al', bind=alt.binding_range(min=0, max=5, step=0.1, name='Albumin (0–5)'), value=1),
    alt.param('su', bind=alt.binding_range(min=0, max=5, step=0.1, name='Sugar (0–5)'), value=1),
    alt.param('rbc', bind=alt.binding_select(options=['normal','abnormal'], name='RBC'), value='normal'),
    alt.param('pc', bind=alt.binding_select(options=['normal','abnormal'], name='Pus Cells'), value='normal'),
    alt.param('pcc', bind=alt.binding_select(options=['present','not present'], name='Pus Cell Clumps'), value='not present'),
    alt.param('ba', bind=alt.binding_select(options=['present','not present'], name='Bacteria'), value='not present'),
    alt.param('bgr', bind=alt.binding_range(min=50, max=500, step=1, name='Blood Glucose Random (mg/dl)'),value=100),
    alt.param('bu', bind=alt.binding_range(min=5, max=200, step=1, name='Blood Urea (mg/dl)'), value=30),
    alt.param('sc', bind=alt.binding_range(min=0.5, max=15, step=0.1, name='Serum Creatinine (mg/dl)'), value=1.0),
    alt.param('sod', bind=alt.binding_range(min=100,max=160, step=1, name='Sodium (mEq/l)'), value=135),
    alt.param('pot', bind=alt.binding_range(min=2, max=8, step=0.1, name='Potassium (mEq/l)'), value=4.0),
    alt.param('hemo', bind=alt.binding_range(min=5, max=20, step=0.1, name='Hemoglobin (g/dl)'), value=12.0),
    alt.param('pcv', bind=alt.binding_range(min=15, max=60, step=1, name='Packed Cell Volume (%)'), value=40),
    alt.param('wc', bind=alt.binding_range(min=2500, max=20000,step=1, name='WBC Count (cells/cumm)'), value=8000),
    alt.param('rc', bind=alt.binding_range(min=2, max=7, step=0.1, name='RBC Count (millions/cumm)'), value=5),
    alt.param('htn', bind=alt.binding_select(options=['yes','no'], name='Hypertension'), value='no'),
    alt.param('dm', bind=alt.binding_select(options=['yes','no'], name='Diabetes Mellitus'), value='no'),
    alt.param('cad', bind=alt.binding_select(options=['yes','no'], name='Coronary Artery Disease'), value='no'),
    alt.param('appet', bind=alt.binding_select(options=['good','poor'], name='Appetite'), value='good'),
    alt.param('pe', bind=alt.binding_select(options=['yes','no'], name='Pedal Edema'), value='no'),
    alt.param('ane', bind=alt.binding_select(options=['yes','no'], name='Anemia'), value='no'),
]

base = alt.Chart(placeholder).transform_calculate(
    **{f"{f}_val": f for f in features},

    rbc_num = f'datum.rbc_val === "{class_map["rbc"][0].strip()}" ? 0 : 1',
    pc_num = f'datum.pc_val === "{class_map["pc"][0].strip()}" ? 0 : 1',
    pcc_num = f'datum.pcc_val === "{class_map["pcc"][0].strip()}" ? 0 : 1',
    ba_num = f'datum.ba_val === "{class_map["ba"][0].strip()}" ? 0 : 1',
    htn_num = f'datum.htn_val === "{class_map["htn"][0].strip()}" ? 0 : 1',
    dm_num = f'datum.dm_val === "{class_map["dm"][0].strip()}" ? 0 : 1',
    cad_num = f'datum.cad_val === "{class_map["cad"][0].strip()}" ? 0 : 1',
    appet_num = f'datum.appet_val === "{class_map["appet"][0].strip()}" ? 0 : 1',
    pe_num = f'datum.pe_val === "{class_map["pe"][0].strip()}" ? 0 : 1',
    ane_num = f'datum.ane_val === "{class_map["ane"][0].strip()}" ? 0 : 1',

    logit=(
        f"{intercept}"
        + f" + {coefs[0]} * datum.age_val"
        + f" + {coefs[1]} * datum.bp_val"
        + f" + {coefs[2]} * datum.sg_val"
        + f" + {coefs[3]} * datum.al_val"
        + f" + {coefs[4]} * datum.su_val"
        + f" + {coefs[5]} * datum.rbc_num"
        + f" + {coefs[6]} * datum.pc_num"
        + f" + {coefs[7]} * datum.pcc_num"
        + f" + {coefs[8]} * datum.ba_num"
        + f" + {coefs[9]} * datum.bgr_val"
        + f" + {coefs[10]} * datum.bu_val"
        + f" + {coefs[11]} * datum.sc_val"
        + f" + {coefs[12]} * datum.sod_val"
        + f" + {coefs[13]} * datum.pot_val"
        + f" + {coefs[14]} * datum.hemo_val"
        + f" + {coefs[15]} * datum.pcv_val"
        + f" + {coefs[16]} * datum.wc_val"
        + f" + {coefs[17]} * datum.rc_val"
        + f" + {coefs[18]} * datum.htn_num"
        + f" + {coefs[19]} * datum.dm_num"
        + f" + {coefs[20]} * datum.cad_num"
        + f" + {coefs[21]} * datum.appet_num"
        + f" + {coefs[22]} * datum.pe_num"
        + f" + {coefs[23]} * datum.ane_num"
    ),

    risk  = "1 - (1/(1+exp(-datum.logit)))",
    angle = "datum.risk * 2 * PI"
)

gauge = base.mark_arc(innerRadius=100, outerRadius=130).encode(
    theta=alt.Theta('risk:Q', scale=alt.Scale(domain=[0,1], range=[0,2 * math.pi])),
    color=alt.Color('risk:Q', scale=alt.Scale(domain=[0,1], scheme='redyellowgreen', reverse=True))
).properties(width=300, height=300)

text = base.mark_text(size=60, align='center', baseline='middle').encode(
    text=alt.Text('risk:Q', format='.1%'),
    color= alt.condition(
        alt.datum.risk > 0.5,
        alt.value('red'),
        alt.value('green')
    )
).properties(width=300, height=300)

chart = (gauge + text).add_params(*params).resolve_scale(color='independent')

#69.0,80.0,1.02,3.0,0.0,abnormal,normal,notpresent,notpresent,148.0365168539326,103.0,4.1,132.0,5.9,12.5,38.88449848024316,8406.122448979591,4.707434944237917,yes,no,no,good,no,no,ckd
st.altair_chart(chart, use_container_width=True)
