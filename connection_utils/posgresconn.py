
import psycopg2


class postgres_conn:
    def getConn(self):
        try:
            connection = psycopg2.connect(user="bi_marico",
                                          password="bi_marico$028e1a5a92a1c984b80f5bc9cf89b74c",
                                          host="1.pgsql.db.1digitalstack.com",
                                          port="5432",
                                          database="postgres")
            cursor = connection.cursor()
            # Print PostgreSQL Connection properties
            print(connection.get_dsn_parameters(), "\n")
            # Print PostgreSQL version
            return cursor, connection
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
            return error, error
        
    def getConn2(self):
        try:
            connection = psycopg2.connect(user="powerbi",
                                          password="powerbi@007",
                                          host="2.pgsql.db.1digitalstack.com",
                                          port="5432",
                                          database="postgres")
            cursor = connection.cursor()
            # Print PostgreSQL Connection properties
            print(connection.get_dsn_parameters(), "\n")
            # Print PostgreSQL version
            return cursor, connection
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
            return error, error
        
    def close_connection(self, cursor, connection):
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
            
    def getConn3(self):
        try:
            connection = psycopg2.connect(user="postgres",
                                          password="powerbi@007",
                                          host="3.pgsql.db.1digitalstack.com",
                                          port="5432",
                                          database="postgres")
            cursor = connection.cursor()
            # Print PostgreSQL Connection properties
            print(connection.get_dsn_parameters(), "\n")
            # Print PostgreSQL version
            return cursor, connection
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
            return error, error