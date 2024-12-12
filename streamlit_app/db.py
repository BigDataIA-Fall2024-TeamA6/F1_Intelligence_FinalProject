from langchain_community.utilities import SQLDatabase


def get_connection():

    host = 'bdia-finalproject-instance.chk4u4ukiif4.us-east-1.rds.amazonaws.com'
    user='admin'
    password='amazonrds7245'
    port = 3306
    database='bdia_team6_finalproject_db'   

    url="mysql+mysqlconnector://{0}:{1}@{2}:{3}/{4}".format(user,password,host,port,database)
    db = SQLDatabase.from_uri(url)  
    return db
