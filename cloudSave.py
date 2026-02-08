from io import BytesIO
from minio import Minio
import pandas as pd

def load_csv(filename):
    client = Minio("minio.101100.ca",
        access_key="uyBquJD1wBqebVcMhIgq",
        secret_key="ZGa6YUerybM1Jd0NPYugZhTnPhbtb48cZLiFuKYo",
    )

    try:
        response = client.get_object("scouting-xtreme", filename)
        return response.data.decode("ISO-8859-1")
    
    except:
        print("Failed to upload")
    finally:
        response.close()
        response.release_conn()

def save_csv(filename, csv_string):
    client = Minio("minio.101100.ca",
        access_key="uyBquJD1wBqebVcMhIgq",
        secret_key="ZGa6YUerybM1Jd0NPYugZhTnPhbtb48cZLiFuKYo",
    )

    csv_bytes = csv_string.encode('ISO-8859-1')
    try:
        result = client.put_object(
            "scouting-xtreme", filename, BytesIO(csv_bytes), len(csv_bytes),
            content_type="application/csv",
        )
    except:
        print("Failed to download")

def save_image(filename, image, ext):

    client = Minio("minio.101100.ca",
        access_key="uyBquJD1wBqebVcMhIgq",
        secret_key="ZGa6YUerybM1Jd0NPYugZhTnPhbtb48cZLiFuKYo",
    )

    try:
        result = client.put_object(
            "scouting-xtreme", filename, BytesIO(image), len(image),
            content_type=f"application/{ext}",
        )
    except:
        print("Failed to download")
    

def save_questions(questions, dataset="pit"):
    """
    questions: question dictionary from the main file
    dataset: \"pit\" or \"match\"
    """

    qmain = {
        "Position": [],
        "Type": [],
        "Question": []
    }
    qnr = {
        "Position": [],
        "Question": [],
        "Minimum": [],
        "Maximum": []
    }
    qmc = {
        "Position": [],
        "Question": [],
        "Option1": [],
        "Option1": [],
        "Option2": [],
        "Option3": [],
        "Option4": [],
        "Option5": [],
        "Option6": [],
        "Option7": [],
        "Option8": [],
        "Option9": [],
        "Option10": []
    }
    qsb = {
        "Position": [],
        "Question": [],
        "Option1": [],
        "Option1": [],
        "Option2": [],
        "Option3": [],
        "Option4": [],
        "Option5": [],
        "Option6": [],
        "Option7": [],
        "Option8": [],
        "Option9": [],
        "Option10": []
    }

    qnum = 0

    for question in questions:

        if questions[question]["Type"] == "Multiple Choice":
            
            qmc["Question"].append(question)
            qmc["Position"].append(qnum+1)
            
            for i in range(len(questions[question]["Options"])):
                qmc[f"Option{i+1}"].append(questions[question]["Options"][i])

            if len(questions[question]["Options"]) < 10:

                for i in range(len(questions[question]["Options"]), 10):
                    qmc[f"Option{i+1}"].append("N/A")

        elif questions[question]["Type"] == "Selection Box":
            
            qsb["Question"].append(question)
            qsb["Position"].append(qnum+1)
            
            for i in range(len(questions[question]["Options"])):
                qsb[f"Option{i+1}"].append(questions["Question"]["Options"][i])

            if len(questions[question]["Options"]) < 10:

                for i in range(len(questions[question]["Options"]), 10):
                    qsb[f"Option{i+1}"].append("N/A")

        elif questions[question]["Type"] == "Number Input":
            
            qnr["Question"].append(question)
            qnr["Position"].append(qnum+1)
            qnr["Minimum"].append(questions[question]["Minimum"])
            qnr["Maximum"].append(questions[question]["Maximum"])

        else:
            qmain["Question"].append(question)
            qmain["Position"].append(qnum+1)
            qmain["Type"].append(questions[question]["Type"])

        qnum += 1

    qdata = pd.DataFrame.from_dict(qmain).to_csv()
    save_csv(f"{dataset}qmain.csv", qdata)

    qdata = pd.DataFrame.from_dict(qmc).to_csv()
    save_csv(f"{dataset}qmc.csv", qdata)

    qdata = pd.DataFrame.from_dict(qsb).to_csv()
    save_csv(f"{dataset}qsb.csv", qdata)

    qdata = pd.DataFrame.from_dict(qnr).to_csv()
    save_csv(f"{dataset}qnr.csv", qdata)