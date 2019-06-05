from mongoengine import connect


# Uncomment as needed to clear the database(s) during testing

db1 = connect('sat_database')
# db1.drop_database('sat_database')

db2 = connect('smt_database')
# db2.drop_database('smt_database')
