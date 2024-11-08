# To Do:
#
# Add data comparison and visual representation functionality
# Finish Data Editor
# Implement a working system log
# Add code modularity with easily modifiable functions or objects
# Add columns separator, column items and expanders to the Question Editor (columns)

############################################################################################################################################################################################################################################################################################

# Importing necessities
import streamlit as st
import os
import time

# Total rounds for the game
totalrounds = 0

# Modules that need to be installed
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
from io import StringIO

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

def gitupdate(savemsg: str ="Update GitHub"):
    os.system("git add .")
    os.system(f"git commit -m \"{savemsg}\"")
    os.system("git push")
    os.system("git pull")

def savequestions():
    
    writequestions = f"""
pitq = {st.session_state.pitq}
matchq = {st.session_state.matchq}
"""
    
    print(writequestions)

    try:
        with open("questions.py", "w") as file:
            file.write(writequestions)
        print("Questions Saved.")
    
    except:
        print("Questions could not be saved.")

def savedata():

    writedata = f"""
pitdata = {st.session_state.pitdata}
matchdata = {st.session_state.matchdata}
"""
    
    print(writedata)


    try:
        with open("scoutingsrc.py", "w") as file:
            file.write(writedata)
        print("Data Saved.")
    
    except:
        print("Data could not be saved.")
    
def toCSV(data):
    return data.to_csv(index=False).encode()


if st.session_state.pitdata == {}:
    for i in st.session_state.pitq:
        st.session_state.pitdata[i] = []

if st.session_state.matchdata == {}:
    for i in st.session_state.matchq:
        st.session_state.matchdata[i] = []

hometext = {
}

sect = st.sidebar.radio("Navigation:", [":red[**Home**]", "**Add a Data Entry**", "**Reset Inputs**", "**View Data**", "**Data Comparison**", "**Visual Analysis**", "**Edit Items**", "**Edit Data**"])

pitcols = []
for i in st.session_state.pitdata.keys():
    pitcols.append(i)

matchcols = []
for i in st.session_state.matchdata.keys():
    matchcols.append(i)
    

if sect == "Reset Inputs":
    st.subheader("Inputs have been reset successfully.")

elif sect == ":red[**Home**]":
    
    st.title(":blue[Scouting]:red[XTREME]")
    st.subheader("**Use the sidebar on the left to navigate the site.**")
    st.write("---")


else:
    st.title(sect)
    st.write("---")

if sect == "Add a Data Entry":

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
                    uin = st.selectbox(f"**{q}**", st.session_state.pitq[q]["Options"], index=st.session_state.pitq[q]["DefaultIndex"])

                inputs.append(uin)
        
                st.subheader("")

        if st.button("Submit"):
        
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
                    uin = st.selectbox(f"**{q}**", st.session_state.matchq[q]["Options"], index=st.session_state.matchq[q]["DefaultIndex"])

                inputs.append(uin)
        
                st.subheader("")

        if st.button("Submit"):
        
            for x, y in zip(st.session_state.matchdata.keys(), inputs):            
                st.session_state.matchdata[x].append(y)
                
            write = f"""
pitdata = {st.session_state.pitdata}
matchdata = {st.session_state.matchdata}
                """

            with open("scoutingsrc.py", "w") as file:
                file.write(write)

elif sect == "View Data":

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
    
    ex2 = st.sidebar.expander("**DANGER ZONE**")
    resetdata = ex2.button("Reset Data")
    restoredata = ex2.button("Restore Data")
    backupdata = ex2.button("Backup Data")

    if resetdata:

        for i in st.session_state.pitdata:
            st.session_state.pitdata[i] = []

        for i in st.session_state.matchdata:
            st.session_state.matchdata[i] = []

        write = f"""
pitdata = {st.session_state.pitdata}
matchdata = {st.session_state.matchdata}
"""

        with open("scoutingsrc.py", "w") as file:
            file.write(write)
            
    if restoredata:
        import scoutingbackup as backup
        st.session_state.pitdata = backup.pitdata
        st.session_state.matchdata = backup.matchdata

        write = f"""
pitdata = {st.session_state.pitdata}
matchdata = {st.session_state.matchdata}
"""

        with open("scoutingsrc.py", "w") as file:
            file.write(write)

    if backupdata:

        writedata = f"""
pitdata = {st.session_state.pitdata}
matchdata = {st.session_state.matchdata}
    """
        
        print(writedata)

        try:
            with open("scoutingbackup.py", "w") as file:
                file.write(writedata)
            print("Data Saved.")
        
        except:
            print("Data could not be backed up.")

    df = pd.DataFrame().from_dict(data)
    rows = [i for i in range(len(df[selectedcols])) if df["Team No."][i] == team or team == "All"]

    st.dataframe(df[selectedcols].iloc[rows], use_container_width=True, hide_index=True)

    st.write("*Note: Double click on a cell to view all of its contents if it is cut off.*")
    
    st.write("---")

    c1, c2, c3, c4 = st.columns(4)

    c1.write(f"**Teams Scouted:** {len(df['Team No.'].unique())}")
    c2.write(f"**Total Entries:** {len(df)}")
    c3.write(f"**Rounds Scouted:** {len(pd.Series(st.session_state.matchdata['Round No.']).unique())}")
    c4.write(f"**Total Rounds:** {totalrounds}")

    c1, c2 = st.columns(2)
    ex1, ex2 = c1.expander("Download Data"), c2.expander("Import Data")
    
    datatxt = str(df[selectedcols])
    datacsv = toCSV(df[selectedcols])


    ex1.subheader("Download Data")

    filename = ex1.text_input("Data File Name (no extension):", "scoutingdata")
    downloadtxt = ex1.download_button("Download as Text File", datatxt, filename+".txt")
    downloadcsv = ex1.download_button("Download as CSV File", datacsv, filename+".csv")


    ex2.subheader("Import CSV Data")
    ex2.write("**FILE COLUMN NAMES MUST MATCH DATA COLUMN NAMES**")
    
    datafiles = []

    for file in os.listdir():
        if '.csv' in file[-4:]:
            datafiles.append(file)

    userfile = ex2.file_uploader("")
    
    if userfile != None:

        if userfile.name[-4:] != ".csv":
            st.subheader("This is not a valid .csv data file. Please use a different file.")

        else:

            strio = StringIO(userfile.getvalue().decode("utf-8"))

            with open(userfile.name, "w") as file:
                file.write(strio.read())

        dataset = ex2.radio("**Import To:**", ["Pit Data", "Match Data"])
        mode = ex2.radio("**Do you want to add to or replace the existing data?**", ["Add Data", "Replace Data"])
        newdata = pd.read_csv(userfile.name).to_dict()

        for col in newdata:
            
            coldata = []

            for row in newdata[col]:
                coldata.append(str(newdata[col][row]))
            
            newdata[col] = coldata


        if ex2.button("Import Data"):
                
            if mode == "Replace Data":
            
                if dataset == "Pit Data":
                    st.session_state.pitdata = newdata

                if dataset == "Match Data":
                    st.session_state.matchdata = newdata

            if mode == "Add Data":
            
                if dataset == "Pit Data":
                    for col in newdata:
                        st.session_state.pitdata[col] += newdata[col]

                if dataset == "Match Data":
                    for col in newdata:
                        st.session_state.matchdata[col] += newdata[col]

    if downloadtxt:
        c1.write(f"**Successfully downloaded data as {filename}.txt**")

    if downloadcsv:
        c1.write(f"**Successfully downloaded data as {filename}.txt**")

elif sect == "Data Comparison":
    st.header("COMING SOON")

elif sect == "Visual Analysis":

    st.header("COMING SOON")

    '''
    plt.style.use('seaborn-dark-palette')

    opts = st.sidebar.expander("Options")
    stat = opts.selectbox("Select A Data Catagory:", [i for i in cols if i not in ["Match No.", "Team No.", "Extra Notes"]])
    numofteams = opts.number_input("How many teams do you want to show?", 1, 4)
    
    teams = []

    st.title(f"Shown Statistic: *{stat}*")

    c1, c2 = st.columns(2)

    for t in range(numofteams):

        team = opts.selectbox(f"Team {t+1}:", [i for i in pd.Series(data["Team No."]).unique() if i not in teams])
        teams.append(team)

        cats = pd.Series(data[stat]).unique()
        statdata = [data[stat][i] for i in range(len(data[stat])) if data["Team No."][i] == team]
        piedata = [0 for i in cats]
        datainc = []

        for x in range(len(cats)):

            for y in statdata:
                if y == cats[x]:
                    piedata[x] += 1

            if piedata[x] > 0:
                datainc.append(cats[x])

        if t % 2 == 0:

            c1.write("---")

            tc1, tc2, tc3 = c1.columns(3)

            tc2.title(f"{team}")

            fig = plt.figure(figsize=(15, 3), frameon=False, edgecolor="white")

            plt.pie([i for i in piedata if i > 0], labels=[i for i in cats if i in datainc], explode=[0.05 for i in range(len(datainc))], autopct="%.2f")

            c1.pyplot(fig)
            
        else:

            c2.write("---")

            tc1, tc2, tc3 = c2.columns(3)

            tc2.title(f"{team}")

            fig = plt.figure(figsize=(15, 3), frameon=False, edgecolor="white")

            plt.pie([i for i in piedata if i > 0], labels=[i for i in cats if i in datainc], explode=[0.05 for i in range(len(datainc))], autopct="%.2f")

            c2.pyplot(fig)
'''

elif sect == "Edit Items":

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
    qedit = st.sidebar.radio("**What would you like to do?**", ["Add a question", "Remove a question", "Insert a question into a specific position"])

    if qedit == "Remove a question":
        
        st.write("**Note: Removing items will remove ALL DATA associated with that item. Also, DO NOT remove *Round No.* or *Team No.* from the data, as this can cause issues with the rest of the program**")

        if qsect == "Pit":
                
            if len(st.session_state.pitq) == 0:
                st.header("There are no pit questions yet.")

            else:

                itemnum = st.number_input("**Enter the number of the item you'd like to remove:**", 1, len(st.session_state.pitq), step=1)-1
                items = [i for i in st.session_state.pitq]

                if st.sidebar.button("Remove Item"):

                    if items[itemnum] in st.session_state.pitdata:
                        del st.session_state.pitdata[items[itemnum]]

                    if items[itemnum] in st.session_state.pitq:
                        del st.session_state.pitq[items[itemnum]]
                    
                    st.sidebar.subheader("Item Removed Successfully.")

        if qsect == "Match":
            
            itemnum = st.number_input("**Enter the number of the item you'd like to remove:**", 1, len(st.session_state.matchq), step=1)-1
            items = [i for i in st.session_state.matchq]

            if st.sidebar.button("Remove Item"):

                if items[itemnum] in st.session_state.matchdata:
                    del st.session_state.matchdata[items[itemnum]]

                if items[itemnum] in st.session_state.matchq:
                    del st.session_state.matchq[items[itemnum]]
                
                st.sidebar.subheader("Item Removed Successfully.")

    elif qedit == "Insert a question into a specific position":

        st.write("**Note: Inserting a question in a certain position will cause the question in its spot (as well as those after it) to be pushed one position forward (towards the end).**")

        pitqnames = [q for q in st.session_state.pitq]
        matchqnames = [q for q in st.session_state.matchq]

        if qsect == "Pit":
            
            if len(st.session_state.pitq) == 0:
                st.subheader(f"No {qsect} Items Added Yet.")

            qtypes = ["Header", "Selection Box", "Multiple Choice", "Number Input", "Text Input"]
            qtype = c1.selectbox("**What type of element would you like to add?**", qtypes)


            if qtype == "Header":

                qname = c2.text_input("**What should the header say?**")
                pos = st.number_input("What position do you want to insert this at?", step=1, min_value=1, max_value=len(st.session_state.pitq))

                if st.sidebar.button("Add Item"):
                    newq = {"Type": qtype}
                    tempq = {}
                    endq = {}

                    for q in pitqnames[:pos]:
                        tempq[q] = st.session_state.pitq[q]

                    for q in pitqnames[pos:]:
                        endq[q] = st.session_state.pitq[q]

                    tempq[qname] = newq

                    st.session_state.pitq = tempq

                    for q in endq.keys():
                        st.session_state.pitq[q] = endq[q]

            else:

                qname = c2.text_input("**What should this question ask?**")
                    
                additem = st.sidebar.button("Add Item")
                    
                if qtype in "Text Input":

                    if additem:
                        newq = {"Type": qtype, "Character Limit": 200}

                elif qtype in "Number Input":

                    qmin = c1.number_input("**Minimum Value**", step=1)
                    qmax = c2.number_input("**Maximum Value**", step=1)

                    if additem:
                        newq = {"Type": qtype, "Minimum": qmin, "Maximum": qmax}

                else:

                    qoptsnum = c1.number_input("**How many options should this question have?**", 2, step=1)
                    qdefindex = c2.number_input("**Enter the number of the option that this question should default to:**", min_value=1, max_value=qoptsnum, step=1)-1

                    qopts = []

                    if qoptsnum > 0:
                        for q in range(qoptsnum):
                            qopts.append(st.text_input(f"Option {q+1}:"))
                
                    newq = {"Type": qtype, "Options": qopts, "DefaultIndex": qdefindex}

                pos = st.number_input("What position do you want to insert this at?", step=1, min_value=1, max_value=len(st.session_state.pitq))-1


                if additem:

                    newcol = ["N/A" for i in range(len(st.session_state.pitdata['Team No.']))]
                    tempdata = {}
                    enddata = {}

                    for q in pitcols[:pos]:
                        tempdata[q] = st.session_state.pitdata[q]

                    for q in pitcols[pos:]:
                        enddata[q] = st.session_state.pitdata[q]

                    tempdata[qname] = newcol

                    st.session_state.pitdata = tempdata


                    for q in enddata.keys():
                        st.session_state.pitdata[q] = enddata[q]

                    tempq = {}
                    endq = {}

                    for q in pitqnames[:pos]:
                        tempq[q] = st.session_state.pitq[q]

                    for q in pitqnames[pos:]:
                        endq[q] = st.session_state.pitq[q]

                    tempq[qname] = newq

                    st.session_state.pitq = tempq

                    for q in endq.keys():
                        st.session_state.pitq[q] = endq[q]

        if qsect == "Match":
            
            if len(st.session_state.matchq) == 0:
                st.subheader(f"No {qsect} Items Added Yet.")

            qtypes = ["Header", "Selection Box", "Multiple Choice", "Number Input", "Text Input"]
            qtype = c1.selectbox("**What type of element would you like to add?**", qtypes)


            if qtype == "Header":

                qname = c2.text_input("**What should the header say?**")
                pos = st.number_input("What position do you want to insert this at?", step=1, min_value=1, max_value=len(st.session_state.matchq))

                if st.sidebar.button("Add Item"):
                    newq = {"Type": qtype}
                    tempq = {}
                    endq = {}

                    for q in matchqnames[:pos]:
                        tempq[q] = st.session_state.matchq[q]

                    for q in matchqnames[pos:]:
                        endq[q] = st.session_state.matchq[q]

                    tempq[qname] = newq

                    st.session_state.matchq = tempq

                    for q in endq.keys():
                        st.session_state.matchq[q] = endq[q]

            else:

                qname = c2.text_input("**What should this question ask?**")
                    
                additem = st.sidebar.button("Add Item")
                    
                if qtype in "Text Input":

                    if additem:
                        newq = {"Type": qtype, "Character Limit": 200}

                elif qtype in "Number Input":

                    qmin = c1.number_input("**Minimum Value**", step=1)
                    qmax = c2.number_input("**Maximum Value**", step=1)

                    if additem:
                        newq = {"Type": qtype, "Minimum": qmin, "Maximum": qmax}

                else:

                    qoptsnum = c1.number_input("**How many options should this question have?**", 2, step=1)
                    qdefindex = c2.number_input("**Enter the number of the option that this question should default to:**", min_value=1, max_value=qoptsnum, step=1)-1

                    qopts = []

                    if qoptsnum > 0:
                        for q in range(qoptsnum):
                            qopts.append(st.text_input(f"Option {q+1}:"))
                
                    newq = {"Type": qtype, "Options": qopts, "DefaultIndex": qdefindex}

                pos = st.number_input("What position do you want to insert this at?", step=1, min_value=1, max_value=len(st.session_state.matchq))-1


                if additem:

                    newcol = ["N/A" for i in range(len(st.session_state.matchdata['Team No.']))]
                    tempdata = {}
                    enddata = {}

                    for q in matchcols[:pos]:
                        tempdata[q] = st.session_state.matchdata[q]

                    for q in matchcols[pos:]:
                        enddata[q] = st.session_state.matchdata[q]

                    tempdata[qname] = newcol

                    st.session_state.matchdata = tempdata


                    for q in enddata.keys():
                        st.session_state.matchdata[q] = enddata[q]

                    tempq = {}
                    endq = {}

                    for q in matchqnames[:pos]:
                        tempq[q] = st.session_state.matchq[q]

                    for q in matchqnames[pos:]:
                        endq[q] = st.session_state.matchq[q]

                    tempq[qname] = newq

                    st.session_state.matchq = tempq

                    for q in endq.keys():
                        st.session_state.matchq[q] = endq[q]

    else:

        if qsect == "Pit":
            
            if len(st.session_state.pitq) == 0:
                st.subheader(f"No {qsect} Items Added Yet.")

            qtypes = ["Header", "Selection Box", "Multiple Choice", "Number Input", "Text Input"]
            qtype = c1.selectbox("**What type of element would you like to add?**", qtypes)
            
            if qtype == "Header":

                qname = c2.text_input("**What should the header say?**")

                if st.sidebar.button("Add Item"):
                    st.session_state.pitq[qname] = {"Type": qtype}

            else:

                qname = c2.text_input("**What should this question ask?**")
                    
                additem = st.sidebar.button("Add Item")
                    
                if qtype in "Text Input":
                    if additem:
                        st.session_state.pitq[qname] = {"Type": qtype, "Character Limit": 200}
                        newcol = []
                        st.session_state.pitdata[qname] = newcol

                elif qtype in "Number Input":

                    qmin = c1.number_input("**Minimum Value**", step=1)
                    qmax = c2.number_input("**Maximum Value**", step=1)

                    if additem:
                        st.session_state.pitq[qname] = {"Type": qtype, "Minimum": qmin, "Maximum": qmax}
                        newcol = ["N/A" for i in range(len(st.session_state.pitdata['Team No.']))]
                        st.session_state.pitdata[qname] = newcol

                else:

                    qoptsnum = c1.number_input("**How many options should this question have?**", 2, step=1)
                    qdefindex = c2.number_input("**Enter the number of the option that this question should default to:**", min_value=1, max_value=qoptsnum, step=1)-1

                    qopts = []

                    if qoptsnum > 0:
                        for q in range(qoptsnum):
                            qopts.append(st.text_input(f"Option {q+1}:"))
                
                    st.session_state.pitq[qname] = {"Type": qtype, "Options": qopts, "DefaultIndex": qdefindex}

                if additem:
                    newcol = ["N/A" for i in range(len(st.session_state.pitdata['Team No.']))]
                    st.session_state.pitdata[qname] = newcol

        if qsect == "Match":

            if len(st.session_state.matchq) == 0:
                st.subheader(f"No {qsect} Items Added Yet.")

            qtypes = ["Header", "Selection Box", "Multiple Choice", "Number Input", "Text Input"]
            qtype = c1.selectbox("**What type of element would you like to add?**", qtypes)
            
            if qtype == "Header":

                qname = c2.text_input("**What should the header say?**")

                if st.sidebar.button("Add Item"):
                    st.session_state.matchq[qname] = {"Type": qtype}

            else:

                qname = c2.text_input("**What should this question ask?**")
                    
                additem = st.sidebar.button("Add Item")
                    
                if qtype in "Text Input":
                    if additem:
                        st.session_state.matchq[qname] = {"Type": qtype, "Character Limit": 200}
                        newcol = []
                        st.session_state.matchdata[qname] = newcol

                elif qtype in "Number Input":

                    qmin = c1.number_input("**Minimum Value**", step=1)
                    qmax = c2.number_input("**Maximum Value**", step=1)

                    if additem:
                        st.session_state.matchq[qname] = {"Type": qtype, "Minimum": qmin, "Maximum": qmax}
                        newcol = ["N/A" for i in range(len(st.session_state.matchdata['Team No.']))]
                        st.session_state.matchdata[qname] = newcol

                else:

                    qoptsnum = c1.number_input("**How many options should this question have?**", 2, step=1)
                    qdefindex = c2.number_input("**Enter the number of the option that this question should default to:**", min_value=1, max_value=qoptsnum, step=1)-1

                    qopts = []

                    if qoptsnum > 0:
                        for q in range(qoptsnum):
                            qopts.append(st.text_input(f"Option {q+1}:"))
                
                    st.session_state.matchq[qname] = {"Type": qtype, "Options": qopts, "DefaultIndex": qdefindex}

                if additem:
                    newcol = ["N/A" for i in range(len(st.session_state.matchdata['Team No.']))]
                    st.session_state.matchdata[qname] = newcol

elif sect == "Edit Data":
    
    showdata = st.sidebar.checkbox("Show Data", value=True)
    dataselect = st.sidebar.radio("Which dataset would you like to edit?", ["Pit Data", "Match Data"])

    if dataselect == "Pit Data":
        data = st.session_state.pitdata
    if dataselect == "Match Data":
        data = st.session_state.matchdata

    if len(data) == 0:
        st.header("This dataset is empty right now.")

    else:

        if showdata:
            st.header(dataselect)
            st.dataframe(data, use_container_width=True, hide_index=False)
            st.write("---")
            editmode = st.sidebar.radio("Edit Mode:", ["Replace", "Remove"])

        if editmode == "Remove":

            removeselect = st.radio("Would you like to remove a row or a specific data entry?", ["Row", "Data Entry"])

            if removeselect == "Row":

                index = st.number_input("What row would you like to remove?", min_value=0, max_value=len(data))
                
                if st.button("Remove Data"):
                    
                    for col in data:
                        data[col].pop(index)

gitsave = st.sidebar.expander("**Save to GitHub Repository...**")
savemsg = gitsave.text_input("**Commit Message:**", "Update GitHub", max_chars=100)

if gitsave.button("Save"):
    savedata()
    gitupdate(savemsg)

if st.sidebar.button("Clear System Log"):
    os.system("cls")
    print("""\033[1m
-------------------
Scouting XTREME Log
-------------------
    \033[0m""")
