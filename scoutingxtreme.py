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
import numpy as np

# Total rounds for the game
totalrounds = 0

# Modules that need to be installed
requiredmodules = [
    "pandas",
    "matplotlib",
    "seaborn",
    "minio"
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

import cloudSave

st.set_page_config("Scouting XTREME", layout="wide", page_icon="icon.png", initial_sidebar_state="expanded")
pd.set_option("display.max_rows", None, "display.max_columns", None)

sidebar = st.sidebar
theme = """
[theme]
base="dark"
primaryColor="#ff3636"
backgroundColor="#0e0e0e"
secondaryBackgroundColor="#1e2029"
"""

if ["pitq", "matchq", "pitdata", "matchdata", "admin"] not in st.session_state:
    
    import scoutingsrc as src
    import questions

    st.session_state.pitq = questions.pitq
    st.session_state.matchq = questions.matchq

    st.session_state.pitdata = src.pitdata
    st.session_state.matchdata = src.matchdata

    st.session_state.robotphotos = {}
    
    st.session_state.admin = False

def gitpull(repo: str = None):
    
    if repo:
        os.system(f"git pull {repo}")
    else:
        os.system("git pull")

def gitpush(savemsg: str ="Update GitHub"):
    os.system("git add .")
    os.system(f"git commit -m \"{savemsg}\"")
    os.system("git push")
    os.system("git pull")

def savequestions(pitq=st.session_state.pitq, matchq=st.session_state.matchq):
    
    writequestions = f"""
pitq = {pitq}
matchq = {matchq}
"""
    
    print(writequestions)

    try:
        with open("questions.py", "w") as file:
            file.write(writequestions)
        print("Questions Saved.")
    
    except:
        print("Questions could not be saved.")

def savedata(pitdata=None, matchdata=None):

    writedata = f"""
pitdata = {pitdata if pitdata is not None else st.session_state.pitdata}
matchdata = {matchdata if matchdata is not None else st.session_state.matchdata}
"""
    
    print(writedata)


    try:
        with open("scoutingsrc.py", "w") as file:
            file.write(writedata)
        print("Data Saved.")
    
    except:
        print("Data could not be saved.")

def isNum(string: str):

    try:
        test = float(string)
        return True
    except:
        return False            

@st.cache_data()
def toCSV(data):
    return data.to_csv(index=False).encode()


if st.session_state.pitdata == {}:
    for i in st.session_state.pitq:
        st.session_state.pitdata[i] = []

if st.session_state.matchdata == {}:
    for i in st.session_state.matchq:
        st.session_state.matchdata[i] = []

access = sidebar.expander("**:red[Login as Admin...]**")
accesslvl = access.radio("**Access Level:**", ["User", "Admin"])

pages = {
    "user": [":blue[**Home**]", "**Add a Data Entry**", "**View Data**"],
    "admin": [":blue[**Home**]", "**Add a Data Entry**", "**View Data**", "**Data Comparison**", "**Edit Items (:red[USE OFFLINE ONLY])**", "**Edit Data**"],
    "full": [":blue[**Home**]", "**Add a Data Entry**", "**Robot Photos**", "**View Data**", "**Data Comparison**", "**Visual Analysis**", "**Edit Items (:red[USE OFFLINE ONLY])**", "**Edit Data**"]
}

if accesslvl == "Admin":

    password = access.text_input("**Enter Admin Password:**", placeholder="Enter Password")

    if password == st.secrets.adminpassword:
        st.session_state.admin = True

if st.session_state.admin:
    sect = sidebar.radio("Navigation:", pages['full'])
else:
    sect = sidebar.radio("Navigation:", pages['user'])

pitcols = []
for i in st.session_state.pitdata.keys():
    pitcols.append(i)

matchcols = []
for i in st.session_state.matchdata.keys():
    matchcols.append(i)
    
if sidebar.button("Refresh Page"):
    pass

if sect == ":blue[**Home**]":
    
    st.title(":blue[Scouting]:red[XTREME]")
    st.subheader("**Use the sidebar on the left to navigate the site.**")
    st.write("---")    

else:
    st.title(sect)
    st.write("---")

if sect == "**Add a Data Entry**":

    datasect = st.radio("Which data would you like to add to?", ["Pit Data", "Match Data"])
    inputs = []

    resetinputs = st.checkbox("Reset All Inputs")

    if resetinputs:
        st.subheader("Inputs reset successfully. Uncheck the \"Reset All Inputs\" box to continue.")

    else:

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

                    elif st.session_state.pitq[q]["Type"] == "Checkbox":
                        uin = st.checkbox(f"**{q}**", str(st.session_state.pitq[q]["DefaultIndex"]))

                    inputs.append(uin)
            
                    st.subheader("")

            if st.button("Submit"):

                try:

                    for x, y in zip(st.session_state.pitdata.keys(), inputs):
                        st.session_state.pitdata[x].append(y)
                        
                    try:
                        st.write("**Submission Saved Successfully.**")
                        time.sleep(2)
                        savedata()
                    except:
                        savedata()            

                except:
                    st.write("**Could not save your submission. Please try again.**")

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

                        elif st.session_state.matchq[q]["Type"] == "Checkbox":
                            uin = str(st.checkbox(f"**{q}**", st.session_state.matchq[q]["DefaultIndex"]))

                        inputs.append(uin)
                
                        st.subheader("")

            if not resetinputs:

                if st.button("Submit"):
                
                    for x, y in zip(st.session_state.matchdata.keys(), inputs):            
                        st.session_state.matchdata[x].append(y)

                    try:
                        st.write("**Submission Saved Successfully.**")
                        time.sleep(2)
                        savedata()
                    except:
                        savedata()            

elif sect == "**Robot Photos**":
    
    viewmode = st.radio("Do you want to add or view robot photos?", ["Add", "View"])

    if viewmode == "Add":

        teamno = st.number_input("**Team Number:**", 1, 10000)
        image = st.file_uploader("**Upload the robot photo here:**")

        if st.button("Save Image"):

            st.session_state.robotphotos[teamno] = image
            st.write(image)
            st.write("**Image Saved Successfully.**")

    elif len(st.session_state.robotphotos) == 0:
        st.subheader("Please upload a photo before viewing them.")

    else:
        
        teamno = st.selectbox("**Select a Team:**", st.session_state.robotphotos.keys())
        st.image(st.session_state.robotphotos[teamno], teamno)

elif sect == "**View Data**":

    viewdata = sidebar.radio("Which data would you like to view?", ["Pit Data", "Match Data"])

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
    ex1 = sidebar.expander("Selected Columns:")

    st.write("---")

    selectedcols = []

    selectall = ex1.checkbox("Select All", value=True)


    if type(data["Team No."]) == str:
        teamnums = [data["Team No."]]
    else:
        teamnums = data["Team No."]

    df = pd.DataFrame()
    cols = []

    for col in data:

        if viewdata == "Pit Data":

            try:
                cols.append(st.session_state.pitq[col]["Display Name"])

            except:
                cols.append(col)

        else:

            try:
                cols.append(st.session_state.matchq[col]["Display Name"])

            except:
                cols.append(col)

    for key, col in zip(data.keys(), cols):
        df[col] = data[key]
        
    for i in df.columns:

        if i == "Round No." or i == "Team No.":
            checkbox = True
        else:
            checkbox = ex1.checkbox(i, value=selectall)

        if checkbox:
            selectedcols.append(i)

    if viewdata == "Match Data":

        if ex1.checkbox("Points Scored (Excluding Penalties)", selectall):
            selectedcols.append("Points Scored (Excluding Penalties)")

    numcols = []

    for col in df.columns:

        for i in range(len(df[col])):
                
            if col != "Team No.":

                try:
                    df[col][i] = float(df[col][i])
                    numcols.append(col)
                    break
                except:
                    pass

    for col in numcols:

        for i in range(len(df[col])):

            try:
                df[col][i] = float(df[col][i])
            
            except:
                
                try:
                    df[col][i] = float(df[col][i].split()[0])
                except:
                    df[col][i] = 0

    if viewdata == "Match Data": 

        df["Points Scored (Excluding Penalties)"] = ["N/A" for i in range(len(df))]

        for i in range(len(df)):

            df["Points Scored (Excluding Penalties)"][i] = 0

            for q in st.session_state.matchq:

                if st.session_state.matchq[q]["Type"] == "Number Input":

                    df["Points Scored (Excluding Penalties)"][i] += float(df[q][i])*st.session_state.matchq[q]["Point Value"]

            rows = [i for i in range(len(df[selectedcols])) if df["Team No."][i] == team or team == "All"]

    ex2 = sidebar.expander("Sort By...")

    sortcols = []

    enablesort = ex2.checkbox("Sort Items")
    order = ex2.selectbox("**Order:**", ["Ascending", "Descending"])
    numsortcols = ex2.slider("**Number of Columns to Sort By (Most to Least Priority):**", 1, 5)

    for i in range(numsortcols):
        sortcols.append(ex2.selectbox(f"**Sort {i+1}:**", [i for i in selectedcols if i != "Round No." and i not in sortcols]))

    if order == "Ascending":
        ascending = True
    else:
        ascending = False

    df = df[selectedcols]
    
    if enablesort:
        df = df.sort_values(by=sortcols, ascending=ascending, na_position="last")

    st.dataframe(df, use_container_width=True, hide_index=True)

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

        try:
            del newdata["Unnamed: 0"]
        except:
            pass

        for col in newdata:
            
            coldata = []

            for row in newdata[col]:
                coldata.append(str(newdata[col][row]))
            
            newdata[col] = coldata


        if ex2.button("Import Data"):
                
            if mode == "Replace Data":
            
                if dataset == "Pit Data":
                    
                    for i in st.session_state.pitdata:
                        st.session_state.pitdata[i] = []
                        
                    for col in newdata:
                        st.session_state.pitdata[col] += newdata[col]

                    savedata()

                if dataset == "Match Data":
                    
                    for i in st.session_state.matchdata:
                        st.session_state.matchdata[i] = []

                    for col in newdata:
                        st.session_state.matchdata[col] += newdata[col]

                    savedata()


            if mode == "Add Data":
            
                if dataset == "Pit Data":
                    for col in newdata:
                        st.session_state.pitdata[col] += newdata[col]

                if dataset == "Match Data":
                    for col in newdata:
                        st.session_state.matchdata[col] += newdata[col]

            savedata()

    if downloadtxt:
        c1.write(f"**Successfully downloaded data as {filename}.txt**")

    if downloadcsv:
        c1.write(f"**Successfully downloaded data as {filename}.txt**")

elif sect == "**Data Comparison**":
        
    viewdata = sidebar.radio("**Which data would you like to analyze?**", ["Pit Data", "Match Data"])
    compmode = sidebar.radio("**Comparison Mode:**", ["Statistics", "Table of Averages"])
    criteria = sidebar.expander("**Data Selection**")

    if viewdata == "Pit Data":
        cols = [col for col in st.session_state.pitdata.keys()]
    
    else:
        cols = [col for col in st.session_state.matchdata.keys()]

    if ( viewdata == "Pit Data" and len(st.session_state.pitdata[cols[1]]) == 0 ) or ( viewdata == "Match Data" and len(st.session_state.matchdata[cols[1]]) == 0 ):

        st.subheader("Please add data to this data set before trying to compare data (cannot compare data in an empty dataset).")

    else:

        if compmode == "Statistics":

            selectedcols = []

            criteria.write("**What data do you want to see?**")

            with st.expander(f"**{viewdata}**"):

                st.header(viewdata)

                if viewdata == "Pit Data":
                    data = st.session_state.pitdata
                    dataq = st.session_state.pitq
                if viewdata == "Match Data":
                    data = st.session_state.matchdata
                    dataq = st.session_state.matchq

                for col in data:
                    if "Text Input" != dataq[col]["Type"] and criteria.checkbox(col, True):
                        selectedcols.append(col)

                df = pd.DataFrame().from_dict(data)

                st.dataframe(df[selectedcols], use_container_width=True, hide_index=True)
            
            compareval = criteria.radio("**What data do you want to compare by?**", [col for col in df.columns if "Text Input" != dataq[col]["Type"]])
            viewmode = criteria.radio("**Viewing Mode:**", ["Occurrences", "Percentages"])
            showavg = criteria.checkbox("Show Averages For Numerical Values", True)

            st.subheader(f"Comparison By `{compareval}` (`data: occurences/percentage`)")

            c1, c2 = st.columns(2)

            val1 = c1.selectbox(f"Value 1", df[compareval].unique())

            for col in [col for col in selectedcols if col not in (compareval, "Team No.", "Round No.")]:

                write = f"`{col}`: `"
                
                if dataq[col]["Type"] == "Number Input" and showavg:

                    val1lst = [float(data[col][i]) for i in range(len(data[col])) if data[compareval][i] == val1]
                    avg = sum(val1lst)/len(val1lst)
                    write += f"{avg} AVG."

                    c1.write(write+"`")

                else:

                    items = {}

                    for val in df[col].unique():
                        items[val] = 0

                    for item in range(len(data[col])):

                        if data[compareval][item] == val1:
                            items[data[col][item]] += 1
                            
                    totalvals = 0

                    for val in items.values():
                        totalvals += val

                    for item, val in zip(items, items.values()):
                        if viewmode == "Percentages":
                            write += f"{item}: {round(val/totalvals*100, 2)}%, "
                        else:
                            write += f"{item}: {val}, "

                    c1.write(write[:-2]+"`")


            val2 = c2.selectbox(f"Value 2", df[compareval].unique())

            for col in [col for col in selectedcols if col not in (compareval, "Team No.", "Round No.")]:

                write = f"`{col}`: `"
                
                if dataq[col]["Type"] == "Number Input" and showavg:

                    val2lst = [float(data[col][i]) for i in range(len(data[col])) if data[compareval][i] == val2]
                    avg = sum(val2lst)/len(val2lst)
                    write += f"{avg} AVG."

                    c2.write(write+"`")

                else:

                    items = {}

                    for val in df[col].unique():
                        items[val] = 0

                    for item in range(len(data[col])):

                        if data[compareval][item] == val2:
                            items[data[col][item]] += 1
                            
                    totalvals = 0

                    for val in items.values():
                        totalvals += val

                    for item, val in zip(items, items.values()):
                        if viewmode == "Percentages":
                            write += f"{item}: {round(val/totalvals*100, 2)}%, "
                        else:
                            write += f"{item}: {val}, "

                    c2.write(write[:-2]+"`")

        else:

            data = {}

            if viewdata == "Pit Data":

                for col in st.session_state.pitdata:

                    if isNum(str(st.session_state.pitdata[col][0])):
                        data[col] = st.session_state.pitdata[col]
                    
                    elif isNum(str(st.session_state.pitdata[col][0].split(" ")[0])):
                        data[col] = st.session_state.pitdata[col]

            if viewdata == "Match Data":

                for col in st.session_state.matchdata:
                    
                    if isNum(str(st.session_state.matchdata[col][0])) and col not in ["Round No."]:
                        data[col] = st.session_state.matchdata[col]
                    
                    elif isNum(str(st.session_state.matchdata[col][0].split(" ")[0])) and col not in ["Round No."]:
                        data[col] = st.session_state.matchdata[col]

            selectedcols = []
            selectall = criteria.checkbox("Select All", True)

            for col in data:
                if criteria.checkbox(col, selectall):
                    selectedcols.append(col)

            df = pd.DataFrame()
            compdata = {}

            for col in selectedcols:
                compdata[col] = []

            compdata["Team No."] = pd.Series(data["Team No."]).unique()

            for team in compdata["Team No."]:
            
                for col in [c for c in selectedcols if c != "Team No."]:

                    numlist = []
                    
                    for row in range(len(data[col])):

                        if data["Team No."][row] == team:
                            numlist.append(float(data[col][row]))

                    avg = np.mean(numlist)
                    compdata[col].append(avg)

            for col in compdata:
                df[col] = compdata[col]

            st.dataframe(df, use_container_width=True, hide_index=True)           

elif sect == "**Visual Analysis**":

    plt.style.use('seaborn-dark-palette')

    opts = sidebar.expander("Options")
    shownull = opts.checkbox("Show percentage of missing data", True)
    choosedata = opts.radio("What data set do you want to view?", ["Pit Data", "Match Data"])
    
    if choosedata == "Match Data":
        data = st.session_state.pitdata

    else:
        data = st.session_state.matchdata
    
    cols = data.keys()
    stat = opts.selectbox("Select A Data Catagory:", [i for i in cols if i not in ["Match No.", "Team No.", "Extra Notes"]])
    numofteams = opts.number_input("How many teams do you want to show?", 1, 4)
    
    teams = []

    if shownull:
        nullvals = []
    else:
        nullvals = ["N/A", "nan"]

    st.title(f"Shown Statistic: *{stat}*")
    st.write("---")
    
    c1, c2 = st.columns(2)

    for t in range(numofteams):

        team = opts.selectbox(f"Team {t+1}:", [i for i in pd.Series(data["Team No."]).unique() if i not in teams])
        teams.append(team)

        cats = [cat for cat in pd.Series(data[stat]).unique() if cat not in nullvals]
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

            tc1, tc2, tc3 = c1.columns(3)

            tc2.title(f"{team}")

            fig, ax = plt.subplots(figsize=(15, 3), frameon=False, edgecolor="white")

            patches, texts, pcts = ax.pie([i for i in piedata if i > 0], labels=[i for i in cats if i in datainc], explode=[0.0025 for i in range(len(datainc))], autopct="%.2f", colors=sn.color_palette("dark"), wedgeprops={"linewidth": 2.5, "edgecolor": "white"})

            for i, patch in enumerate(patches):
                texts[i].set_color(patch.get_facecolor())

            plt.setp(pcts, color="white", fontweight="bold")
            plt.setp(texts, fontweight=600, fontsize=15)

            c1.pyplot(fig)
            
        else:

            tc1, tc2, tc3 = c2.columns(3)

            tc2.title(f"{team}")

            fig, ax = plt.subplots(figsize=(15, 3), frameon=False, edgecolor="white")

            patches, texts, pcts = ax.pie([i for i in piedata if i > 0], labels=[i for i in cats if i in datainc], explode=[0.0025 for i in range(len(datainc))], autopct="%.2f", colors=sn.color_palette("dark"), wedgeprops={"linewidth": 2.5, "edgecolor": "white"})

            for i, patch in enumerate(patches):
                texts[i].set_color(patch.get_facecolor())

            plt.setp(pcts, color="white", fontweight="bold")
            plt.setp(texts, fontweight=600)

            c2.pyplot(fig)

elif sect == "**Edit Items (:red[USE OFFLINE ONLY])**":

    qtypes = ["Header", "Selection Box", "Multiple Choice", "Number Input", "Text Input", "Checkbox"]

    qsect = sidebar.radio("**Which set of questions would you like to edit?**", ["Pit", "Match"])
    qedit = sidebar.radio("**What would you like to do?**", ["Add a question", "Remove a question", "Insert a question into a specific position"])
    c1, c2 = st.columns(2)

    if qedit == "Remove a question":
        
        if qsect == "Pit":
        
            st.write("**Note: Removing items will remove ALL DATA associated with that item. The first 2 items cannot be removed, as they are necessary for the software to function, and are universal questions.**")
                
            if len(st.session_state.pitq) == 0:
                st.header("There are no pit questions yet.")

            else:

                try:

                    itemnum = st.number_input("**Enter the number of the item you'd like to remove:**", 3, len(st.session_state.pitq), step=1)-1
                
                    items = [i for i in st.session_state.pitq]

                    if sidebar.button("Remove Item"):

                        if items[itemnum] in st.session_state.pitdata:
                            del st.session_state.pitdata[items[itemnum]]

                        if items[itemnum] in st.session_state.pitq:
                            del st.session_state.pitq[items[itemnum]]

                        savedata()
                        savequestions()
                        
                        sidebar.subheader("Item Removed Successfully.")

                except:
                    st.write(f"**There are no existing items that can be removed in the {qsect} Data.**")

        if qsect == "Match":

            st.write("**Note: Removing items will remove ALL DATA associated with that item. The first 3 items cannot be removed, as they are necessary for the software to function, and are universal questions.**")
            
            try:

                itemnum = st.number_input("**Enter the number of the item you'd like to remove:**", 4, len(st.session_state.matchq), step=1)-1
                items = [i for i in st.session_state.matchq]

                if sidebar.button("Remove Item"):

                    if items[itemnum] in st.session_state.matchdata:
                        del st.session_state.matchdata[items[itemnum]]

                    if items[itemnum] in st.session_state.matchq:
                        del st.session_state.matchq[items[itemnum]]
                    
                    savedata()
                    savequestions()
                    
                    sidebar.subheader("Item Removed Successfully.")

            except:
                st.write(f"**There are no existing items that can be removed in the {qsect} Data.**")

    elif qedit == "Insert a question into a specific position":
        
        st.subheader(":red[NOT FUNCTIONAL YET]")
        st.write("**Note: Inserting a question in a certain position will cause the question in its spot (as well as those after it) to be pushed one position forward (towards the end).**")

        if qsect == "Pit":

            if len(st.session_state.pitq) > 2:

                qtype = sidebar.selectbox("**What type of element would you like to add?**", qtypes)
                pos = sidebar.number_input("What position do you want to insert this at?", step=1, min_value=3, max_value=len(st.session_state.pitq))-1
                
                if len(st.session_state.pitq) == 0:
                    st.subheader(f"No {qsect} Items Added Yet.")

                c3, c4 = st.columns(2)

                if qtype == "Header":

                    qname = c1.text_input("**What should the header say?**")

                    if sidebar.button("Insert Item"):

                        st.session_state.pitq = list(st.session_state.pitq.items())
                        st.session_state.pitq.insert(pos, (qname, {"Type": "Header"}))
                        st.session_state.pitq = dict(st.session_state.pitq)

                        savedata()
                        savequestions()

                elif qtype == "Checkbox":

                    qname = c1.text_input("**What should the checkbox say?**")
                    defaultval = c2.radio("**Default Value:**", ["Unchecked", "Checked"])

                    if sidebar.button("Insert Item"):

                        if defaultval == "Checked":
                            defaultindex = True

                        else:
                            defaultindex = False

                        st.session_state.pitq = list(st.session_state.pitq.items())
                        st.session_state.pitq.insert(pos, (qname, {"Type": "Checkbox", "DefaultIndex": defaultindex}))
                        st.session_state.pitq = dict(st.session_state.pitq)

                        savedata()
                        savequestions()

                else:

                    qname = c1.text_input("**What should this question ask?**")
                    displayname = c2.text_input("**Data Column Display Name (:red[DO NOT USE EXISTING DISPLAY NAMES])**:", qname, max_chars=100)
                                                
                    if qtype in "Text Input":

                        if sidebar.button("Insert Item"):

                            st.session_state.pitq = list(st.session_state.pitq.items())
                            st.session_state.pitq.insert(pos, (qname, {"Type": qtype, "Character Limit": 200, "Display Name": displayname}))
                            st.session_state.pitq = dict(st.session_state.pitq)

                            st.session_state.pitdata = list(st.session_state.pitq.items())
                            st.session_state.pitdata.insert(pos, (qname, ["N/A" for i in range(len(st.session_state.pitdata))]))
                            st.session_state.pitdata = dict(st.session_state.pitdata)

                            savedata()
                            savequestions()


                    elif qtype in "Number Input":

                        qmin = c1.number_input("**Minimum Value**", step=1)
                        qmax = c2.number_input("**Maximum Value**", step=1)

                        if sidebar.button("Insert Item"):

                            st.session_state.pitq = list(st.session_state.pitq.items())
                            st.session_state.pitq.insert(pos, (qname, {"Type": qtype, "Minimum": qmin, "Maximum": qmax, "Display Name": displayname}))
                            st.session_state.pitq = dict(st.session_state.pitq)

                            st.session_state.pitdata = list(st.session_state.pitq.items())
                            st.session_state.pitdata.insert(pos, (qname, ["N/A" for i in range(len(st.session_state.pitdata))]))
                            st.session_state.pitdata = dict(st.session_state.pitdata)

                            savedata()
                            savequestions()

                    else:

                        qoptsnum = c1.number_input("**How many options should this question have?**", min_value=2, step=1)
                        qdefindex = c2.number_input("**Enter the number of the option that this question should default to:**", min_value=1, max_value=qoptsnum, step=1)-1

                        qopts = []

                        if qoptsnum > 0:
                            for q in range(qoptsnum):
                                qopts.append(st.text_input(f"Option {q+1}:"))
                    
                        if sidebar.button("Insert Item"):

                            st.session_state.pitq = list(st.session_state.pitq.items())
                            st.session_state.pitq.insert(pos, (qname, {"Type": qtype, "Options": qopts, "DefaultIndex": qdefindex, "Display Name": displayname}))
                            st.session_state.pitq = dict(st.session_state.pitq)

                            st.session_state.pitdata = list(st.session_state.pitq.items())
                            st.session_state.pitdata.insert(pos, (qname, ["N/A" for i in range(len(st.session_state.pitdata))]))
                            st.session_state.pitdata = dict(st.session_state.pitdata)

                            savedata()
                            savequestions()

            else:
                st.write("**You need to add a question before you can insert questions.**")

        if qsect == "Match":
            
            if len(st.session_state.matchq) > 3:

                qtype = sidebar.selectbox("**What type of element would you like to add?**", qtypes)
                pos = sidebar.number_input("What position do you want to insert this at?", step=1, min_value=4, max_value=len(st.session_state.matchq))-1
                
                if len(st.session_state.matchq) == 0:
                    st.subheader(f"No {qsect} Items Added Yet.")

                c3, c4 = st.columns(2)


                if qtype == "Header":

                    qname = st.text_input("**What should the header say?**")

                    if sidebar.button("Insert Item"):

                        st.session_state.matchq = list(st.session_state.matchq.items())
                        st.session_state.matchq.insert(pos, (qname, {"Type": "Header"}))
                        st.session_state.matchq = dict(st.session_state.matchq)

                        savedata()
                        savequestions()

                elif qtype == "Checkbox":

                    qname = c1.text_input("**What should the checkbox say?**")
                    defaultval = c2.radio("**Default Value:**", ["Unchecked", "Checked"])

                    if sidebar.button("Insert Item"):

                        if defaultval == "Checked":
                            defaultindex = True

                        else:
                            defaultindex = False

                        st.session_state.matchq = list(st.session_state.matchq.items())
                        st.session_state.matchq.insert(pos, (qname, {"Type": "Checkbox", "DefaultIndex": defaultindex}))
                        st.session_state.matchq = dict(st.session_state.matchq)

                        savedata()
                        savequestions()

                else:

                    qname = c1.text_input("**What should this question ask?**")
                    displayname = c2.text_input("**Data Column Display Name (:red[DO NOT USE EXISTING DISPLAY NAMES])**:", qname, max_chars=100)
                                                
                    if qtype in "Text Input":

                        if sidebar.button("Insert Item"):

                            st.session_state.matchq = list(st.session_state.matchq.items())
                            st.session_state.matchq.insert(pos, (qname, {"Type": qtype, "Character Limit": 200, "Display Name": displayname}))
                            st.session_state.matchq = dict(st.session_state.matchq)

                            st.session_state.matchdata = list(st.session_state.pitq.items())
                            st.session_state.matchdata.insert(pos, (qname, ["N/A" for i in range(len(st.session_state.matchdata))]))
                            st.session_state.matchdata = dict(st.session_state.matchdata)

                            savedata()
                            savequestions()


                    elif qtype in "Number Input":

                        qmin = c1.number_input("**Minimum Value**", step=1)
                        qmax = c2.number_input("**Maximum Value**", step=1)
                        ptval = c1.number_input("**Point Value (per objective scored - enter `0` if this is not a point-based question)**", step=1)
                        maxpts = c2.number_input("**Maximum Scorable Points (enter `0` for no limit)**", step=1)

                        if sidebar.button("Insert Item"):

                            st.session_state.matchq = list(st.session_state.matchq.items())
                            st.session_state.matchq.insert(pos, (qname, {"Type": qtype, "Minimum": qmin, "Maximum": qmax, "Point Value": ptval, "Maximum Points": maxpts, "Display Name": displayname}))
                            st.session_state.matchq = dict(st.session_state.matchq)

                            st.session_state.matchdata = list(st.session_state.pitq.items())
                            st.session_state.matchdata.insert(pos, (qname, ["N/A" for i in range(len(st.session_state.matchdata))]))
                            st.session_state.matchdata = dict(st.session_state.matchdata)

                            savedata()
                            savequestions()

                    else:

                        qoptsnum = c1.number_input("**How many options should this question have?**", min_value=2, step=1)
                        qdefindex = c2.number_input("**Enter the number of the option that this question should default to:**", min_value=1, max_value=qoptsnum, step=1)-1

                        qopts = []

                        if qoptsnum > 0:
                            for q in range(qoptsnum):
                                qopts.append(st.text_input(f"Option {q+1}:"))
                    
                        if sidebar.button("Insert Item"):

                            st.session_state.matchq = list(st.session_state.matchq.items())
                            st.session_state.matchq.insert(pos, (qname, {"Type": qtype, "Options": qopts, "DefaultIndex": qdefindex, "Display Name": displayname}))
                            st.session_state.matchq = dict(st.session_state.matchq)

                            st.session_state.matchdata = list(st.session_state.pitq.items())
                            st.session_state.matchdata.insert(pos, (qname, ["N/A" for i in range(len(st.session_state.matchdata))]))
                            st.session_state.matchdata = dict(st.session_state.matchdata)

                            savedata()
                            savequestions()

            else:
                st.write("**You need to add a question before you can insert questions.**")

    else:

        if qsect == "Pit":
            
            if len(st.session_state.pitq) == 0:
                st.subheader(f"No {qsect} Items Added Yet.")

            qtype = sidebar.selectbox("**What type of element would you like to add?**", qtypes)
            
            if qtype == "Header":

                qname = st.text_input("**What should the header say?**")

                if sidebar.button("Add Item"):
                    st.session_state.pitq[qname] = {"Type": qtype}
                    savedata()
                    savequestions()

            elif qtype == "Checkbox":

                qname = c1.text_input("**What should the checkbox say?**")
                defaultval = c2.radio("**Default Value:**", ["Unchecked", "Checked"])

                if defaultval == "Checked":
                    defaultindex = True

                else:
                    defaultindex = False

                if sidebar.button("Add Item"):
                    st.session_state.pitq[qname] = {"Type": qtype, "DefaultIndex": defaultindex}
                    newcol = ["N/A" for i in range(len(st.session_state.pitdata['Team No.']))]
                    st.session_state.pitdata[qname] = newcol
                    savedata()
                    savequestions()


            else:

                qname = c1.text_input("**What should this question ask?**")
                displayname = c2.text_input("**Data Column Display Name (:red[DO NOT USE EXISTING DISPLAY NAMES])**:", qname, max_chars=100)
                                        
                if qtype in "Text Input":

                    if sidebar.button("Add Item"):
                        st.session_state.pitq[qname] = {"Type": qtype, "Character Limit": 200, "Display Name": displayname}
                        newcol = ["N/A" for i in range(len(st.session_state.pitdata['Team No.']))]
                        st.session_state.pitdata[qname] = newcol
                        savedata()
                        savequestions()

                elif qtype in "Number Input":

                    qmin = c1.number_input("**Minimum Value**", step=1)
                    qmax = c2.number_input("**Maximum Value**", step=1)

                    if sidebar.button("Add Item"):
                        st.session_state.pitq[qname] = {"Type": qtype, "Minimum": qmin, "Maximum": qmax, "Display Name": displayname}
                        newcol = ["N/A" for i in range(len(st.session_state.pitdata['Team No.']))]
                        st.session_state.pitdata[qname] = newcol
                        savedata()
                        savequestions()

                else:

                    qoptsnum = c1.number_input("**How many options should this question have?**", 2, step=1)
                    qdefindex = c2.number_input("**Enter the number of the option that this question should default to:**", min_value=1, max_value=qoptsnum, step=1)-1

                    qopts = []

                    if qoptsnum > 0:
                        for q in range(qoptsnum):
                            qopts.append(st.text_input(f"Option {q+1}:"))
                
                    if sidebar.button("Add Item"):
                        st.session_state.pitq[qname] = {"Type": qtype, "Options": qopts, "DefaultIndex": qdefindex, "Display Name": displayname}
                        newcol = ["N/A" for i in range(len(st.session_state.pitdata['Team No.']))]
                        st.session_state.pitdata[qname] = newcol
                        savedata()
                        savequestions()

        if qsect == "Match":

            if len(st.session_state.matchq) == 0:
                st.subheader(f"No {qsect} Items Added Yet.")

            qtype = sidebar.selectbox("**What type of element would you like to add?**", qtypes)

            if qtype == "Header":

                qname = st.text_input("**What should the header say?**")

                if sidebar.button("Add Item"):
                    st.session_state.matchq[qname] = {"Type": qtype}
                    savedata()
                    savequestions()

            elif qtype == "Checkbox":

                qname = c1.text_input("**What should the checkbox say?**")
                defaultval = c2.radio("**Default Value:**", ["Unchecked", "Checked"])

                if defaultval == "Checked":
                    defaultindex = True

                else:
                    defaultindex = False

                if sidebar.button("Add Item"):
                    st.session_state.matchq[qname] = {"Type": qtype, "DefaultIndex": defaultindex}
                    newcol = ["N/A" for i in range(len(st.session_state.matchdata['Team No.']))]
                    st.session_state.matchdata[qname] = newcol
                    savedata()
                    savequestions()

            else:

                qname = c1.text_input("**What should this question ask?**")
                displayname = c2.text_input("**Data Column Display Name (:red[DO NOT USE EXISTING DISPLAY NAMES])**:", qname, max_chars=100)
                                        
                if qtype in "Text Input":

                    if sidebar.button("Add Item"):
                        st.session_state.matchq[qname] = {"Type": qtype, "Character Limit": 200, "Display Name": displayname}
                        newcol = ["N/A" for i in range(len(st.session_state.matchdata['Team No.']))]
                        st.session_state.matchdata[qname] = newcol
                        savedata()
                        savequestions()

                elif qtype in "Number Input":

                    qmin = c1.number_input("**Minimum Value**", step=1)
                    qmax = c2.number_input("**Maximum Value**", step=1)
                    ptval = c1.number_input("**Point Value (per objective scored - enter `0` if this is not a point-based question)**", step=1)
                    maxpts = c2.number_input("**Maximum Scorable Points (enter `0` for no limit)**", step=1)

                    if sidebar.button("Add Item"):
                        st.session_state.matchq[qname] = {"Type": qtype, "Minimum": qmin, "Maximum": qmax, "Point Value": ptval, "Maximum Points": maxpts, "Display Name": displayname}
                        newcol = ["N/A" for i in range(len(st.session_state.matchdata['Team No.']))]
                        st.session_state.matchdata[qname] = newcol
                        savedata()
                        savequestions()

                else:

                    qoptsnum = c1.number_input("**How many options should this question have?**", 2, step=1)
                    qdefindex = c2.number_input("**Enter the number of the option that this question should default to:**", min_value=1, max_value=qoptsnum, step=1)-1

                    qopts = []

                    if qoptsnum > 0:
                        for q in range(qoptsnum):
                            qopts.append(st.text_input(f"Option {q+1}:"))
                
                    st.session_state.matchq[qname] = {"Type": qtype, "Options": qopts, "DefaultIndex": qdefindex, "Display Name": displayname}

                    if sidebar.button("Add Item"):
                        newcol = ["N/A" for i in range(len(st.session_state.matchdata['Team No.']))]
                        st.session_state.matchdata[qname] = newcol
                        savedata()
                        savequestions()
    
    st.write("---")

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

elif sect == "**Edit Data**":

    showdata = sidebar.checkbox("Show Data", value=True)
    dataselect = sidebar.radio("**Which dataset would you like to edit?**", ["Pit Data", "Match Data"])

    if dataselect == "Pit Data":
        data = st.session_state.pitdata
    if dataselect == "Match Data":
        data = st.session_state.matchdata

    if len(data[list(data.keys())[0]]) == 0:
        st.header("This dataset is empty right now.")

    else:

        if showdata:
            st.header(dataselect)
            st.dataframe(data, use_container_width=True, hide_index=False)
            st.write("---")
            editmode = sidebar.radio("**Edit Mode:**", ["Replace", "Remove"])

        if editmode == "Replace":

            replaceselect = st.radio("Would you like to replace a row or a specific data entry?", ["Row", "Data Entry"])


exgitpull = sidebar.expander("**Pull From GitHub Repository**\n\n**(:red[OFFLINE ONLY])**")

if exgitpull.button("Pull From GitHub"):
    savedata()
    gitpull()
    savedata()

if st.session_state.admin:
    
    exgitpush = sidebar.expander("**Push To GitHub Repository**\n\n**(:red[OFFLINE ONLY])**")
    savemsg = exgitpush.text_input("**Commit Message:**", "Update GitHub", max_chars=100)

    if exgitpush.button("Push to GitHub"):
        savedata()
        gitpush(savemsg)


    exminpull = sidebar.expander("**Load Data From MinIO**")

    if exminpull.button("Load From MinIO"):

        with open("tempfile.csv", "w") as file:
            file.write(cloudSave.load_csv("pitdata.csv"))
        data = pd.read_csv("tempfile.csv").to_dict()
        del data["Unnamed: 0"]
        
        for col in data:

            vals = []

            for val in data[col].values():
                vals.append(str(val))
            
            data[col] = vals

        st.session_state.pitdata = data
        
        with open("tempfile.csv", "w") as file:
            file.write(cloudSave.load_csv("matchdata.csv"))
        data = pd.read_csv("tempfile.csv").to_dict()
        del data["Unnamed: 0"]
       
        for col in data:

            vals = []

            for val in data[col].values():
                vals.append(str(val))
            
            data[col] = vals

        st.session_state.matchdata = data
        
        savedata()
    
    exminpush = sidebar.expander("**Save Data to MinIO**")

    if exminpush.button("Save to MinIO"):

        data = pd.DataFrame.from_dict(st.session_state.pitdata).to_csv()
        cloudSave.save_csv("pitdata.csv", data)
        data = pd.DataFrame.from_dict(st.session_state.matchdata).to_csv()
        cloudSave.save_csv("matchdata.csv", data)

        cloudSave.save_questions(st.session_state.pitq, "pit")
        cloudSave.save_questions(st.session_state.matchq, "match")

    ex2 = sidebar.expander("**DANGER ZONE**\n\n**(:red[OFFLINE ONLY])**")
    clearlog = ex2.button("Clear System Log")
    resetdata = ex2.button("Reset Data")

    if clearlog:
        os.system("cls")
        print("""\033[1m
-------------------
Scouting XTREME Log
-------------------
        \033[0m""")

    if resetdata:

        for i in st.session_state.pitdata:
            st.session_state.pitdata[i] = []

        for i in st.session_state.matchdata:
            st.session_state.matchdata[i] = []

        savedata()

print(f"Admin Mode: {st.session_state.admin}")
