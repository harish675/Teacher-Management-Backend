from datetime import datetime, timezone

now = datetime.now(timezone.utc)

students_mock_data = [
    {"name": "Amit Sharma", "email": "amit.sharma@example.com", "age": 20, "is_active": True, "created_date": now, "updated_date": now},
    {"name": "Priya Desai", "email": "priya.desai@example.com", "age": 21, "is_active": True, "created_date": now, "updated_date": now},
    {"name": "Rahul Verma", "email": "rahul.verma@example.com", "age": 22, "is_active": True, "created_date": now, "updated_date": now},
    {"name": "Sneha Patil", "email": "sneha.patil@example.com", "age": 19, "is_active": True, "created_date": now, "updated_date": now},
    {"name": "Vikas Singh", "email": "vikas.singh@example.com", "age": 23, "is_active": True, "created_date": now, "updated_date": now},
    {"name": "Nisha Gupta", "email": "nisha.gupta@example.com", "age": 20, "is_active": True, "created_date": now, "updated_date": now},
    {"name": "Kunal Joshi", "email": "kunal.joshi@example.com", "age": 24, "is_active": True, "created_date": now, "updated_date": now},
    {"name": "Riya Kapoor", "email": "riya.kapoor@example.com", "age": 18, "is_active": True, "created_date": now, "updated_date": now},
    {"name": "Arjun Reddy", "email": "arjun.reddy@example.com", "age": 22, "is_active": True, "created_date": now, "updated_date": now},
    {"name": "Manisha Jagtap", "email": "manisha.jagtap@example.com", "age": 21, "is_active": True, "created_date": now, "updated_date": now},
    {"name": "Harshit Mehta", "email": "harshit.mehta@example.com", "age": 23, "is_active": True, "created_date": now, "updated_date": now},
    {"name": "Sonal Chavan", "email": "sonal.chavan@example.com", "age": 19, "is_active": True, "created_date": now, "updated_date": now},
    {"name": "Rohan Kulkarni", "email": "rohan.kulkarni@example.com", "age": 20, "is_active": True, "created_date": now, "updated_date": now},
    {"name": "Divya More", "email": "divya.more@example.com", "age": 22, "is_active": True, "created_date": now, "updated_date": now},
    {"name": "Sagar Nikam", "email": "sagar.nikam@example.com", "age": 24, "is_active": True, "created_date": now, "updated_date": now}
]

teachers_mock_data = [
    {"name": "Dr. Meera Kulkarni", "email": "meera.kulkarni@example.com", "subject_expertise": "Mathematics", "experience_years": 10, "is_active": True, "created_date": now, "updated_date": now},
    {"name": "Prof. Ajay Deshmukh", "email": "ajay.deshmukh@example.com", "subject_expertise": "Physics", "experience_years": 8, "is_active": True, "created_date": now, "updated_date": now},
    {"name": "Dr. Smita Patwardhan", "email": "smita.patwardhan@example.com", "subject_expertise": "Chemistry", "experience_years": 12, "is_active": True, "created_date": now, "updated_date": now},
    {"name": "Prof. Kiran Joshi", "email": "kiran.joshi@example.com", "subject_expertise": "Computer Science", "experience_years": 7, "is_active": True, "created_date": now, "updated_date": now},
    {"name": "Prof. Ravi Shinde", "email": "ravi.shinde@example.com", "subject_expertise": "Biology", "experience_years": 9, "is_active": True, "created_date": now, "updated_date": now},
    {"name": "Dr. Leena Shah", "email": "leena.shah@example.com", "subject_expertise": "English", "experience_years": 11, "is_active": True, "created_date": now, "updated_date": now},
    {"name": "Prof. Suresh Pawar", "email": "suresh.pawar@example.com", "subject_expertise": "History", "experience_years": 6, "is_active": True, "created_date": now, "updated_date": now},
    {"name": "Dr. Anita Naik", "email": "anita.naik@example.com", "subject_expertise": "Economics", "experience_years": 13, "is_active": True, "created_date": now, "updated_date": now},
    {"name": "Prof. Manohar Kale", "email": "manohar.kale@example.com", "subject_expertise": "Sociology", "experience_years": 5, "is_active": True, "created_date": now, "updated_date": now},
    {"name": "Dr. Varsha Deshpande", "email": "varsha.deshpande@example.com", "subject_expertise": "Statistics", "experience_years": 14, "is_active": True, "created_date": now, "updated_date": now}
]

courses_mock_data = [
    {"course_name": "Mathematics 101", "description": "Basic and advanced mathematics concepts", "teacher_ids": [], "enrolled_student_ids": [], "is_active": True, "created_date": now, "updated_date": now},
    {"course_name": "Physics Fundamentals", "description": "Introduction to classical and modern physics", "teacher_ids": [], "enrolled_student_ids": [], "is_active": True, "created_date": now, "updated_date": now},
    {"course_name": "Organic Chemistry", "description": "Foundations of organic chemical structures", "teacher_ids": [], "enrolled_student_ids": [], "is_active": True, "created_date": now, "updated_date": now},
    {"course_name": "Computer Programming", "description": "Learn programming fundamentals", "teacher_ids": [], "enrolled_student_ids": [], "is_active": True, "created_date": now, "updated_date": now},
    {"course_name": "English Communication", "description": "Improve spoken & written English", "teacher_ids": [], "enrolled_student_ids": [], "is_active": True, "created_date": now, "updated_date": now}
]
