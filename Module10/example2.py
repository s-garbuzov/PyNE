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

# third-party modules
import json


class Device(object):
    """Class representing a network device."""

    def __init__(self, name=None, os_type=None, ip_addr=None, iflist=None):
        """The constructor of the class instance."""
        self.name = name
        self.os_type = os_type
        self.ip_addr = ip_addr
        self.iflist = iflist

    def toJSON(self):
        """Converts instance object to JSON."""
        return json.dumps(self, default=lambda o: o.__dict__)


def print_device_info(device):
    """Prints information about given object instance of the Device class."""
    assert(isinstance(device, Device))
    print(" Device Name : %s" % device.name)
    print(" OS Type     : %s" % device.os_type)
    print(" IP Address  : %s" % device.ip_addr)
    print(" Interfaces  : %s" % ", ".join(device.iflist))


def db_create_devices_table(db_path):
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
            # The 'name' and 'info' are the column names for each row to be
            # created in the table. PRIMARY KEY constraint uniquely identifies
            # each row/record in a database table, primary key column cannot
            # have NULL values.
            sql = ("CREATE TABLE IF NOT EXISTS Devices"
                   "(name TEXT PRIMARY KEY NOT NULL,"
                   "info TEXT)")
            cursor.execute(sql)
    except (db.OperationalError) as e:
        print("!!!Error, %s" % repr(e))


def db_add_device_record(db_path, rec_name, rec_info):
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
            tup = (rec_name, rec_info)
            sql = ("REPLACE INTO Devices VALUES (?,?)")
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
            sql = ("SELECT info FROM Devices WHERE name=?")
            cursor.execute(sql, (rec_name,))
            rec = cursor.fetchone()
            return rec[0]
    except (db.OperationalError) as e:
        print("!!!Error, %s" % repr(e))


def db_delete_device_record(db_path, rec_name):
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
            # Prepare and execute SQL statement (make sure the 'record_name'
            # parameter follows with comma to make it a tuple)
            sql = "DELETE FROM Devices WHERE name=?"
            cursor.execute(sql, (rec_name,))
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

    db_path = "./example2.db"
    device1 = Device(name='Router1', os_type='IOS-XR',
                     ip_addr='10.30.30.1',
                     iflist=['Lo0', 'Mg0/0/CPU0/0',
                             'Gi0/0/0/0', 'Gi0/0/0/1',
                             'Gi0/0/0/2', 'Gi0/0/0/3'])
    device2 = Device(name='Router2', os_type='IOS-XR',
                     ip_addr='10.30.30.2',
                     iflist=['Lo0', 'Mg0/0/CPU0/0',
                             'Gi0/0/0/0', 'Gi0/0/0/1',
                             'Gi0/0/0/2', 'Gi0/0/0/3'])
    device3 = Device(name='Router3', os_type='IOS-XR',
                     ip_addr='10.30.30.3',
                     iflist=['Lo0', 'Mg0/0/CPU0/0',
                             'Gi0/0/0/0', 'Gi0/0/0/1',
                             'Gi0/0/0/2', 'Gi0/0/0/3'])
    devices = [device1, device2, device3]

    print("\n").strip()
    print("Creating 'Devices' Table")
    print("\n").strip()
    db_create_devices_table(db_path)
    db_print_table_rows_cnt(db_path, 'Devices')
    print("\n").strip()

    print("Adding records to the 'Devices' Table")
    print("\n").strip()
    for item in devices:
        db_add_device_record(db_path, rec_name=item.name,
                             rec_info=item.toJSON())
    db_print_table_rows_cnt(db_path, 'Devices')
    print("\n").strip()

    print("Searching for the records in the 'Devices' Table")
    print("\n").strip()
    for item in devices:
        rec_name = item.name
        js = db_get_device_info(db_path, rec_name)
        d = json.loads(js)
        device = Device(**d)
        print("%s" % ('<' * 78))
        print_device_info(device)
        print("%s" % ('>' * 78))
    print("\n").strip()

    print("Removing records from the 'Devices' Table")
    print("\n").strip()
    for item in devices:
        db_delete_device_record(db_path, item.name)
    db_print_table_rows_cnt(db_path, 'Devices')
    print("\n").strip()
