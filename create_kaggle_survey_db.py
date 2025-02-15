

# 以 pandas 模組載入資料

#* 分三個檔案載入：
#* 2020 Kaggle Machine Learning & Data Science Survey
#* 2021 Kaggle Machine Learning & Data Science Survey
#* 2022 Kaggle Machine Learning & Data Science Survey
#* low_memory=False: 遭遇混合資料類型且沒有指定欄位的資料類型時設定。

import pandas as pd

survey_years = [2020, 2021, 2022]
df_dict = dict()
for survey_year in survey_years:
    file_path = f"data/kaggle_survey_{survey_year}_responses.csv"  # place holder
    df = pd.read_csv(file_path, low_memory=False)                  # low_memory=False 避免 dtype warning
    df_dict[survey_year] = df
    
    
# 檢視載入成果

# print(df_dict[2020].head())
df_dict[2020].head()
df_dict[2021].head()
df_dict[2022].head()


# 檢視後調整載入邏輯

#* 應該將資料分做兩部分載入。
#* 題目敘述。
#* 填答回覆。
#* skiprows=[1]: 略過第一列資料不載入。
#* [1:]: 刪除填答時間的欄位。


survey_years = [2020, 2021, 2022]
df_dict = dict()
for survey_year in survey_years:
    file_path = f"data/kaggle_survey_{survey_year}_responses.csv"
    df = pd.read_csv(file_path, low_memory=False, skiprows=[1])
    df = df.iloc[:, 1:]                        # slicing 1: 省略第0欄
    df_dict[survey_year, "responses"] = df
    df = pd.read_csv(file_path, nrows=1) 
    question_descriptions = df.values.ravel()  # ndarray 儲存 (ravel 一維)
    question_descriptions = question_descriptions[1:]
    df_dict[survey_year, "question_descriptions"] = question_descriptions
    
 
# 重新檢視載入成果

for survey_year in survey_years:
    df_dict[survey_year, "question_descriptions"]
    print(df_dict[survey_year, "responses"])


df_dict[2020, "question_descriptions"]
df_dict[2020, "responses"].head()
df_dict[2021, "question_descriptions"]
df_dict[2021, "responses"].head()
df_dict[2022, "question_descriptions"]
df_dict[2022, "responses"]


# 2020/2021 年資料整理

#* 確定資料型態
survey_year = 2020
column_names = df_dict[survey_year, "responses"].columns
for elem in column_names:
    print(elem)
    print(elem.split("_"))        # 分割符

descriptions = df_dict[survey_year, "question_descriptions"]
for elem in descriptions:
    print(elem)
    print(elem.split(" - "))      # 分割符

import string
print(string.ascii_uppercase)
print("A" in string.ascii_uppercase)
print("B" in string.ascii_uppercase)
print("Part" in string.ascii_uppercase)


import string

survey_year = 2020
question_indexes, question_types, question_descriptions = [], [], []        # 建立 空的list
column_names = df_dict[survey_year, "responses"].columns
descriptions = df_dict[survey_year, "question_descriptions"]
for column_name, question_description in zip(column_names, descriptions):
    column_name_split = column_name.split("_")
    question_description_split = question_description.split(" - ")
    if len(column_name_split) == 1:
        question_index = column_name_split[0]
        question_indexes.append(question_index)
        question_types.append("Multiple choice")
        question_descriptions.append(question_description_split[0])
    else:
        if column_name_split[1] in string.ascii_uppercase:
            question_index = column_name_split[0] + column_name_split[1]
            question_indexes.append(question_index)
        else:
            question_index = column_name_split[0]
            question_indexes.append(question_index)
        question_types.append("Multiple selection")
        question_descriptions.append(question_description_split[0])

print(question_indexes)
print(question_types)
print(question_descriptions)


question_df = pd.DataFrame()
question_df["question_index"] = question_indexes
question_df["question_type"] = question_types
question_df["question_description"] = question_descriptions
question_df["surveyed_in"] = survey_year
#* groupby 取唯一值
question_df = question_df.groupby(["question_index", "question_type", "question_description", "surveyed_in"]).count().reset_index()
question_df.head()


response_df = df_dict[survey_year, "responses"]
response_df.columns = question_indexes
response_df_reset_index = response_df.reset_index() #受訪者流水編號
#* melt 轉置
response_df_melted = pd.melt(response_df_reset_index, id_vars="index", var_name="question_index", value_name="response")
#print(response_df_reset_index)
#print(response_df_melted)
response_df_melted["responded_in"] = survey_year
response_df_melted = response_df_melted.rename(columns={"index": "respondent_id"})
response_df_melted = response_df_melted.dropna().reset_index(drop=True)
response_df_melted


# 2022 年資料整理

survey_year = 2022
question_indexes, question_types, question_descriptions = [], [], []
column_names = df_dict[survey_year, "responses"].columns
descriptions = df_dict[survey_year, "question_descriptions"]
for column_name, question_description in zip(column_names, descriptions):
    column_name_split = column_name.split("_")
    question_description_split = question_description.split(" - ")
    if len(column_name_split) == 1:
        question_types.append("Multiple choice")
    else:
        question_types.append("Multiple selection")
    question_index = column_name_split[0]
    question_indexes.append(question_index)
    question_descriptions.append(question_description_split[0])

#print(question_indexes)
#print(question_types)
#print(question_descriptions)      

question_df = pd.DataFrame()
question_df["question_index"] = question_indexes
question_df["question_type"] = question_types
question_df["question_description"] = question_descriptions
question_df["surveyed_in"] = survey_year
question_df = question_df.groupby(["question_index", "question_type", "question_description", "surveyed_in"]).count().reset_index()
question_df.head()

response_df = df_dict[survey_year, "responses"]
response_df.columns = question_indexes
response_df_reset_index = response_df.reset_index()
response_df_melted = pd.melt(response_df_reset_index, id_vars="index", var_name="question_index", value_name="response")
response_df_melted["responded_in"] = survey_year
response_df_melted = response_df_melted.rename(columns={"index": "respondent_id"})
response_df_melted = response_df_melted.dropna().reset_index(drop=True)
response_df_melted

# 整理程式碼為一個類別 CreateKaggleSurveyDB

import pandas as pd
import string
import sqlite3

class CreateKaggleSurveyDB:
    def __init__(self):
        survey_years = [2020, 2021, 2022]
        df_dict = dict()
        for survey_year in survey_years:
            file_path = f"data/kaggle_survey_{survey_year}_responses.csv"
            df = pd.read_csv(file_path, low_memory=False, skiprows=[1])
            df = df.iloc[:, 1:]
            df_dict[survey_year, "responses"] = df
            df = pd.read_csv(file_path, nrows=1)
            question_descriptions = df.values.ravel()
            question_descriptions = question_descriptions[1:]
            df_dict[survey_year, "question_descriptions"] = question_descriptions
        self.survey_years = survey_years  #做成屬性
        self.df_dict = df_dict

    def tidy_2020_2021_data(self, survey_year: int) -> tuple:
        question_indexes, question_types, question_descriptions = [], [], []
        column_names = self.df_dict[survey_year, "responses"].columns
        descriptions = self.df_dict[survey_year, "question_descriptions"]
        for column_name, question_description in zip(column_names, descriptions):
            column_name_split = column_name.split("_")
            question_description_split = question_description.split(" - ")
            if len(column_name_split) == 1:
                question_index = column_name_split[0]
                question_indexes.append(question_index)
                question_types.append("Multiple choice")
                question_descriptions.append(question_description_split[0])
            else:
                if column_name_split[1] in string.ascii_uppercase:
                    question_index = column_name_split[0] + column_name_split[1]
                    question_indexes.append(question_index)
                else:
                    question_index = column_name_split[0]
                    question_indexes.append(question_index)
                question_types.append("Multiple selection")
                question_descriptions.append(question_description_split[0])
        question_df = pd.DataFrame()
        question_df["question_index"] = question_indexes
        question_df["question_type"] = question_types
        question_df["question_description"] = question_descriptions
        question_df["surveyed_in"] = survey_year
        question_df = question_df.groupby(["question_index", "question_type", "question_description", "surveyed_in"]).count().reset_index()
        response_df = self.df_dict[survey_year, "responses"]
        response_df.columns = question_indexes
        response_df_reset_index = response_df.reset_index()
        response_df_melted = pd.melt(response_df_reset_index, id_vars="index", var_name="question_index", value_name="response")
        response_df_melted["responded_in"] = survey_year
        response_df_melted = response_df_melted.rename(columns={"index": "respondent_id"})
        response_df_melted = response_df_melted.dropna().reset_index(drop=True)
        return question_df, response_df_melted

    def tidy_2022_data(self, survey_year: int) -> tuple:
        question_indexes, question_types, question_descriptions = [], [], []
        column_names = self.df_dict[survey_year, "responses"].columns
        descriptions = self.df_dict[survey_year, "question_descriptions"]
        for column_name, question_description in zip(column_names, descriptions):
            column_name_split = column_name.split("_")
            question_description_split = question_description.split(" - ")
            if len(column_name_split) == 1:
                question_types.append("Multiple choice")
            else:
                question_types.append("Multiple selection")
            question_index = column_name_split[0]
            question_indexes.append(question_index)
            question_descriptions.append(question_description_split[0])
        question_df = pd.DataFrame()
        question_df["question_index"] = question_indexes
        question_df["question_type"] = question_types
        question_df["question_description"] = question_descriptions
        question_df["surveyed_in"] = survey_year
        question_df = question_df.groupby(["question_index", "question_type", "question_description", "surveyed_in"]).count().reset_index()
        response_df = self.df_dict[survey_year, "responses"]
        response_df.columns = question_indexes
        response_df_reset_index = response_df.reset_index()
        response_df_melted = pd.melt(response_df_reset_index, id_vars="index", var_name="question_index", value_name="response")
        response_df_melted["responded_in"] = survey_year
        response_df_melted = response_df_melted.rename(columns={"index": "respondent_id"})
        response_df_melted = response_df_melted.dropna().reset_index(drop=True)
        return question_df, response_df_melted
    
    def create_database(self):
        question_df = pd.DataFrame()
        response_df = pd.DataFrame()
        for survey_year in self.survey_years:
            if survey_year == 2022:
                q_df, r_df = self.tidy_2022_data(survey_year)
            else:
                q_df, r_df = self.tidy_2020_2021_data(survey_year)
            question_df = pd.concat([question_df, q_df], ignore_index=True)  # concat 垂直合併
            response_df = pd.concat([response_df, r_df], ignore_index=True)
        connection = sqlite3.connect("data/kaggle_survey.db")
        question_df.to_sql("questions", con=connection, if_exists="replace", index=False)
        response_df.to_sql("responses", con=connection, if_exists="replace", index=False)
        cur = connection.cursor()      
        # 建立 檢視表
        drop_view_sql = """
        DROP VIEW IF EXISTS aggregated_responses;
        """
        create_view_sql = """
        CREATE VIEW aggregated_responses AS
        SELECT questions.surveyed_in,
               questions.question_index,
               questions.question_type,
               questions.question_description,
               responses.response,
               COUNT(responses.respondent_id) AS response_count
          FROM responses
          JOIN questions
            ON responses.question_index = questions.question_index AND
               responses.responded_in = questions.surveyed_in
         GROUP BY questions.surveyed_in,
                  questions.question_index,
                  responses.response; 
        """
        cur.execute(drop_view_sql)
        cur.execute(create_view_sql)
        connection.close()


# 檢查類別 CreateKaggleSurveyDB 能否順利運行

create_kaggle_survey_db = CreateKaggleSurveyDB() # 初始化
create_kaggle_survey_db.create_database()