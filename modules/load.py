import glob
import os
import shutil
from modules.dbload import ensure_database, get_connection

def load_dataframe_to_mysql(df, table_name='iris_setosa'):
    ensure_database()

    conn = get_connection()
    cursor = conn.cursor()

    columns = df.columns
    column_defs = ', '.join(f"{col} VARCHAR(255)" for col in columns)

    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    cursor.execute(f"CREATE TABLE {table_name} ({column_defs})")

    rows = [tuple(str(v) if v is not None else None for v in row) for row in df.collect()]
    if rows:
        placeholders = ', '.join(['%s'] * len(columns))
        insert_sql = f"INSERT INTO {table_name} ({', '.join(f'{col}' for col in columns)}) VALUES ({placeholders})"
        cursor.executemany(insert_sql, rows)

    conn.commit()
    cursor.close()
    conn.close()

def save_csv(df, output_folder, original_filename):
    import shutil

    # Byg det ønskede endelige filnavn: transformed_iris.csv
    final_filename = "transformed_" + original_filename
    final_path = os.path.join(output_folder, final_filename)

    # Spark gemmer til en midlertidig mappe
    temp_dir = os.path.join(output_folder, "_temp_spark_output")

    df.coalesce(1).write.csv(temp_dir, header=True, mode='overwrite')

    # Find den fil Spark oprettede (hedder noget med "part-00000...")
    part_files = glob.glob(os.path.join(temp_dir, "part-*.csv"))
    if not part_files:
        raise FileNotFoundError("Spark genererede ingen output-fil.")

    # Flyt og omdøb til det rigtige navn
    if os.path.exists(final_path):
        os.remove(final_path)
    shutil.move(part_files[0], final_path)

    # Slet den midlertidige mappe
    shutil.rmtree(temp_dir)

    print(f"CSV gemt: {final_path}")