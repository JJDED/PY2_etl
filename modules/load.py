import os
import glob
import shutil
import pandas as pd
from modules.dbload import ensure_database, get_connection
from modules.security import encrypt


def load_dataframe_to_mysql(df, table_name='iris_setosa'):
    """
    Krypterer alle celleværdier og gemmer dem i MySQL.
    """
    ensure_database()
    conn = get_connection()
    cursor = conn.cursor()

    columns = df.columns

    # TEXT i stedet for VARCHAR da krypterede værdier er lange base64-strenge
    column_defs = ', '.join(f"`{col}` TEXT" for col in columns)
    cursor.execute(f"DROP TABLE IF EXISTS `{table_name}`")
    cursor.execute(f"CREATE TABLE `{table_name}` ({column_defs})")

    # Krypter hver celle i hver række
    encrypted_rows = []
    for row in df.collect():
        encrypted_row = tuple(encrypt(str(v)) if v is not None else None for v in row)
        encrypted_rows.append(encrypted_row)

    if encrypted_rows:
        placeholders = ', '.join(['%s'] * len(columns))
        col_names = ', '.join(f"`{col}`" for col in columns)
        insert_sql = f"INSERT INTO `{table_name}` ({col_names}) VALUES ({placeholders})"
        cursor.executemany(insert_sql, encrypted_rows)

    conn.commit()
    cursor.close()
    conn.close()
    print(f"[load] {len(encrypted_rows)} krypterede rækker gemt i MySQL.")


def save_csv(df, output_folder, original_filename):
    """
    Krypterer alle celleværdier og gemmer dem i en CSV-fil.
    """
    # Konverter Spark DataFrame til pandas
    pandas_df = df.toPandas()

    # Krypter hver celle med encrypt()
    encrypted_df = pandas_df.map(lambda v: encrypt(str(v)) if v is not None else None)

    # Gem som CSV
    os.makedirs(output_folder, exist_ok=True)
    final_filename = "transformed_" + original_filename
    final_path = os.path.join(output_folder, final_filename)

    encrypted_df.to_csv(final_path, index=False)
    print(f"[load] Krypteret CSV gemt: {final_path}")