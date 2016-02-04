import sqlite3

class Storage:
  def __init__(self, filename):
    self._connection = sqlite3.connect(filename) 
    self._cursor = self._connection.cursor()

    commands = [
      "create table if not exists storage (namespace text not null, key text not null, value text, ts datetime default current_timestamp, primary key (namespace, key))",
      "create table if not exists favorites (user_id integer not null, listing_id integer, ts datetime default current_timestamp)",
      "create table if not exists api_calls (func text, ts datetime default current_timestamp)",
      "create table if not exists tags (iteration integer, listing_id integer, tag text)",
      #"create table if not exists tags (iteration integer, listing_id integer, tag text)",


      "create index if not exists idx_favorites_ts on favorites(ts)",
      "create index if not exists idx_tags_iteration on tags(iteration)",
      "create index if not exists idx_tags_listing_id on tags(listing_id)"
    ]

    for command in commands:
      self._cursor.execute(command)
      self._connection.commit()


  def api_call(self, func): 
    command = "insert into api_calls(func) values ('%s')" % func
    self._cursor.execute(command)
    self._connection.commit()

  def get_api_calls_count(self, start, duration):
    command = "select strftime('%%d/%%m %%H:00', 'now', '-%s hours', '+3 hours'), count(*) from api_calls where ts between strftime('%%Y-%%m-%%d %%H:00', 'now', '-%s hours') and strftime('%%Y-%%m-%%d %%H:00', 'now', '-%s hours')" % (start+2, start+duration, start)
    self._cursor.execute(command)
    result = self._cursor.fetchone()
    return result if result else None

  def put(self, namespace, key, value):
    command = "insert or replace into storage(namespace, key, value) values ('%s', '%s', '%s')" % (namespace, key, value)
    self._cursor.execute(command)
    self._connection.commit()

  def get(self, namespace, key):
    command = "select value from storage where namespace = '%s' and key = '%s'" % (namespace, key)
    self._cursor.execute(command)
    result = self._cursor.fetchone()
    return result[0] if result else None

  def get_last(self, namespace, key, period):
    command = "select value from storage where namespace = '%s' and key = '%s' and ts > datetime('now', '-%s')" % (namespace, key, period)
    self._cursor.execute(command)
    result = self._cursor.fetchall()
    return result if result else []

  def put_favorite(self, user_id, listing_id, ts=None):
    if ts != None:
      command = "insert into favorites(user_id, listing_id, ts) values (%s, %s, datetime('%s', 'unixepoch'))" % (user_id, listing_id, ts)
    else:
      command = "insert into favorites(user_id, listing_id) values (%s, %s)" % (user_id, listing_id)

    self._cursor.execute(command)
    self._connection.commit()

  def get_tags_iteration(self, namespace, key):
    command = "select max(iteration) from tags"
    self._cursor.execute(command)
    result = self._cursor.fetchone()
    return result[0] if result else None

  def put_tags(self, iteration, listing_id, tags):
    if tags and len(tags)>0:
      command = "insert into tags values %s" % ", ".join(["(%s, %s, '%s')" % (iteration, listing_id, tag) for tag in tags])
      print command
      self._cursor.execute(command)
      self._connection.commit()

  def get_last_favorite_users(self, period):
    command = "select distinct user_id from favorites where ts > datetime('now', '-%s')" % period
    self._cursor.execute(command)
    result = self._cursor.fetchall()
    return [x[0] for x in result]

  def get_favorite_listings(self):
    command = "select distinct listing_id from favorites"
    self._cursor.execute(command)
    result = self._cursor.fetchall()
    return [x[0] for x in result]

  def get_favorite_listings_for_user(self, user_id):
    command = "select distinct listing_id from favorites where user_id = '%s'" % user_id
    self._cursor.execute(command)
    result = self._cursor.fetchall()
    return [x[0] for x in result]

  def _test(self):
    command = "select datetime('now')"
    self._cursor.execute(command)
    result = self._cursor.fetchone()
    return result[0] if result else None
    
  def _upgrade(self):
    command = "create table if not exists favoritesold (user_id text not null, listing_id text, ts datetime default current_timestamp)"
    print command
    self._cursor = self._connection.cursor()
    self._cursor.execute(command)
    self._connection.commit()

    command = "insert into favoritesold (user_id, listing_id, ts) select * from favorites"
    print command
    self._cursor = self._connection.cursor()
    self._cursor.execute(command)
    self._connection.commit()

    command = "drop table favorites"
    print command
    self._cursor = self._connection.cursor()
    self._cursor.execute(command)
    self._connection.commit()

    command = "create table if not exists favorites (user_id integer not null, listing_id integer, ts datetime default current_timestamp)"
    print command
    self._cursor = self._connection.cursor()
    self._cursor.execute(command)
    self._connection.commit()

    command = "insert into favorites (user_id, listing_id, ts) select cast(user_id as integer), cast(listing_id as integer), ts from favoritesold"
    print command
    self._cursor = self._connection.cursor()
    self._cursor.execute(command)
    self._connection.commit()

    command = "drop table favoritesold"
    print command
    self._cursor = self._connection.cursor()
    self._cursor.execute(command)
    self._connection.commit()
