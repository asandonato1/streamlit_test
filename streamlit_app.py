import streamlit as st
import pandas as pd
import ID3
from sklearn import preprocessing
import pymysql

def main():
    st.write("Hello World!")
    connection = st.connection('mysql', type='sql')
    query = "SELECT * FROM mytable"

    df = pd.read_sql(connection.query(query, ttl=600), con=connection)

    df = pd.read_sql(query, con=connection)
    df.drop(columns=['num'], inplace=True)  
    df = pd.DataFrame(df)
    st.session_state.df = df

    with st.form("add_coisas"):
        outlook = st.selectbox("Outlook", ["Sunny", "Overcast", "Rain"])
        temp = st.selectbox("Temperature", ["Hot", "Mild", "Cold"])
        hum = st.selectbox("Humidity", ["High", "Normal"])
        wind = st.selectbox("Wind", ["Weak", "Strong"])
        pt = st.selectbox("PT?", ["Yes", "No"])
        submit = st.form_submit_button("submit? ")

    if submit:
        df_new = pd.DataFrame(
            [
                {
                    "Outlook": outlook,
                    "Temperature": temp,
                    "Humidity": hum,
                    "Wind": wind,
                    "PT": pt
                }
            ]
        )
        st.dataframe(df_new, use_container_width=True, hide_index=True)
        st.session_state.df = pd.concat([df_new, st.session_state.df], axis=0)
    df_ed = st.data_editor(
        st.session_state.df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Outlook": st.column_config.SelectboxColumn(
                "Outlook",
                help='Outlook',
                options=['Sunny', 'Overcast', 'Rain'],
                required=True
            ),
        }
    )

    df_ed = df_ed.apply(preprocessing.LabelEncoder().fit_transform)
    x = df_ed.columns.to_numpy()
    x = x[:-1]; x
    x = df_ed[x]

    y = df_ed.PT

   # st.write(x)
    x, y = ID3.ID3(df_ed, x, y, 0.8)

 #   st.write(x)    
    st.write("\n", y)

main()