from pydantic import BaseModel  #Used to define request body schema
from datetime import datetime   

# CourseRequest for GET method
class CourseRequest(BaseModel):
    filters: dict = {}
    sort_col: str = "courses_id"
    sort_dir: str = "ASC"
    limit: int = 20
    offset: int = 0


#CourseCreate for INSERTING data into stagging table
class CourseCreate(BaseModel):
    courses_id: int
    course_code: str
    course_name: str
    description: str
    duration_months: int
    course_type: str
    category: str
    level: str
    prerequisites: str
    syllabus: str
    total_seats: int
    fee_amount: float
    is_active: bool = True
    created_at: datetime
    updated_at: datetime
