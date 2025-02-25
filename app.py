import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

# Загрузка модели и энкодеров
model = joblib.load('schizophrenia_model.pkl')
encoder = joblib.load('label_encoder.pkl')

# Словари для отображения текста в интерфейсе и числовых значений для модели
gender_options = {0: 'Female', 1: 'Male'}
education_options = {0: 'Primary', 1: 'Middle School', 2: 'High School', 3: 'University', 4: 'Postgraduate'}
marital_status_options = {0: 'Single', 1: 'Married', 2: 'Divorced', 3: 'Widowed'}
occupation_options = {0: 'Unemployed', 1: 'Employed', 2: 'Retired', 3: 'Student'}
income_level_options = {0: 'Low', 1: 'Medium', 2: 'High'}
family_history_options = {0: 'No', 1: 'Yes'}
substance_use_options = {0: 'No', 1: 'Yes'}
suicide_attempt_options = {0: 'No', 1: 'Yes'}
social_support_options = {0: 'Low', 1: 'Medium', 2: 'High'}
stress_factors_options = {0: 'Low', 1: 'Medium', 2: 'High'}
medication_compliance_options = {0: 'No', 1: 'Yes'}

# Заголовок
st.title('Schizophrenia Diagnosis Prediction')

# Ввод данных с помощью Streamlit
age = st.number_input('Age', min_value=18, max_value=80, value=25)

# Ввод через selectbox с отображением текста, но сохранением числовых значений
gender = st.selectbox('Gender', options=['Female', 'Male'])
education_level = st.selectbox('Education Level', options=['Primary', 'Middle School', 'High School', 'University', 'Postgraduate'])
marital_status = st.selectbox('Marital Status', options=['Single', 'Married', 'Divorced', 'Widowed'])
occupation = st.selectbox('Occupation', options=['Unemployed', 'Employed', 'Retired', 'Student'])
income_level = st.selectbox('Income Level', options=['Low', 'Medium', 'High'])
family_history = st.selectbox('Family History of Schizophrenia', options=['No', 'Yes'])
substance_use = st.selectbox('Substance Use', options=['No', 'Yes'])
suicide_attempt = st.selectbox('Suicide Attempt', options=['No', 'Yes'])
social_support = st.selectbox('Social Support', options=['Low', 'Medium', 'High'])
stress_factors = st.selectbox('Stress Factors', options=['Low', 'Medium', 'High'])
medication_compliance = st.selectbox('Medication Compliance', options=['No', 'Yes'])

# Преобразование ввода в числовые данные для модели
input_data = {
    'Age': age,
    'Gender': list(gender_options.keys())[list(gender_options.values()).index(gender)],
    'Education_Level': list(education_options.keys())[list(education_options.values()).index(education_level)],
    'Marital_Status': list(marital_status_options.keys())[list(marital_status_options.values()).index(marital_status)],
    'Occupation': list(occupation_options.keys())[list(occupation_options.values()).index(occupation)],
    'Income_Level': list(income_level_options.keys())[list(income_level_options.values()).index(income_level)],
    'Family_History_of_Schizophrenia': list(family_history_options.keys())[list(family_history_options.values()).index(family_history)],
    'Substance_Use': list(substance_use_options.keys())[list(substance_use_options.values()).index(substance_use)],
    'Suicide_Attempts': list(suicide_attempt_options.keys())[list(suicide_attempt_options.values()).index(suicide_attempt)],
    'Social_Support': list(social_support_options.keys())[list(social_support_options.values()).index(social_support)],
    'Stress_Factors': list(stress_factors_options.keys())[list(stress_factors_options.values()).index(stress_factors)],
    'Medication_Compliance': list(medication_compliance_options.keys())[list(medication_compliance_options.values()).index(medication_compliance)]
}

input_df = pd.DataFrame([input_data]) 

# Предсказание с использованием модели
if st.button('Predict'):
    prediction = model.predict(input_df)[0]
    if prediction == 0:
        st.write("Prediction: The person is not schizophrenic.")
    else:
        st.write("Prediction: The person may be schizophrenic.")


# Загрузка данных
df = pd.read_csv("backend/schizophrenia_dataset.csv")
df = df[['Diagnosis', 'Age', 'Gender', 'Education_Level', 'Marital_Status','Occupation', 'Income_Level', 
                'Family_History_of_Schizophrenia','Substance_Use', 'Suicide_Attempts',
                'Social_Support', 'Stress_Factors', 'Medication_Compliance']]

# Корреляционная матрица
correlation_matrix = df.corr()

# Построение тепловой карты
fig, ax = plt.subplots(figsize=(10,6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', ax=ax, vmin=-1, vmax=1)

# Настроим график
ax.set_title('Correlation Matrix of Features')
st.pyplot(fig)
