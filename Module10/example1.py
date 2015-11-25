#!/usr/bin/python

# Python standard library modules
import os
import sqlite3 as sql


def db_create_table(db_path, table_name):
    try:
        with sql.connect(db_path) as conn:
            print("Creating new '%s' table" % table_name)
            cursor = conn.cursor()

            # UNIQUE constraint prevents two records from having identical
            # values in a particular column. In this example two rows with
            # same value for the name column are not allowed for insert
            query = ("CREATE TABLE IF NOT EXISTS {tn}"
                     "(name TEXT UNIQUE, "
                     "os_type TEXT, "
                     "ip_address TEXT)").format(tn=table_name)
            cursor.execute(query)
    except (sql.OperationalError) as e:
        print("!!!Error, %s" % repr(e))


def db_dump_table(db_path, table_name):
    path_exist = os.path.exists(db_path)
    if path_exist is False:
        print '!!!Error, database does not exist.'
        return

    try:
        with sql.connect(db_path) as conn:
            cursor = conn.cursor()
            print("'%s' table:" % table_name)

            # Prepare SQL query statement
            query = ("PRAGMA TABLE_INFO({tn})").format(tn=table_name)
            # Execute an SQL statement
            cursor.execute(query)
            names = [tup[1] for tup in cursor.fetchall()]
            print(names)

            # Prepare SQL query statement
            query = ("SELECT * FROM {tn}").format(tn=table_name)
            # Execute an SQL statement
            for row in cursor.execute(query):
                print row
    except (sql.OperationalError) as e:
        print("!!!Error, %s" % repr(e))


def db_insert_table_record(db_path, device_info):
    path_exist = os.path.exists(db_path)
    if path_exist is False:
        print '!!!Error, database does not exist.'
        return

    try:
        with sql.connect(db_path) as conn:
            print 'Adding new entry'
            cursor = conn.cursor()
            # Prepare SQL query statement
            tup = (device_info['device_name'],
                   device_info['os_type'],
                   device_info['ip_address'])
            query = ("REPLACE INTO Devices VALUES (?,?,?)")
            # Execute SQL query statement
            cursor.execute(query, tup)
            conn.commit()
    except (sql.OperationalError) as e:
        print("!!!Error, %s" % repr(e))


def db_delete_table_record(db_path, record_name):
    path_exist = os.path.exists(db_path)
    if path_exist is False:
        print '!!!Error, database does not exist.'
        return

    try:
        with sql.connect(db_path) as conn:
            print("Removing '%s' record" % record_name)
            cursor = conn.cursor()
            # Prepare SQL query statement (make sure the 'record_name'
            # parameter follows with comma to make it a tuple)
            query = "DELETE FROM Devices WHERE name=?"
            # Execute SQL query statement
            cursor.execute(query, (record_name,))
    except (sql.OperationalError) as e:
        print("!!!Error, %s" % repr(e))
    pass


if __name__ == "__main__":
    db_path = "./network.db"
    table_name = "Devices"
    print "0.0"
    db_create_table(db_path, "Devices")

    db_dump_table(db_path, table_name)

    device_info1 = {'device_name': 'Device1',
                    'os_type': 'IOS-XR',
                    'ip_address': '10.30.30.1'}
    db_insert_table_record(db_path, device_info1)
    db_dump_table(db_path, table_name)

    device_info2 = {'device_name': 'Device2',
                    'os_type': 'IOS-XR',
                    'ip_address': '10.30.30.22'}
    db_insert_table_record(db_path, device_info2)
    db_dump_table(db_path, table_name)

    record_name = device_info1['device_name']
    db_delete_table_record(db_path, record_name)
    db_dump_table(db_path, table_name)
