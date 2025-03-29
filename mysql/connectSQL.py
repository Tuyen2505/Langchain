import mysql.connector

# def connect_to_mysql():
#     try:
#         connection = mysql.connector.connect(
#             host='DESKTOP-O4GQ5PS',
#             user='tuyen',
#             password='250503',
#             database='shopquanao'
#         )
#         if connection.is_connected():
#             print("Successfully connected to the database")
#             return connection
#     except mysql.connector.Error as err:
#         print(f"Error: {err}")
#         return None


def query_mysql(query):
    connection = mysql.connector.connect(
        host='DESKTOP-O4GQ5PS',
        user='tuyen',
        password='250503',
        database='clothes-web-shop'
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result


# while True:
#     text_input = input("Nhập văn bản (hoặc 'exit' để thoát): ")
#     if text_input.lower() == 'exit':
#         break
#     result = query_mysql(text_input)
#     print(result)