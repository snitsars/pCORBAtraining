import sqlite3

class Storage:
  def __init__(self, filename):
    self._connection = sqlite3.connect(filename) 
    self._cursor = self._connection.cursor()

    command = "create table if not exists storage (namespace text not null, key text not null, value text, ts datetime default current_timestamp, primary key (namespace, key))"
    self._cursor.execute(command)
    self._connection.commit()

  def put(self, namespace, key, value):
    command = "insert or replace into storage values ('%s', '%s', '%s')" % (namespace, key, value)
    self._cursor.execute(command)
    self._connection.commit()

  def get(self, namespace, key):
    command = "select value from storage where namespace = '%s' and key = '%s'" % (namespace, key)
    self._cursor.execute(command)
    result = self._cursor.fetchone()
    return result[0] if result else None