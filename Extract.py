import pypyodbc as odbc #To connect to SQL SERVER DBMS
import pandas as pd # To clean the data

"""
Step 1. Importing dataset from CSV
"""
df = pd.read_csv('Real-Time_Traffic_Incident_Reports.csv')

"""
Step 2.1 Data clean up
"""
df['Published Date'] = pd.to_datetime(df['Published Date']).dt.strftime('%Y-%m-%d %H:%M:%S')
df['Status Date'] = pd.to_datetime(df['Published Date']).dt.strftime('%Y-%m-%d %H:%M:%S')

#Delete records that has no location or have a status
df.drop(df.query('Location.isnull() | Status.isnull()').index, inplace=True)


"""
Step 2.2 Specify columns we want to import
"""
columns = ['Traffic Report ID', 'Published Date', 'Issue Reported', 'Location', 
            'Address', 'Status', 'Status Date']

df_data = df[columns]
#Convert data set to list(nestless)
records = df_data.values.tolist()


"""
Step 3.1 Create SQL Server Connection String
"""
DRIVER = 'SQL SERVER'
SERVER_NAME = 'DESKTOP-EKP2CQS'
DATABASE_NAME = 'etlTest'

def connection_string(driver, server_name, database_name):
    conn_string = f"""
        DRIVER={{{driver}}};
        SERVER={server_name};
        DATABASE={database_name};
        Trust_Connection=yes;        
    """
    return conn_string

"""
Step 3.2 Create database connection instance
"""
try:
    conn = odbc.connect(connection_string(DRIVER, SERVER_NAME, DATABASE_NAME))
except odbc.DatabaseError as e:
    print('Database Error:')    
    print(str(e.value[1]))
except odbc.Error as e:
    print('Connection Error:')
    print(str(e.value[1]))


"""
Step 3.3 Create a cursor connection and insert records
"""

sql_insert = '''
    INSERT INTO Austin_Traffic_Incident 
    VALUES (?, ?, ?, ?, ?, ?, ?, GETDATE())
'''

try:
    cursor = conn.cursor()
    cursor.executemany(sql_insert, records)
    cursor.commit();    
except Exception as e:
    cursor.rollback()
    print(str(e[1]))
finally:
    print('Task is complete.')
    cursor.close()
    conn.close()