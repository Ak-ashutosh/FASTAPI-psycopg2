from fastapi import FastAPI     #Web framework to create APIs
import json                     #Converts Python dictionary to JSON string (for DB function input)
from db import get_connection   #DB connection
from model import CourseRequest 
from model import CourseCreate  

app = FastAPI()

# CREATE STAGING TABLE ON STARTUP
@app.on_event("startup")
def create_staging_table():
    conn = get_connection()
    query = conn.cursor()  #cursor() object gives .execute() method

    query.execute("""
        CREATE TABLE IF NOT EXISTS stg_courses AS
        SELECT * FROM courses WHERE 1=0;
    """)

    conn.commit()
    query.close()
    conn.close()

    print("Staging table ready")

#Insert data into stagging table
@app.post("/courses/staging")
def insert_into_staging(course: CourseCreate):
    conn = get_connection()
    query = conn.cursor()

    query.execute("""
        INSERT INTO stg_courses (
            courses_id,
            course_code,
            course_name,
            description,
            duration_months,
            course_type,
            category,
            level,
            prerequisites,
            syllabus,
            total_seats,
            fee_amount,
            is_active,
            created_at,
            updated_at
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING *;
    """, (
        course.courses_id,
        course.course_code,
        course.course_name,
        course.description,
        course.duration_months,
        course.course_type,
        course.category,
        course.level,
        course.prerequisites,
        course.syllabus,
        course.total_seats,
        course.fee_amount,
        course.is_active,
        course.created_at,
        course.updated_at
    ))

    inserted = query.fetchone()
    columns = [desc[0] for desc in query.description]

    conn.commit()
    query.close()
    conn.close()

    print("Data inserted into staging successfully")
    return {"data": dict(zip(columns, inserted))}


# GET COURSES
@app.post("/courses/get")
def get_courses(request: CourseRequest):

    conn = get_connection()
    query = conn.cursor()

    query.execute(
        """
        SELECT * FROM public.crud_get_courses(
            %s, %s, %s, %s, %s
        );
        """,
        (
            json.dumps(request.filters),
            request.sort_col,
            request.sort_dir,
            request.limit,
            request.offset
        )
    )

    columns = [desc[0] for desc in query.description]
    rows = query.fetchall()

    result = [dict(zip(columns, row)) for row in rows]

    query.close()
    conn.close()

    return {"data": result}


# SAVE FROM STAGING → MAIN TABLE
@app.put("/courses/save")
def save_courses():
    conn = get_connection()
    query = conn.cursor()

    query.execute(
        "SELECT public.crud_put_courses(%s);",
        ('stg_courses',)
    )

    status = query.fetchone()[0]

    conn.commit()
    query.close()
    conn.close()

    return {"status": status}


# DELETE COURSE
@app.delete("/courses/{course_id}")
def delete_course(course_id: int):
    conn = get_connection()
    query = conn.cursor()

    query.execute(
        "SELECT public.crud_delete_courses(%s);",
        (course_id,)
    )

    status = query.fetchone()[0]

    conn.commit()
    query.close()
    conn.close()

    return {"status": status}
