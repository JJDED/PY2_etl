from pyspark.sql import SparkSession

def filter_by_value(csv_path, column, value):
    spark = SparkSession.builder.getOrCreate()
    df = spark.read.csv(csv_path, header=False).toDF('sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species')
    return df.filter(df[column] == value)

# spark = SparkSession \
#     .builder \
#     .appName("Python Spark SQL basic example") \
#     .config("spark.some.config.option", "some-value") \
#     .getOrCreate()

# def read_iris_file(filepath):
#     df = spark.read.csv(filepath, header=False, inferSchema=True)
#     df.show(5)
#     return df

# def add_colums (df):
#     pass

# def select_setosa(df):
#     pass

# if __name__ == "__main__":
#     read_iris_file("input_data/iris.csv")