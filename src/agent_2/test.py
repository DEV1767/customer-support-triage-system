from agent_2.database import check_connection

if check_connection():
    print("MongoDB connected successfully!")