from mongoengine import connect


db1 = connect('sat_database')
db1.drop_database('sat_database')
