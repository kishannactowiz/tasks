import mysql.connector
import json
def connction():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="actowiz",
        database="tometo_db"
    )

    cur =conn.cursor()
    return conn,cur

def create_db():
    conn,cur = connction()
    cur.execute('''
    create table if not exists movies(
                m_id int auto_increment primary key,
                movie_name varchar(255),
                score varchar(255),
                description text,
                img text,
                review_count int,
                videos json,
                want_to_know text,
                cast_and_crew json,
                all_reviews json
                )
    ''')
    conn.commit()
    conn.close()

def insert_movie(data):
    conn, cur = connction()

    query = '''
    INSERT INTO movies(
        movie_name,
        score,
        description,
        img,
        review_count,
        videos,
        want_to_know,
        cast_and_crew,
        all_reviews
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''

    values = (
        data.get('movie_name'),
        data.get('score'),
        data.get('desc'),
        data.get('img'),
        data.get('review_count'),
        json.dumps(data.get('videos')),
        data.get('want_to_know'),      
        json.dumps(data.get('cast')),
        json.dumps(data.get('all_reviews'))   # ✅ fixed
    )

    cur.execute(query, values)
    conn.commit()
    conn.close()