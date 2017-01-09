# Radon
# Created by Xinyu Chen <xinyu@evestemptation.com>

# Database Installation
# This script creates table structures in the database and then populate certain tables use the configure data in the
# config module

import sqlite3
import config

sql_tables = [
    '''CREATE TABLE IF NOT EXISTS `url_stats` (
        `id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        `url`	TEXT NOT NULL UNIQUE,
        `rate`	INTEGER NOT NULL
    )''',
    '''CREATE TABLE IF NOT EXISTS `abnormal_request` (
        `id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        `timestamp`	NUMERIC NOT NULL,
        `host`	TEXT,
        `method`	TEXT,
        `status`	INTEGER,
        `url`	TEXT,
        `referer`	TEXT,
        `agent`	TEXT
    )''',
    '''CREATE TABLE IF NOT EXISTS  `url_ignore_list` (
        `id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        `pattern`	TEXT NOT NULL UNIQUE
    )''',
    '''CREATE TABLE IF NOT EXISTS `agent_ignore_list` (
        `id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        `keyword`	TEXT NOT NULL UNIQUE,
        `description`   TEXT
    )''',
    '''CREATE TABLE IF NOT EXISTS  `cacheable_param` (
        `id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        `param`	TEXT NOT NULL UNIQUE
    )''',
    '''CREATE TABLE IF NOT EXISTS  `host_ignore_list` (
        `id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        `host`	TEXT NOT NULL UNIQUE,
        `description`   TEXT
    )''',
    '''CREATE TABLE IF NOT EXISTS  `email_recipients` (
        `id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        `email`	TEXT NOT NULL UNIQUE,
        `name`	TEXT
    );'''
]


conn = sqlite3.connect(config.database_file)
c = conn.cursor()

for sql in sql_tables:
    c.execute(sql)
conn.commit()

sql_url_ignore = 'INSERT OR IGNORE INTO `url_ignore_list`' \
             '(pattern) VALUES (?)'
for pattern in config.url_ignore_list:
    c.execute(sql_url_ignore, (pattern,))
conn.commit()

sql_agent_ignore = 'INSERT OR IGNORE INTO `agent_ignore_list`' \
                   '(keyword, description) VALUES (?, ?)'
for agent in config.agent_ignore_list:
    c.execute(sql_agent_ignore, (agent[0], agent[1]))
conn.commit()

sql_cacheable_param = 'INSERT OR IGNORE INTO `cacheable_param`' \
                      '(param) VALUES (?)'
for param in config.cacheable_param:
    c.execute(sql_cacheable_param, (param,))
conn.commit()

sql_host_ignore = 'INSERT OR IGNORE INTO `host_ignore_list`' \
                  '(host, description) VALUES (?, ?)'
for param in config.host_ignore_list:
    c.execute(sql_host_ignore, (param[0], param[1]))
conn.commit()

sql_agent_mock = 'INSERT INTO `agent_ignore_list`' \
                 '(id, keyword, description) VALUES (?, ?, ?)'
try:
    c.execute(sql_agent_mock, (1, 'http://www.google.com/bot.html', 'Googlebot'))
    conn.commit()
except:
    # idempotence, do nothing here
    print('')
print('Database installation completed.')
