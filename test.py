import sqlite3

con = sqlite3.connect('movies_2020s.db')
cursor = con.cursor()

#cursor.execute('SELECT production_countries FROM movie_data_raw')

cursor.execute('DELETE FROM movie_data_raw')
con.commit()
'''

rows = cursor.fetchall()
# Print the results
for row in rows:
    print(row)
'''
con.close()