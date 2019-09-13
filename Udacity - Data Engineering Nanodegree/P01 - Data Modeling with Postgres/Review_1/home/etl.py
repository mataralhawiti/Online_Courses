import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *
pd.set_option('mode.chained_assignment', None)


def process_song_file(cur, filepath):
    # open song file
    df =  pd.DataFrame()
    df = df.append(pd.read_json(filepath, typ='series'),ignore_index=True)

    # insert song record
    song_data = df.iloc[0][['song_id', 'title', 'artist_id', 'year', 'duration']]
    try :
        cur.execute(song_table_insert, song_data)
    except psycopg2.Error as e:
        cur.execute("rollback;")

    
    # insert artist record
    artist_data = df.iloc[0][['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']]
    try :
        cur.execute(artist_table_insert, artist_data)
    except psycopg2.Error as e:
        cur.execute("rollback;")
        


def process_log_file(cur, filepath):
    # open log file
    df = pd.DataFrame()
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df.loc[df['page']=='NextSong']

    # convert timestamp column to datetime
    t = df[['ts']]
    t['datetime'] = pd.to_datetime(t['ts'], unit='ms')
    
    t['hour'] = t['datetime'].dt.hour
    t['day'] = t['datetime'].dt.day
    t['week'] = t['datetime'].dt.week
    t['month'] = t['datetime'].dt.month
    t['year'] = t['datetime'].dt.year
    t['weekday'] = t['datetime'].dt.weekday
    
    # insert time data records
    time_data = (list(t['ts'].values), 
                 list(t['hour'].values), 
                 list(t['day'].values), 
                 list(t['week'].values), 
                 list(t['month'].values), 
                 list(t['year'].values),
                 list(t['weekday'].values)
                )
    
    column_labels = list(t.columns.values)
    column_labels.remove('datetime')
    
    time_df = pd.DataFrame.from_dict(dict(zip(column_labels, time_data)))

    for i, row in time_df.iterrows():
        try :
            cur.execute(time_table_insert, list(row))
        except psycopg2.Error as e:
            cur.execute("rollback;")
            

    # load user table
    user_df = df.loc[:, ['userId', 'firstName', 'lastName', 'gender', 'level']]
    
    # remove duplicate rows
    user_df.drop_duplicates(keep="first",inplace=True) 

    # insert user records
    for i, row in user_df.iterrows():
        try :
            cur.execute(user_table_insert, row)
        except psycopg2.Error as e:
            cur.execute("rollback;")

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row.ts, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        try :
            cur.execute(songplay_table_insert, songplay_data)
        except psycopg2.Error as e:
            cur.execute("rollback;")
            

def process_data(cur, conn, filepath, func):
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()