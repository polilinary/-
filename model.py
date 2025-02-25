import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from imblearn.under_sampling import RandomUnderSampler
from sklearn.metrics import accuracy_score,confusion_matrix,classification_report
import joblib

df = pd.read_csv("backend/schizophrenia_dataset.csv")

df_CHOSEN = df[['Age', 'Gender', 'Education_Level', 'Marital_Status','Occupation', 'Income_Level', 
                'Family_History_of_Schizophrenia','Substance_Use', 'Suicide_Attempts',
                'Social_Support', 'Stress_Factors', 'Medication_Compliance',
                'Diagnosis']]

# Преобразование категориальных данных
categorical_columns = ['Gender', 'Education_Level', 'Marital_Status', 'Occupation', 
                       'Income_Level', 'Family_History_of_Schizophrenia', 
                       'Substance_Use', 'Suicide_Attempts', 'Social_Support', 'Stress_Factors', 'Medication_Compliance']

# Применение LabelEncoder для кодирования категориальных переменных
encoder = LabelEncoder()
for col in categorical_columns:
    df_CHOSEN[col] = encoder.fit_transform(df_CHOSEN[col])

# Разделение на признаки и таргет
X = df_CHOSEN.drop(columns=['Diagnosis'])
y = df_CHOSEN['Diagnosis']

# Разделение на тренировочную и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Применение undersampling для сбалансирования классов
undersampler = RandomUnderSampler(sampling_strategy='majority', random_state=42)
X_train_resampled, y_train_resampled = undersampler.fit_resample(X_train, y_train)

# Используем лучшие гиперпараметры для построения финальной модели
best_model = LogisticRegression(C=0.1, class_weight='balanced', max_iter=500, penalty='l1', solver='saga')

# Обучение модели на сбалансированных данных
best_model.fit(X_train_resampled, y_train_resampled)

# Предсказания
y_pred = best_model.predict(X_test)

# Сохранение модели и энкодеров
joblib.dump(best_model, 'schizophrenia_model.pkl')
joblib.dump(encoder, 'label_encoder.pkl')
