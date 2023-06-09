# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 19:45:31 2023

@author: ryan8
"""

import sqlite3

# 建立資料庫連線
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# 建立資料表
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        JID TEXT,
        claim TEXT,
        claim_summary TEXT,
        judge_summary TEXT,
        law_summary TEXT,
        result TEXT
    )
''')

# 插入範例資料
cursor.execute("INSERT INTO users (JID, claim, claim_summary, judge_summary, law_summary, result) VALUES ('TEST01', '我是原告主張', '我是原告主張摘要','我是判決理由摘要','第一項第一款', '敗訴')")
cursor.execute("INSERT INTO users (JID, claim, claim_summary, judge_summary, law_summary, result) VALUES ('TEST02', '我是原告主張', '我是原告主張摘要','我是判決理由摘要','第一項第一款', '敗訴')")
cursor.execute("INSERT INTO users (JID, claim, claim_summary, judge_summary, law_summary, result) VALUES ('TEST03', '我是原告主張', '我是原告主張摘要','我是判決理由摘要','第一項第一款', '敗訴')")

# 儲存變更
conn.commit()

# 關閉資料庫連線
conn.close()
