from io import BytesIO
from minio import Minio

def load_csv(filename):
    client = Minio("minio.101100.ca",
        access_key="uyBquJD1wBqebVcMhIgq",
        secret_key="ZGa6YUerybM1Jd0NPYugZhTnPhbtb48cZLiFuKYo",
    )

    try:
        response = client.get_object("scouting-xtreme", filename)
        return response.data.decode("utf-8")
    
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

    csv_bytes = csv_string.encode('utf-8')
    try:
        result = client.put_object(
            "scouting-xtreme", filename, BytesIO(csv_bytes), len(csv_bytes),
            content_type="application/csv",
        )
    except:
        print("Failed to download")