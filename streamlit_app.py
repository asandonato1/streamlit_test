import streamlit as st
import pymysql
import pandas as pd
import ID3
from sklearn import preprocessing

def main():
    st.write("Hello World!")
    conn = st.connection('mysql', type='sql')
    query = "SELECT * FROM mytable"
    

    df = pd.read_sql(conn.query(query, ttl=600), con=conn)
    c = st.text_input('input?: ')
    if(c == 'Sim'):
        outlook = st.text_input("Outlook: ")
        temp = st.text_input("Temperature: ")
        hum  = st.text_input("Humidity: ")
        wind = st.text_input("Wind: ")
        PT = st.text_input("PT? : ")
        num = df.shape[0] + 1
        cursor = conn.cursor()
        cursor.execute('INSERT INTO mytable VALUES(%s, %s, %s, %s, %s, %s)', (outlook, temp, hum, wind, PT, num))
        df = pd.read_sql(query, con=conn)

    st.write(df)

    df.drop(columns=["num"], inplace=True)
    df = df.apply(preprocessing.LabelEncoder().fit_transform)
    x = df.columns.to_numpy()
    x = x[:-1]; x
    x = df[x]

    y = df.PT

   # st.write(x)
    x, y = ID3.ID3(df, x, y, 0.8)

    st.write(x)    
    st.write("\n", y)

main()