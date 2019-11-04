import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

IAM_ROLE_ARN = config.get("IAM_ROLE","ARN")
LOG_DATA = config.get("S3","LOG_DATA")
LOG_JSONPATH = config.get("S3","LOG_JSONPATH")
SONG_DATA = config.get("S3","SONG_DATA")


# DROP TABLES

staging_events_table_drop = "drop table if exists staging_events;"
staging_songs_table_drop = "drop table if exists staging_songs;"
songplay_table_drop = "drop table if exists songplays;"
user_table_drop = "drop table if exists users;"
song_table_drop = "drop table if exists songs;"
artist_table_drop = "drop table if exists artists;"
time_table_drop = "drop table if exists time;"

# CREATE TABLES

staging_events_table_create= ("""
CREATE TABLE IF NOT EXISTS staging_events \
(artist VARCHAR (255), auth VARCHAR (255), firstName VARCHAR (255), gender CHAR (1), itemInSession INT, lastName VARCHAR (255), length NUMERIC(18,8), level CHAR(4), \
location VARCHAR(255), method CHAR(3), page VARCHAR(50), registration NUMERIC(18,0), sessionId INT, \
song VARCHAR(255), status INT, ts BIGINT, userAgent TEXT, userId INT) ;
""")

staging_songs_table_create = ("""
CREATE TABLE IF NOT EXISTS staging_songs \
(num_songs INT, artist_id VARCHAR (255), artist_latitude NUMERIC(18,8), artist_longitude NUMERIC(18,8), artist_location VARCHAR (255), \
artist_name VARCHAR (255), song_id VARCHAR (255), title VARCHAR (255), duration NUMERIC(18,8), year INT);
""")

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays \
(songplay_id bigint identity(1, 1) NOT NULL, start_time bigint NULL, user_id INT NULL, level CHAR(4), song_id VARCHAR NULL, artist_id VARCHAR NULL, session_id INT, location VARCHAR, user_agent TEXT);
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users \
(user_id  INT NOT NULL sortkey distkey, first_name VARCHAR (255) NULL, last_name VARCHAR(255) NULL, gender CHAR(1) NULL, level CHAR(4) NULL);
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs \
(song_id VARCHAR(255) NOT NULL sortkey, title VARCHAR(255) NULL, artist_id VARCHAR(255) NULL distkey, year INT NULL, duration NUMERIC(18,8) NULL);
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists \
(artist_id VARCHAR(255) NOT NULL distkey, name VARCHAR(255) NULL, location VARCHAR(255) NULL, latitude NUMERIC(18,8) NULL, longitude NUMERIC(18,8) NULL);
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time \
(start_time BIGINT NOT NULL distkey, hour INT NULL, day INT NULL, week INT NULL, month INT NULL sortkey, year INT NULL, weekday INT NULL);
""")

# STAGING TABLES

staging_events_copy = ("""
copy staging_events from {}
credentials 'aws_iam_role={}'
json {};
""").format(LOG_DATA, IAM_ROLE_ARN, LOG_JSONPATH)

staging_songs_copy = ("""
copy staging_songs from {}
credentials 'aws_iam_role={}'
json 'auto';
""").format(SONG_DATA, IAM_ROLE_ARN)

# FINAL TABLES

songplay_table_insert = ("""
insert into songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent) \
( select distinct staging_events.ts, staging_events.userId, staging_events.level, tm.song_id, tm.artist_id, \
staging_events.sessionId, staging_events.location, staging_events.userAgent \
from public."staging_events" left join (select songs.song_id, songs.title, duration, songs.artist_id , artists.name \
from songs inner join artists on songs.artist_id = artists.artist_id) as tm on staging_events.song = tm.title AND staging_events.length = tm.duration \
where staging_events.page = 'NextSong' );
""")

user_table_insert = ("""
INSERT INTO users \
(SELECT distinct userId, firstName, lastName, gender, level FROM staging_events WHERE userId IS NOT NULL AND page ='NextSong');
""")

song_table_insert = ("""
INSERT INTO songs \
(SELECT song_id, title, artist_id, year, duration FROM staging_songs);
""")

artist_table_insert = ("""
INSERT INTO artists \
(SELECT distinct artist_id, artist_name, artist_location, artist_latitude, artist_longitude FROM staging_songs);
""")

time_table_insert = ("""
INSERT INTO time \
(SELECT ts \
,cast ( date_part('hour', TIMESTAMP 'epoch' + ts/1000 * INTERVAL'1 Second') as int) \
,cast ( date_part('day', TIMESTAMP 'epoch' + ts/1000 * INTERVAL'1 Second') as int) \
,cast ( date_part('week', TIMESTAMP 'epoch' + ts/1000 * INTERVAL'1 Second') as int) \
,cast ( date_part('month', TIMESTAMP 'epoch' + ts/1000 * INTERVAL'1 Second') as int) \
,cast ( date_part('year', TIMESTAMP 'epoch' + ts/1000 * INTERVAL'1 Second') as int) \
,cast ( date_part('weekday', TIMESTAMP 'epoch' + ts/1000 * INTERVAL'1 Second') as int) \
FROM staging_events WHERE page ='NextSong');
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [user_table_insert, song_table_insert, artist_table_insert, time_table_insert, songplay_table_insert]

#insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]

#print(staging_events_copy)
#print(staging_songs_copy)