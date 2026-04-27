import os
import modules.extract
from modules.extract import download_file_wget, download_file_subprocess, download_file_requests, extract_iris
from modules.transform import filter_by_value
from modules.load import save_csv, load_dataframe_to_mysql
from modules.visualize import fetch_dataframe_from_mysql, plot_scatter, plot_histogram, plot_boxplot

IRIS_DOWNLOAD_URL = 'https://raw.githubusercontent.com/jbrownlee/Datasets/master/iris.csv'
INPUT_FOLDER = 'input_data'
CSV_FILE = 'iris.csv'
OUTPUT_FOLDER = 'output_data' #+ '/transformed_' + CSV_FILE


# Download filer
# download_file_wget(IRIS_DOWNLOAD_URL, INPUT_FOLDER)
# download_file_subprocess(IRIS_DOWNLOAD_URL, INPUT_FOLDER)
download_file_requests(IRIS_DOWNLOAD_URL, INPUT_FOLDER)

# Filtrer din data
filtered = filter_by_value(os.path.join(INPUT_FOLDER, CSV_FILE), column='species', value='Iris-setosa')
save_csv(filtered, OUTPUT_FOLDER, original_filename=CSV_FILE)
load_dataframe_to_mysql(filtered)

# Hent data fra db
vis_df = fetch_dataframe_from_mysql()

# Generer diagrammer
plot_scatter(vis_df, OUTPUT_FOLDER)
plot_histogram(vis_df, OUTPUT_FOLDER)
plot_boxplot(vis_df, OUTPUT_FOLDER)