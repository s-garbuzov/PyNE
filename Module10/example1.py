#!/usr/bin/env python


# Python standard library modules
import os
import sqlite3 as db


def db_create_device_table(db_path):
    try:
        with db.connect(db_path) as conn:
            table_name = "Devices"
            cursor = conn.cursor()

            # PRIMARY KEY constraint uniquely identifies each row/record
            # in a database table.
            # Primary keys must contain unique values, a primary key column
            # cannot have NULL values.
            sql = ("CREATE TABLE IF NOT EXISTS {tn}"
                   "(name TEXT PRIMARY KEY NOT NULL,"
                   "os_type TEXT NOT NULL,"
                   "ip_address TEXT NOT NULL,"
                   "interfaces BLOB)").format(tn=table_name)
            cursor.execute(sql)
    except (db.OperationalError) as e:
        print("!!!Error, %s" % repr(e))


def db_insert_device_record(db_path, device_info):
    path_exist = os.path.exists(db_path)
    if path_exist is False:
        print '!!!Error, database does not exist.'
        return

    try:
        with db.connect(db_path) as conn:
            cursor = conn.cursor()
            # Prepare SQL query statement
            tup = (device_info['device_name'],
                   device_info['os_type'],
                   device_info['ip_address'],
                   ",".join(device_info['interfaces']))
            sql = ("REPLACE INTO Devices VALUES (?,?,?,?)")
            # Execute SQL query statement
            cursor.execute(sql, tup)
            conn.commit()
    except (db.OperationalError) as e:
        print("!!!Error, %s" % repr(e))


def db_delete_device_record(db_path, record_name):
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


def db_dump_table(db_path, table_name):
    path_exist = os.path.exists(db_path)
    if path_exist is False:
        print '!!!Error, database does not exist.'
        return

    try:
        with db.connect(db_path) as conn:
            cursor = conn.cursor()
            print("  Table %s' :" % table_name)

            # Prepare SQL query statement
            sql = ("PRAGMA TABLE_INFO({tn})").format(tn=table_name)
            # Execute SQL query statement
            cursor.execute(sql)
            names = [tup[1] for tup in cursor.fetchall()]
            print("  %s" % names)

            # Prepare SQL query statement
            sql = ("SELECT * FROM {tn}").format(tn=table_name)
            # Execute SQL query statement
            for row in cursor.execute(sql):
                print("  %s" % str(row))
            print("\n").strip()
    except (db.OperationalError) as e:
        print("!!!Error, %s" % repr(e))

if __name__ == "__main__":

    device_info1 = {'device_name': 'Device1',
                    'os_type': 'IOS-XR',
                    'ip_address': '10.30.30.1',
                    'interfaces': ['eth0', 'eth1', 'eth3']}
    device_info2 = {'device_name': 'Device1',
                    'os_type': 'IOS-XR',
                    'ip_address': '10.30.30.2',
                    'interfaces': ['eth0', 'eth1', 'eth3']}
    device_info3 = {'device_name': 'Device1',
                    'os_type': 'IOS-XR',
                    'ip_address': '10.30.30.3',
                    'interfaces': ['eth0', 'eth1', 'eth3']}
    devices_info = [device_info1, device_info2, device_info3]

    db_path = "./network.db"

    print("\n").strip()
    print("Creating 'Devices' Table")
    print("\n").strip()
    db_create_device_table(db_path)
    db_dump_table(db_path, 'Devices')
    print("\n").strip()

    print("Adding records to the 'Devices' Table")
    print("\n").strip()
    for item in devices_info:
        db_insert_device_record(db_path, item)
    db_dump_table(db_path, 'Devices')
    print("\n").strip()

    print("Removing records from the 'Devices' Table")
    print("\n").strip()
    for item in devices_info:
        db_delete_device_record(db_path, item['device_name'])
    db_dump_table(db_path, 'Devices')
    print("\n").strip()
