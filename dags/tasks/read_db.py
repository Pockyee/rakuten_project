import pandas as pd
from sqlalchemy import create_engine

def load_images():
    engine = create_engine("postgresql+psycopg2://rakutenadmin:rakutenadmin@postgres:5432/rakuten_db")

    df = pd.read_sql("SELECT imageid, productid FROM X_test", con=engine)

    filenames = [
        f"image_{row.imageid}_product_{row.productid}.jpg"
        for _, row in df.iterrows()
    ]
    print(filenames[:5])