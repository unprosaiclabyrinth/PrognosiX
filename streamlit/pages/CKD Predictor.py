import streamlit as st
import json
import os
import re
import pandas as pd
from dotenv import load_dotenv
import google.genai as genai
import glob
from joblib import load
from sklearn.preprocessing import LabelEncoder

def response_to_df(text):
    if 'json' in text:
        fixed_str = text.removeprefix('```json\n').removesuffix('\n```')
        if '{' not in fixed_str:
            fixed_str = '{' + fixed_str
        if '\n}' not in fixed_str:
            fixed_str += '\n}'

        fixed_str = re.sub(r'(\b(?:yes|no|true|false)\b)(?=\s*[\n,])', r'"\1"', fixed_str) # add double quotes around non-numeric values
        fixed_str = re.sub(r'([{,]?\s*)(\w+)(\s*:)', r'\1"\2"\3', fixed_str) # add double quotes around keys if necessary
        fixed_str = re.sub(r'(?<=[\d"])\s*\n(?=\s*"\w+":)', ',\n', fixed_str) # add commas to end of life (except last) if necessary

        try:
            data = json.loads(fixed_str)
        except:
            print(fixed_str)
            return
    else:
        try:
            data = dict(line.split(': ') for line in text.strip().splitlines())
        except:
            print(text)
            return
    
    try:
        df = pd.DataFrame([data]).reindex(columns=expected_cols)
    except:
        print(data)
        return
    
    return df

def get_pairs_text(text):
    example = '''
    Example 1:
    Text: 'I'm 43 years old, and my recent blood tests showed a low specific gravity. I have been feeling quite fatigued, and my doctor mentioned I might have anemia. My blood pressure is high, and I have a poor appetite.'

    Key-value pairs:
    age: 43
    appet: poor
    ane: yes
    htn: yes
    '''

    prompt = f'''
 	1. Age (numerical): age in years
 	2. Blood Pressure (numerical): bp in mm/Hg
 	3. Specific Gravity (nominal): sg - (1.005,1.010,1.015,1.020,1.025)
 	4. Albumin (nominal): al - (0,1,2,3,4,5)
 	5. Sugar (nominal): su - (0,1,2,3,4,5)
 	6. Red Blood Cells (nominal): rbc - (normal,abnormal)
 	7. Pus Cell (nominal): pc - (normal,abnormal)
 	8. Pus Cell clumps (nominal): pcc - (present,notpresent)
 	9. Bacteria (nominal): ba - (present,notpresent)
 	10. Blood Glucose Random (numerical): bgr in mgs/dl
 	11. Blood Urea (numerical): bu in mgs/dl
 	12. Serum Creatinine (numerical): sc in mgs/dl
 	13. Sodium (numerical): sod in mEq/L
 	14. Potassium (numerical): pot in mEq/L
 	15. Hemoglobin (numerical): hemo in gms
 	16. Packed Cell Volume (numerical): pcv in %
 	17. White Blood Cell Count (numerical): wc in cells/cumm
 	18. Red Blood Cell Count (numerical): rc in millions/cmm
 	19. Hypertension (nominal): htn - (yes,no)
 	20. Diabetes Mellitus (nominal): dm - (yes,no)
 	21. Coronary Artery Disease (nominal): cad - (yes,no)
 	22. Appetite (nominal): appet - (good,poor)
 	23. Pedal Edema (nominal): pe - (yes,no)	
 	24. Anemia (nominal): ane - (yes,no)

    I'll provide you with an example of generating key-value pairs, then ask you to do the same for a new text.
    
    {example}

    Now, please extract the text from this pdf, then generate only the key-value pairs. Do not give any explanation.
    Text: {text}

    Key-value pairs:
    '''

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model='gemini-2.0-flash', contents=prompt
    )
    return response.text

def get_pairs_image(path):
    example = '''
    Example:
    Text: 'I'm 43 years old, and my recent blood tests showed a specific gravity of 1.010. I have been feeling quite fatigued, and my doctor mentioned I might have anemia. My blood pressure is high, and I have a poor appetite.'

    Key-value pairs:
    age: 43
    sg: 1.010
    appet: poor
    ane: yes
    htn: yes
    '''

    prompt = f'''
    Here are the keys, what they represent, and their possible values.

 	1. Age (numerical): age in years
 	2. Blood Pressure (numerical): bp in mm/Hg
 	3. Specific Gravity (nominal): sg - (1.005,1.010,1.015,1.020,1.025)
 	4. Albumin (nominal): al - (0,1,2,3,4,5)
 	5. Sugar (nominal): su - (0,1,2,3,4,5)
 	6. Red Blood Cells (nominal): rbc - (normal,abnormal)
 	7. Pus Cell (nominal): pc - (normal,abnormal)
 	8. Pus Cell clumps (nominal): pcc - (present,notpresent)
 	9. Bacteria (nominal): ba - (present,notpresent)
 	10. Blood Glucose Random (numerical): bgr in mgs/dl
 	11. Blood Urea (numerical): bu in mgs/dl
 	12. Serum Creatinine (numerical): sc in mgs/dl
 	13. Sodium (numerical): sod in mEq/L
 	14. Potassium (numerical): pot in mEq/L
 	15. Hemoglobin (numerical): hemo in gms
 	16. Packed Cell Volume (numerical): pcv in %
 	17. White Blood Cell Count (numerical): wc in cells/cumm
 	18. Red Blood Cell Count (numerical): rc in millions/cmm
 	19. Hypertension (nominal): htn - (yes,no)
 	20. Diabetes Mellitus (nominal): dm - (yes,no)
 	21. Coronary Artery Disease (nominal): cad - (yes,no)
 	22. Appetite (nominal): appet - (good,poor)
 	23. Pedal Edema (nominal): pe - (yes,no)	
 	24. Anemia (nominal): ane - (yes,no)

    I'll provide you with an textual example of generating key-value pairs, then ask you to do the same for a lab report.
    
    {example}

    Now, please extract the text from this pdf, then generate only the key-value pairs. Do not give any explanation.

    Key-value pairs:
    '''

    client = genai.Client(api_key=api_key)

    myfile = client.files.upload(file=path)
    response = client.models.generate_content(
        model='gemini-2.5-pro-exp-03-25', contents=[myfile, prompt]
    )
    return response.text

def create_response(pred, df):
    field_labels = {
        'age': 'Age (years)',
        'bp': 'Blood Pressure (mmHg)',
        'sg': 'Specific Gravity',
        'al': 'Albumin',
        'su': 'Sugar',
        'rbc': 'Red Blood Cells',
        'pc': 'Pus Cell',
        'pcc': 'Pus Cell Clumps',
        'ba': 'Bacteria',
        'bgr': 'Blood Glucose Random (mg/dL)',
        'bu': 'Blood Urea (mg/dL)',
        'sc': 'Serum Creatinine (mg/dL)',
        'sod': 'Sodium (mEq/L)',
        'pot': 'Potassium (mEq/L)',
        'hemo': 'Hemoglobin (gms)',
        'pcv': 'Packed Cell Volume (%)',
        'wc': 'White Blood Cell Count (cells/cumm)',
        'rc': 'Red Blood Cell Count (millions/cmm)',
        'htn': 'Hypertension',
        'dm': 'Diabetes Mellitus',
        'cad': 'Coronary Artery Disease',
        'appet': 'Appetite',
        'pe': 'Pedal Edema',
        'ane': 'Anemia'
    }

    patient_info = ''

    for col, label in field_labels.items():
        value = df.iloc[0].get(col)
        if pd.notna(value):
            patient_info += f'- {label}: {value}\n'

    prediction_text = 'No CKD suspected' if pred == 0 else 'Possible risk of CKD'

    prompt = f'''
        Patient Information:
        {patient_info}

        Prediction: {prediction_text}

        Write a SHORT (max 5-6 sentences), professional, empathetic message directly to the patient based on the provided information.

        - DO NOT explain that you are an AI.
        - DO NOT include extra commentary or instructions.
        - DO NOT mention this is generated by AI.
        - ONLY output the final message as if speaking to the patient.

        Make it clear that this is NOT a diagnosis and recommend consulting a healthcare professional.
        '''.strip()

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model='gemini-2.5-pro-exp-03-25', contents=prompt
    )
    return response.text

def impute_values(df, impute_df):
    result = {}
    
    for column in impute_df.columns:
        if impute_df[column].dtype == 'object':
            result[column] = impute_df[column].mode()[0]
        else:
            result[column] = impute_df[column].median()
    
    df = df.fillna(result)

    return df

_ = load_dotenv()
api_key = os.getenv('API_KEY')

expected_cols = [
    'age', 'bp', 'sg', 'al', 'su', 'rbc', 'pc', 'pcc',
    'ba', 'bgr', 'bu', 'sc', 'sod', 'pot', 'hemo', 'pcv', 
    'wc', 'rc', 'htn', 'dm', 'cad', 'appet', 'pe', 'ane',
]

if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'submitted' not in st.session_state:
    st.session_state.submitted = False
if 'user_prompt' not in st.session_state:
    st.session_state.user_prompt = ''
if 'user_files' not in st.session_state:
    st.session_state.user_files = []
if 'expanded' not in st.session_state:
    st.session_state.expanded = True
if 'expander_open' not in st.session_state:
    st.session_state.expander_open = True
if 'disable_button' not in st.session_state:
    st.session_state.disable_buttons = False

def toggle_expander():
    st.session_state.expander_open = not st.session_state.expander_open

def toggle_button():
    st.session_state.disable_buttons = not st.session_state.disable_buttons

disabled = st.session_state.disable_buttons

st.set_page_config(page_title='CKD Predictor', page_icon='⚙️', layout='wide')
st.title('⚙️ CKD Predictor')

with st.expander('Example prompt'):
    if st.button('Try this example', disabled=disabled):
        toggle_button()
        toggle_expander()
        st.session_state.user_prompt = 'I\'m 43 years old, and my recent blood tests showed a specific gravity of 1.010. I have been feeling quite fatigued, and my doctor mentioned I might have anemia. My blood pressure is high, and I have a poor appetite.'
        st.session_state.user_files = ['notebooks/llm_src/example_cmp.png','notebooks/llm_src/example_cbc_2.png']
        st.session_state.submitted = True
        st.session_state.messages.append({'role': 'user', 'content': st.session_state.user_prompt + '  \nFiles uploaded.'})
        st.rerun()

    st.write('I\'m 43 years old, and my recent urine tests showed a specific gravity of 1.010. I have been feeling quite fatigued, and my doctor mentioned I might have anemia. My blood pressure is high, and I have a poor appetite.')
    st.image(['notebooks/llm_src/example_cmp.png','notebooks/llm_src/example_cbc_2.png'], use_container_width=True)

prompt = st.text_input('Enter your health conditions:', placeholder='I am XX years old...')

uploaded_files = st.file_uploader(
    'Upload lab reports:',
    accept_multiple_files=True,
    type=['txt', 'pdf', 'jpg', 'png']
)

if st.button('Submit', disabled=disabled):
    if not prompt and not uploaded_files:
        st.write('Please input your health conditions.')
    else:
        st.session_state.user_prompt = prompt
        st.session_state.user_files = uploaded_files
        st.session_state.submitted = True

        if prompt and not uploaded_files:
            st.session_state.messages.append({'role': 'user', 'content': prompt})
        elif uploaded_files and not prompt:
            st.session_state.messages.append({'role': 'user', 'content': 'You uploaded files.'})
        elif prompt and uploaded_files:
            st.session_state.messages.append({'role': 'user', 'content': prompt + '  \nFiles uploaded.'})

        st.rerun()

model = load('streamlit/random_forest_model.joblib')

ckd_df = pd.read_csv('notebooks/ckd_preprocessed.csv')

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

if st.session_state.submitted:
    with st.spinner('🫘 PrognosiX is thinking...'):
        multi_test_df = pd.DataFrame(columns=expected_cols)

        dfs = []

        prompt = st.session_state.user_prompt
        uploaded_files = st.session_state.user_files

        try:   
            if prompt:
                text = get_pairs_text(prompt)
                dfs.append(response_to_df(text))
            if uploaded_files:
                if type(uploaded_files[0]) == str:
                    for file in uploaded_files:
                        text = get_pairs_image(file)
                        dfs.append(response_to_df(text))
                else:
                    for file in uploaded_files:
                        with open(os.getcwd()+'/streamlit/files/'+file.name, 'wb') as f:
                            f.write(file.getbuffer())
                            
                    for file in glob.glob(os.getcwd()+'/streamlit/files/*'):
                        text = get_pairs_image(file)
                        dfs.append(response_to_df(text))
                
                    for file in glob.glob(os.getcwd()+'/streamlit/files/*'):
                        os.remove(file)
        except Exception as e:
            st.session_state.messages.append({'role': 'assistant', 'content': 'Ran out of LLM calls. Please try again tomorrow.'})
            st.session_state.submitted = False
            st.rerun()

        try:
            all_df = pd.concat(dfs, ignore_index=True)
            result_row = all_df.bfill(axis=0).iloc[0]
            multi_test_df.loc[0] = result_row

            nan_counts = multi_test_df.isna().sum(axis=1).iloc[0]
            if nan_counts > 19: # requires at least 5 health condition variables 
                st.session_state.messages.append({'role': 'assistant', 'content': 'You did not input enough information for us to predict whether you have Chronic Kidney Disease. Please try again.'})
                st.session_state.submitted = False
                st.rerun()
        except:
            st.session_state.messages.append({'role': 'assistant', 'content': 'You did not input enough information for us to predict whether you have Chronic Kidney Disease. Please try again.'})
            st.session_state.submitted = False
            st.rerun()

        label_encoder = LabelEncoder()

        object_columns_list = multi_test_df.select_dtypes(include=['object']).columns.tolist()

        for object_column in object_columns_list:
            multi_test_df[object_column] = label_encoder.fit_transform(multi_test_df[object_column])
        pred = model.predict([multi_test_df.loc[0]])

        response = create_response(pred, multi_test_df)

        st.session_state.messages.append({'role': 'assistant', 'content': response})
        st.session_state.submitted = False
<<<<<<< HEAD:streamlit/pages/CKD Predictor.py
        st.toast('Response finished generating.', icon='🫘')
        st.rerun()
=======
        st.rerun()

if st.button('Submit'):
    if not prompt and not uploaded_files:
        st.write('Please input your health information')
    else:
        st.session_state.user_prompt = prompt
        st.session_state.user_files = uploaded_files
        st.session_state.submitted = True

        if prompt and not uploaded_files:
            st.session_state.messages.append({'role': 'user', 'content': prompt})
        elif uploaded_files and not prompt:
            st.session_state.messages.append({'role': 'user', 'content': 'You uploaded files.'})
        elif prompt and uploaded_files:
            st.session_state.messages.append({'role': 'user', 'content': prompt + + '\nFiles uploaded.'})

        st.rerun()
>>>>>>> 911f25a (Add newline @ EOF):streamlit/pages/LLM.py
