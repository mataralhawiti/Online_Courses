# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays \
(songplay_id SERIAL PRIMARY KEY, start_time timestamp NOT NULL, user_id INT NOT NULL, level CHAR(4), song_id VARCHAR, artist_id VARCHAR, session_id INT, location VARCHAR, user_agent TEXT);
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users \
(user_id  INT PRIMARY KEY , first_name  VARCHAR (255), last_name VARCHAR (255), gender CHAR(1), level CHAR(4));
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs \
(song_id VARCHAR (255) PRIMARY KEY, title VARCHAR (255), artist_id VARCHAR (255), year INT, duration NUMERIC(8,5));
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists \
(artist_id VARCHAR (255) PRIMARY KEY, name VARCHAR (255), location VARCHAR (255), latitude DECIMAL, longitude DECIMAL);
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time \
(start_time timestamp PRIMARY KEY, hour INT, day INT, week INT, month INT, year INT, weekday INT);
""")




# INSERT RECORDS

songplay_table_insert = ("""
INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent) \
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
""")

user_table_insert = ("""
INSERT INTO users (user_id, first_name, last_name, gender, level) \
                 VALUES (%s, %s, %s, %s, %s) ON CONFLICT (user_id) DO UPDATE SET level=EXCLUDED.level;
""")

song_table_insert = ("""
INSERT INTO songs (song_id, title, artist_id, year, duration) \
                 VALUES (%s, %s, %s, %s, %s) ON CONFLICT (song_id) DO NOTHING;
""")

artist_table_insert = ("""
INSERT INTO artists (artist_id, name, location, latitude, longitude) \
                 VALUES (%s, %s, %s, %s, %s) ON CONFLICT (artist_id) DO NOTHING;
""")


time_table_insert = ("""
INSERT INTO time (start_time, hour, day, week, month, year, weekday) \
                 VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (start_time) DO NOTHING;
""")

# FIND SONGS

song_select = ("""
select songs.song_id, artists.artist_id \
from songs JOIN artists ON songs.artist_id = artists.artist_id \
where songs.title = %s AND artists.name = %s AND songs.duration = %s ;
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]