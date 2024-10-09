# To Do:
#
# Finish data editing and resetting functions
# Add inserting questions into specific spots functionality
# Add data comparison and visual representation functionality

############################################################################################################################################################################################################################################################################################

# Importing necessities

import streamlit as st
import os
import time

requiredmodules = [
    "pandas",
    "matplotlib",
    "seaborn"
]

requirements = ""

for module in requiredmodules:
    requirements = requirements+f"\n{module}"

with open("requirements.txt", "w") as file:
    file.write(requirements)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn

############################################################################################################################################################################################################################################################################################

# Program Start

import scoutingsrc as src
import scoutingbackup as backup
import questions

st.set_page_config("Scouting XTREME", layout="wide", page_icon="icon.png", initial_sidebar_state="expanded")
pd.set_option("display.max_rows", None, "display.max_columns", None)

if ["pitq", "matchq", "pitdata", "matchdata"] not in st.session_state:

    st.session_state.pitq = questions.pitq
    st.session_state.matchq = questions.matchq

    st.session_state.pitdata = src.pitdata
    st.session_state.matchdata = src.matchdata

if st.session_state.pitdata == {}:
    for i in st.session_state.pitq:
        st.session_state.pitdata[i] = []

if st.session_state.matchdata == {}:
    for i in st.session_state.matchq:
        st.session_state.matchdata[i] = []

sect = st.sidebar.radio("Navigation:", ["View Data", "Data Comparison", "Visual Analysis", "Input Data", "Reset Inputs", "Edit Items", "Edit Data"])

pitcols = []
for i in st.session_state.pitdata.keys():
    pitcols.append(i)

matchcols = []
for i in st.session_state.matchdata.keys():
    matchcols.append(i)
    

if sect == "Reset Inputs":
    st.subheader("Inputs have been reset successfully.")

else:
    st.title(sect)
    st.write("---")


if sect == "View Data":

    viewdata = st.sidebar.radio("Which data would you like to view?", ["Pit Data", "Match Data"])

    st.header(viewdata)

    if viewdata == "Pit Data":
        data = st.session_state.pitdata
    if viewdata == "Match Data":
        data = st.session_state.matchdata

    if type(data["Team No."]) == str:
        teamnums = [data["Team No."]]
    else:
        teamnums = data["Team No."]


    team = st.selectbox("Select a Team To View", pd.Series(["All"]+teamnums).unique())
    ex1 = st.sidebar.expander("Selected Columns:")

    st.write("---")

    selectedcols = []

    selectall = ex1.checkbox("Select All", value=True)

    for i in data.keys():

        if selectall:
            checkbox = ex1.checkbox(i, value=True)
        else:
            checkbox = ex1.checkbox(i)

        if checkbox:
            selectedcols.append(i)

    if type(data["Team No."]) == str:
        teamnums = [data["Team No."]]
    else:
        teamnums = data["Team No."]
    
    if st.sidebar.button("Reset Data"):

        with open("scoutingbackup.py", "w") as file:
            write = f"""
pitdata = {st.session_state.pitdata}
matchdata = {st.session_state.matchdata}
            """

            file.write(write)

        for i in st.session_state.pitq:
            st.session_state.pitdata[i] = []

        for i in st.session_state.matchq:
            st.session_state.matchdata[i] = []

        write = f"""
pitdata = {st.session_state.pitdata}
matchdata = {st.session_state.matchdata}
"""

        with open("scoutingsrc.py", "w") as file:
            file.write(write)
            
    if st.sidebar.button("Restore Data"):
        st.session_state.pitdata = backup.st.session_state.pitdata
        st.session_state.matchdata = backup.st.session_state.matchdata
        write = f"""
pitdata = {st.session_state.pitdata}
matchdata = {st.session_state.matchdata}
"""

        with open("scoutingsrc.py", "w") as file:
            file.write(write)

    st.sidebar.write("***Warning**: Backup data will be deleted if the 'Reset Data' button is pressed twice.*")

    df = pd.DataFrame().from_dict(data)
    rows = [i for i in range(len(df[selectedcols])) if df["Team No."][i] == team or team == "All"]

    st.dataframe(df[selectedcols].iloc[rows], use_container_width=True, hide_index=True)

    st.write("*Note: Double click on a cell to view all of its contents if it is cut off.*")
    
    st.write("---")

    c1, c2, c3 = st.columns(3)

    c1.write(f"**Teams Scouted:** {len(df['Team No.'].unique())}")
    c2.write(f"**Rounds Scouted:** {len(df)}")
    c3.write(f"**Total Rounds:** 0")

    datafilename = st.text_input("Data File Name:", "scoutingdata.txt")
    
    if datafilename[-4:] != ".txt":
        datafilename += ".txt"


    st.download_button("Download Data as .txt File (selected columns)", str(df[[i for i in selectedcols if i != "Extra Notes"]]), datafilename)
    
elif sect == "Data Comparison":
    st.header("COMING SOON")


elif sect == "Input Data":

    datasect = st.radio("Which data would you like to add to?", ["Pit Data", "Match Data"])
    inputs = []

    if datasect == "Pit Data":

        for q in st.session_state.pitq:
                
            if st.session_state.pitq[q]["Type"] in ["Header", "Columns Separator", "Columns Item"]:

                if st.session_state.pitq[q]["Type"] == "Header":
                    st.write("---")
                    st.header(q)
                    st.write("---")

            else:

                if st.session_state.pitq[q]["Type"] == "Number Input":
                    uin = str(st.number_input(f"**{q}**", st.session_state.pitq[q]["Minimum"], st.session_state.pitq[q]["Maximum"], step=1))

                elif st.session_state.pitq[q]["Type"] == "Text Input":
                    uin = st.text_input(f"**{q}**", max_chars=st.session_state.pitq[q]["Character Limit"])

                elif st.session_state.pitq[q]["Type"] == "Multiple Choice":
                    uin = st.radio(f"**{q}**", st.session_state.pitq[q]["Options"], index=st.session_state.pitq[q]["DefaultIndex"])

                elif st.session_state.pitq[q]["Type"] == "Selection Box":
                    uin = st.selectbox(f"**{q}**", st.session_state.pitq[q]["Options"])

                inputs.append(uin)
        
                st.subheader("")

        if st.sidebar.button("Submit"):
        
            for x, y in zip(st.session_state.pitdata.keys(), inputs):
                st.session_state.pitdata[x].append(y)
                
            write = f"""
pitdata = {st.session_state.pitdata}
matchdata = {st.session_state.matchdata}
                """

            with open("scoutingsrc.py", "w") as file:
                file.write(write)

    else:

        for q in st.session_state.matchq:
                
            if st.session_state.matchq[q]["Type"] in ["Header", "Columns Separator", "Columns Item"]:

                if st.session_state.matchq[q]["Type"] == "Header":
                    st.write("---")
                    st.header(q)
                    st.write("---")

            else:

                if st.session_state.matchq[q]["Type"] == "Number Input":
                    uin = str(st.number_input(f"**{q}**", st.session_state.matchq[q]["Minimum"], st.session_state.matchq[q]["Maximum"], step=1))

                elif st.session_state.matchq[q]["Type"] == "Text Input":
                    uin = st.text_input(f"**{q}**", max_chars=st.session_state.matchq[q]["Character Limit"])

                elif st.session_state.matchq[q]["Type"] == "Multiple Choice":
                    uin = st.radio(f"**{q}**", st.session_state.matchq[q]["Options"], index=st.session_state.matchq[q]["DefaultIndex"])

                elif st.session_state.matchq[q]["Type"] == "Selection Box":
                    uin = st.selectbox(f"**{q}**", st.session_state.matchq[q]["Options"])

                inputs.append(uin)
        
                st.subheader("")

        if st.sidebar.button("Submit"):
        
            for x, y in zip(st.session_state.matchdata.keys(), inputs):            
                st.session_state.matchdata[x].append(y)
                
            write = f"""
pitdata = {st.session_state.pitdata}
matchdata = {st.session_state.matchdata}
                """

            with open("scoutingsrc.py", "w") as file:
                file.write(write)

elif sect == "Visual Analysis":
    st.header("COMING SOON")


elif sect == "Edit Items":
    st.header("IN PROGRESS")
