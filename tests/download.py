from io import BytesIO
from minio import Minio
from minio.error import ResponseError

def load_csv():
    client = Minio("minio.101100.ca",
        access_key="uyBquJD1wBqebVcMhIgq",
        secret_key="ZGa6YUerybM1Jd0NPYugZhTnPhbtb48cZLiFuKYo",
    )

    try:
        response = client.get_object("scouting-xtreme", "data.csv")

        return response.data.decode("utf-8")
    except ResponseError as err:
        print("Failed to upload with error:", err)
    finally:
        response.close()
        response.release_conn()


loaded_csv = load_csv()

print("Got CSV:", loaded_csv)
