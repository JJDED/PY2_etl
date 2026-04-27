# visualize.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mysql.connector
import os

from modules.dbload import get_connection  # genbrug den forbindelse der allerede virker

def fetch_dataframe_from_mysql(table_name='iris_setosa'):
    conn = get_connection()
    df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    conn.close()
    
    # Konverter alle numeriske kolonner én gang her
    numeric_cols = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
    
    return df

# def fetch_dataframe_from_mysql(table_name='iris_setosa'):
#     conn = get_connection()  # samme forbindelse som load.py bruger
#     df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
#     conn.close()
#     return df

# def fetch_dataframe_from_mysql(table_name='iris_setosa'):
#     """
#     Henter data fra MySQL og returnerer det som en pandas DataFrame.
#     Kaldes i main.py FØR de 3 visualiseringsmetoder.
#     """
#     conn = mysql.connector.connect(
#         unix_socket='/var/run/mysqld/mysqld.sock',
#         user=os.getenv('DB_USER', 'jjd'),
#         database=os.getenv('DB_NAME', 'floradb')
#     )
#     df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
#     conn.close()
#     return df

def plot_scatter(df, output_folder='output_data'):
    """Scatter plot: sepal_length (x) vs petal_length (y)"""
    plt.figure(figsize=(8, 6))
    plt.scatter(df['sepal_length'], df['petal_length'], alpha=0.7, color='steelblue', edgecolors='white')
    plt.xlabel('Sepal Length (cm)')
    plt.ylabel('Petal Length (cm)')
    plt.title('Iris-setosa: Sepal Length vs Petal Length')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, 'scatter_plot.png'), dpi=150)
    plt.show()

def plot_histogram(df, output_folder='output_data'):
    """Histogram: fordeling af petal_width"""
    plt.figure(figsize=(8, 6))
    plt.hist(df['petal_width'], bins=10, color='steelblue', edgecolor='black', alpha=0.8)
    plt.xlabel('Petal Width (cm)')
    plt.ylabel('Antal observationer')
    plt.title('Iris-setosa: Fordeling af Petal Width')
    plt.grid(True, axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, 'histogram.png'), dpi=150)
    plt.show()

def plot_boxplot(df, output_folder='output_data'):
    """Boxplot: statistisk spredning for alle 4 målinger"""
    numeric_cols = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
    plt.figure(figsize=(9, 6))
    sns.boxplot(data=df[numeric_cols], palette='Set2', width=0.5)
    plt.xlabel('Måling')
    plt.ylabel('Værdi (cm)')
    plt.title('Iris-setosa: Statistisk fordeling af alle målinger')
    plt.xticks(range(len(numeric_cols)), ['Sepal Length', 'Sepal Width', 'Petal Length', 'Petal Width'])
    plt.grid(True, axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, 'boxplot.png'), dpi=150)
    plt.show()