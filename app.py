from dotenv import load_dotenv
load_dotenv() ## Load all the environemnt variables

import streamlit as st
import os
import sqlite3

import google.generativeai as genai

## Configure Genai Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function To Load Google Gemini Model and provide queries as response

def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text

## Fucntion To retrieve query from the database

def read_sql_query(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows

## Define Your Prompt

prompt=["""
        You are an expert in converting English questions into SQL queries. The database is named STUDENT and includes the following columns: NAME, CLASS, SECTION, and MARKS.
        Examples:

        1. Count Records

        Question: How many records are there in the database?
        SQL Query: SELECT COUNT(*) FROM STUDENT;

        2. Retrieve Specific Data

        Question: List all students who are in the "Data Science" class.
        SQL Query: SELECT * FROM STUDENT WHERE CLASS = 'Data Science';
        For each query, ensure that the SQL command is precise and free from unnecessary syntax or additional keywords. Do not include any extra formatting such as backticks or the word "SQL" in the output.

        Also the sql code should not have ``` in beginning or end and sql word in output        

    """]

## Streamlit App

st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini App To Retrieve SQL Data")

question=st.text_input("Input: ",key="input")

submit=st.button("Ask the question")

# If submit is clicked
if submit:
    response=get_gemini_response(question,prompt)
    print(response)
    response=read_sql_query(response,"student.db")
    st.subheader("The Response is")
    for row in response:
        print(row)
        st.header(row)