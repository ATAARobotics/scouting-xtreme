from io import BytesIO
from minio import Minio
from minio.error import ResponseError

def save_csv(csv_string):
    client = Minio("minio.101100.ca",
        access_key="uyBquJD1wBqebVcMhIgq",
        secret_key="ZGa6YUerybM1Jd0NPYugZhTnPhbtb48cZLiFuKYo",
    )

    csv_bytes = csv_string.encode('utf-8')
    try:
        result = client.put_object(
            "scouting-xtreme", "data.csv", BytesIO(csv_bytes), len(csv_bytes),
            content_type="application/csv",
        )
    except ResponseError as err:
        print("Failed to upload with error:", err)


save_csv("""Col1,Col2,Col3
1,2,3
4,5,7
7,8,9
""")
