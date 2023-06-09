# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 18:42:40 2023

@author: ryan8
"""

import sqlite3

# 建立資料庫連線
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# 執行搜尋

def process_user_input(user_input):
    cursor.execute(f"SELECT * FROM users WHERE JID = '{user_input}'")
    result = cursor.fetchone()  # 只取回一筆結果
    
    string_result = f"""
                    JID: {result[1]}
                    主張摘要: {result[3]}
                    判決理由摘要: {result[4]}
                    項款: {result[5]}
                    結果: {result[6]}
                    """

    return string_result
