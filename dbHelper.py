# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 08:15:35 2018

@author: vishnu.kv
"""     
import sqlite3

class DBHelper:
    def __init__(self,dbname="todo.sqlite"):
        self.dbName=dbname
        self.conn=sqlite3.connect(dbname)
        self.setup()
    def setup(self):
        stmt = "CREATE TABLE IF NOT EXISTS items (description text)"
        self.conn.execute(stmt)
        self.conn.commit()
    
    def  addItems(self,itemsText):
        stmt = "INSERT INTO items (description) VALUES (?)"
        args = (itemsText, )
        self.conn.execute(stmt, args)
        self.conn.commit()
        
        
    def deleteItems(self, itemsText):
        stmt = "DELETE FROM items WHERE description = (?)"
        args = (itemsText,)
        self.conn.execute(stmt, args)
        self.conn.commit()
        
    def get_items(self):
        stmt = "SELECT description FROM items "
        return [x[0] for x in self.conn.execute(stmt)]     
        