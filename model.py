# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 18:42:40 2023

@author: ryan8
"""

import sqlite3

# 建立資料庫連線
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

#處理判決結果
def law_result(result):
    law = []
    law.append(f"判決適用第{result[0][3]}項")
    law.append(f"第{result[0][4]}款") if result[0][4] != 0 else None
    law.append("判決結果為成功") if result[0][5] == 1 else result.append("判決結果為失敗")
    return ", ".join(law)

# 執行搜尋
def process_user_input(user_input):
    cursor.execute("SELECT * FROM law_table WHERE JID = '{user_input}'")
    qresult = cursor.fetchone()  # 只取回一筆結果
    
    string_result = f"""
                    1. JID: {result[1]}

                    2. 原告主張摘要: {qresult1[0][1]}
                    
                    3. 判決理由摘要: {qresult1[0][2]}
                    
                    4. 判決結果: {law_result(qresult1)}
                    """

    return string_result
