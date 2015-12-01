#!/usr/bin/env python

"""
Sample script that creates 'Devices' table in an SQLite database, populates
it with some information about network devices, searches database and displays
content of the records, and finally, removes all the records from the database.

The SQLite is integrated in Python as sqlite3 module, which provides
an SQL interface compliant with the DB-API 2.0 specification described by
PEP 249.
"""

# Python standard library modules
import os
import sqlite3 as db


def print_device_info(device_info):
    """Prints out information about given device, represented by 4-tuple.
    """
    assert(isinstance(device_info, tuple))
    assert(len(device_info) == 4)
    print(" Device Name : %s" % device_info[0])
    print(" OS Type     : %s" % device_info[1])
    print(" IP Address  : %s" % device_info[2])
    print(" Interfaces  : %s" % device_info[3])


def db_create_device_table(db_path):
    """In the 'db_path' SQLite database file create the 'Devices' table if it
    does not exist yet.
    """
    try:
        # Open a connection to the 'db_path' database file, the database file
        # will be created automatically the first time we try to connect to it.
        # The 'connect' method returns 'Connection' object that represents the
        # database.
        with db.connect(db_path) as conn:
            # The cursor method returns 'Cursor' object to be used as
            # the primary reference point for all interactions with the
            # SQLite database systems.
            cursor = conn.cursor()

            # Prepare and execute SQL statement.
            # CREATE TABLE is the keyword telling the database system
            # to create a new table. The unique name or identifier for
            # the table follows the CREATE TABLE statement.
            # The 'name', 'os_type', 'ip_address' and 'interfaces' are the
            # column names for each row to be created in the table.
            # PRIMARY KEY constraint uniquely identifies each row/record
            # in a database table, primary key column cannot have NULL values.
            table_name = "Devices"
            sql = ("CREATE TABLE IF NOT EXISTS {tn}"
                   "(name TEXT PRIMARY KEY NOT NULL,"
                   "os_type TEXT,"
                   "ip_address TEXT,"
                   "interfaces TEXT)").format(tn=table_name)
            cursor.execute(sql)
    except (db.OperationalError) as e:
        print("!!!Error, %s" % repr(e))


def db_add_device_record(db_path, device_info):
    """Add a new or replace an existing record in the 'Devices' table."""
    path_exist = os.path.exists(db_path)
    if path_exist is False:
        print '!!!Error, database does not exist.'
        return

    try:
        with db.connect(db_path) as conn:
            cursor = conn.cursor()
            # Prepare and execute SQL statement.
            # The REPLACE statement is an alias for the "INSERT OR REPLACE"
            # variant of the INSERT statement. This alias is provided for
            # compatibility with other SQL database engines.
            tup = (device_info['device_name'],
                   device_info['os_type'],
                   device_info['ip_address'],
                   ", ".join(device_info['interfaces']))
            sql = ("REPLACE INTO Devices VALUES (?,?,?,?)")
            cursor.execute(sql, tup)
            conn.commit()
    except (db.OperationalError) as e:
        print("!!!Error, %s" % repr(e))


def db_get_device_info(db_path, rec_name):
    """Fetch record matching to the given 'rec_name' from
    the 'Devices' table.
    """
    path_exist = os.path.exists(db_path)
    if path_exist is False:
        print '!!!Error, database does not exist.'
        return

    try:
        with db.connect(db_path) as conn:
            cursor = conn.cursor()
            # Prepare and execute SQL statement
            sql = ("SELECT * FROM Devices WHERE name=?")
            cursor.execute(sql, (rec_name,))
            rec = cursor.fetchone()
            return rec
    except (db.OperationalError) as e:
        print("!!!Error, %s" % repr(e))


def db_delete_device_record(db_path, record_name):
    """Delete record matching to the given 'rec_name' from
    the 'Devices' table.
    """
    path_exist = os.path.exists(db_path)
    if path_exist is False:
        print '!!!Error, database does not exist.'
        return

    try:
        with db.connect(db_path) as conn:
            cursor = conn.cursor()
            # Prepare SQL query statement (make sure the 'record_name'
            # parameter follows with comma to make it a tuple)
            sql = "DELETE FROM Devices WHERE name=?"
            # Execute SQL query statement
            cursor.execute(sql, (record_name,))
    except (db.OperationalError) as e:
        print("!!!Error, %s" % repr(e))


def db_print_table_rows_cnt(db_path, table_name):
    """Prints current total number of rows in the table."""
    path_exist = os.path.exists(db_path)
    if path_exist is False:
        print '!!!Error, database does not exist.'
        return

    try:
        with db.connect(db_path) as conn:
            cursor = conn.cursor()
            print(" Table Name : '%s'" % table_name)
            # Prepare and execute SQL statement
            sql = ('SELECT COUNT(*) FROM {}').format(table_name)
            cursor.execute(sql)
            count = cursor.fetchall()
            print(" Total Rows : %s" % count[0][0])
    except (db.OperationalError) as e:
        print("!!!Error, %s" % repr(e))

if __name__ == "__main__":

    db_path = "./example1.db"

    device_info1 = {'device_name': 'Router1',
                    'os_type': 'IOS-XR',
                    'ip_address': '10.30.30.1',
                    'interfaces': ['Lo0', 'Mg0/0/CPU0/0',
                                   'Gi0/0/0/0', 'Gi0/0/0/1',
                                   'Gi0/0/0/2', 'Gi0/0/0/3']}
    device_info2 = {'device_name': 'Router2',
                    'os_type': 'IOS-XR',
                    'ip_address': '10.30.30.2',
                    'interfaces': ['Lo0', 'Mg0/0/CPU0/0',
                                   'Gi0/0/0/0', 'Gi0/0/0/1',
                                   'Gi0/0/0/2', 'Gi0/0/0/3']}
    device_info3 = {'device_name': 'Router3',
                    'os_type': 'IOS-XR',
                    'ip_address': '10.30.30.3',
                    'interfaces': ['Lo0', 'Mg0/0/CPU0/0',
                                   'Gi0/0/0/0', 'Gi0/0/0/1',
                                   'Gi0/0/0/2', 'Gi0/0/0/3']}
    devices_info = [device_info1, device_info2, device_info3]

    print("\n").strip()
    print("Creating 'Devices' Table")
    print("\n").strip()
    db_create_device_table(db_path)
    db_print_table_rows_cnt(db_path, 'Devices')
    print("\n").strip()

    print("Adding records to the 'Devices' Table")
    print("\n").strip()
    for item in devices_info:
        db_add_device_record(db_path, item)
    db_print_table_rows_cnt(db_path, 'Devices')
    print("\n").strip()

    print("Searching for the records in the 'Devices' Table")
    print("\n").strip()
    for item in devices_info:
        rec_name = item['device_name']
        device_info = db_get_device_info(db_path, rec_name)
        print("%s" % ('<' * 78))
        print_device_info(device_info)
        print("%s" % ('>' * 78))
    print("\n").strip()

    print("Removing records from the 'Devices' Table")
    print("\n").strip()
    for item in devices_info:
        db_delete_device_record(db_path, item['device_name'])
    db_print_table_rows_cnt(db_path, 'Devices')
    print("\n").strip()
