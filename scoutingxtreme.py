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
    st.subheader("IN PROGRESS")

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
    st.subheader("IN PROGRESS")

elif sect == "Edit Items":

    st.write("**Note: Removing items will remove ALL DATA associated with that item.**")

    c1, c2 = st.columns(2)

    ex1 = c1.expander("Current Pit Items")

    if len(st.session_state.pitq) == 0:
        ex1.header("No Pit Items Added Yet.")

    else:
        ex1.header("Current Pit Items")
        
        for m in st.session_state.pitq:

            items = [i for i in st.session_state.pitq.keys()]
            num = items.index(m)

            if st.session_state.pitq[m]["Type"] == "Header":
                ex1.subheader(f":blue[{num+1}. {m}] - :red[Header]")
            else:
                ex1.subheader(f"{num+1}. {m}")

            for x, y in st.session_state.pitq[m].items():

                if x == "Options":
                    
                    msg = f" - **{x}**: "

                    for i in st.session_state.pitq[m][x]:
                        msg += f"{i}, "
                    
                    msg = msg[:-2]
                    
                    ex1.write(msg)
                                
                elif st.session_state.pitq[m]["Type"] != "Header":
                    ex1.write(f" - **{x}**: {y}")

    ex1.write("---")

    ex2 = c2.expander("Current Match Items")
    
    if len(st.session_state.matchq) == 0:
        ex2.header("No Match Items Added Yet.")
    
    else:

        ex2.header("Current Match Items")

        for m in st.session_state.matchq:

            items = [i for i in st.session_state.matchq.keys()]
            num = items.index(m)

            if st.session_state.matchq[m]["Type"] == "Header":
                ex2.subheader(f":blue[{num+1}. {m}] - :red[Header]")
            else:
                ex2.subheader(f"{num+1}. {m}")

            for x, y in st.session_state.matchq[m].items():

                if x == "Options":
                    
                    msg = f" - **{x}**: "

                    for i in st.session_state.matchq[m][x]:
                        msg += f"{i}, "
                    
                    msg = msg[:-2]
                    
                    ex2.write(msg)
                
                elif st.session_state.matchq[m]["Type"] != "Header":
                    ex2.write(f" - **{x}**: {y}")

    ex2.write("---")

    qsect = st.sidebar.radio("**Which set of questions would you like to edit?**", ["Pit", "Match"])
    qedit = st.sidebar.radio("**Would you like to add or remove a question?**", ["Add", "Remove"])

    if qedit == "Remove":

        if qsect == "Pit":
                
            if len(st.session_state.pitq) == 0:
                st.header("There are no match questions yet.")

            else:

                itemnum = st.number_input("**Enter the number of the item you'd like to remove:**", 1, len(st.session_state.matchq), step=1)-1
                items = [i for i in st.session_state.pitq]

                if st.sidebar.button("Remove Item"):

                    if items[itemnum] in st.session_state.pitdata:
                        del st.session_state.pitdata[items[itemnum]]

                    if items[itemnum] in st.session_state.pitq:
                        del st.session_state.pitq[items[itemnum]]
                    
                    st.sidebar.subheader("Item Removed Successfully.")

        if qsect == "Match":
            
            if len(st.session_state.matchq) == 0:
                st.header("There are no match questions yet.")

            else:

                itemnum = st.number_input("**Enter the number of the item you'd like to remove:**", 1, len(st.session_state.matchq), step=1)-1
                items = [i for i in st.session_state.matchq]

                if st.sidebar.button("Remove Item"):

                    if items[itemnum] in st.session_state.matchdata:
                        del st.session_state.matchdata[items[itemnum]]

                    if items[itemnum] in st.session_state.matchq:
                        del st.session_state.matchq[items[itemnum]]
                    
                    st.sidebar.subheader("Item Removed Successfully.")

    else:

        if qsect == "Pit":
            
            if len(st.session_state.pitq) == 0:
                st.subheader(f"No {qsect} Items Added Yet.")

            qtypes = ["Header", "Columns Separator", "Columns Item", "Selection Box", "Multiple Choice", "Number Input", "Text Input"]
            qtype = c1.selectbox("**What type of element would you like to add?**", qtypes)
            
            if qtype == "Header":

                qname = c2.text_input("**What should the header say?**")

                if st.sidebar.button("Add Item"):
                    st.session_state.pitq[qname] = {"Type": qtype}

            elif qtype == "Columns Separator":
                qname = c2.number_input("**How many columns should it separate into?**", 2, 5)

            elif qtype == "Columns Item":
                qname = c2.text_input("**What should the name of this item be?**")

            else:

                qname = c2.text_input("**What should this question ask?**")
                    
                if qtype in "Text Input":
                    if st.sidebar.button("Add Item"):
                        st.session_state.pitq[qname] = {"Type": qtype, "Character Limit": 200}

                elif qtype in "Number Input":

                    qmin = c1.number_input("**Minimum Value**", step=1)
                    qmax = c2.number_input("**Maximum Value**", step=1)

                    if st.sidebar.button("Add Item"):
                        st.session_state.pitq[qname] = {"Type": qtype, "Minimum": qmin, "Maximum": qmax}

                else:

                    qoptsnum = c1.number_input("**How many options should this question have?**", 2, step=1)
                    qdefindex = c2.number_input("**Enter the number of the option that this question should default to:**", min_value=1, max_value=qoptsnum, step=1)-1

                    qopts = []

                    if qoptsnum > 0:
                        for q in range(qoptsnum):
                            qopts.append(st.text_input(f"Option {q+1}:"))
                
                if st.sidebar.button("Add Item"):
                    
                    newcol = ["N/A" for i in range(len(st.session_state.pitdata))]

                    newcol.append("N/A")

                    st.session_state.pitq[qname] = {"Type": qtype, "Options": qopts, "DefaultIndex": qdefindex}
                    st.session_state.pitdata[qname] = newcol

        if qsect == "Match":

            if len(st.session_state.matchq) == 0:
                st.subheader(f"No {qsect} Items Added Yet.")

            qtypes = ["Header", "Columns Separator", "Columns Item", "Selection Box", "Multiple Choice", "Number Input", "Text Input"]
            qtype = c1.selectbox("**What type of element would you like to add?**", qtypes)
            
            if qtype == "Header":

                qname = c2.text_input("**What should the header say?**")

                if st.sidebar.button("Add Item"):
                    st.session_state.matchq[qname] = {"Type": qtype}

            elif qtype == "Columns Separator":
                qname = c2.number_input("**How many columns should it separate into?**", 2, 5)

            elif qtype == "Columns Item":
                qname = c2.text_input("**What should the name of this item be?**")

            else:

                qname = c2.text_input("**What should this question ask?**")
                    
                if qtype in "Text Input":
                    if st.sidebar.button("Add Item"):
                        st.session_state.matchq[qname] = {"Type": qtype, "Character Limit": 200}

                elif qtype in "Number Input":

                    qmin = c1.number_input("**Minimum Value**", step=1)
                    qmax = c2.number_input("**Maximum Value**", step=1)

                    if st.sidebar.button("Add Item"):
                        st.session_state.matchq[qname] = {"Type": qtype, "Minimum": qmin, "Maximum": qmax}

                else:

                    qoptsnum = c1.number_input("**How many options should this question have?**", 2, step=1)
                    qdefindex = c2.number_input("**Enter the number of the option that this question should default to:**", min_value=1, max_value=qoptsnum, step=1)-1

                    qopts = []

                    if qoptsnum > 0:
                        for q in range(qoptsnum):
                            qopts.append(st.text_input(f"Option {q+1}:"))
                
                if st.sidebar.button("Add Item"):
                    
                    newcol = ["N/A" for i in range(len(st.session_state.matchdata))]

                    newcol.append("N/A")

                    st.session_state.matchq[qname] = {"Type": qtype, "Options": qopts, "DefaultIndex": qdefindex}
                    st.session_state.matchdata[qname] = newcol
        
    if st.sidebar.button("Save Items"):

        open("questions.py", "w").write(f"pitq = {st.session_state.pitq}\nmatchq = {st.session_state.matchq}")
        open("scoutingsrc.py", "w").write(f"pitdata = {st.session_state.pitdata}\nmatchdata = {st.session_state.matchdata}")
        st.sidebar.subheader("**Items Saved Successfully.**")
        time.sleep(3)

elif sect == "Edit Data":
    st.subheader("IN PROGRESS")
