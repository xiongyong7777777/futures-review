import sqlite3
import os

class DataModel:
    def __init__(self):
        self.db_path = 'futures_review.db'
        self._create_tables()
    
    def _create_tables(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建交易记录表格
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            direction TEXT NOT NULL,
            open_time TEXT NOT NULL,
            open_cycle INTEGER NOT NULL,
            open_boundary_ma TEXT NOT NULL,
            target_boundary_ma TEXT NOT NULL,
            drive_strategy TEXT NOT NULL,
            entry_mode TEXT NOT NULL,
            entry_signal TEXT NOT NULL,
            stop_loss_rule TEXT NOT NULL,
            take_profit_rule TEXT NOT NULL,
            open_emotion TEXT NOT NULL,
            open_price REAL NOT NULL,
            drawdown REAL NOT NULL,
            add_price REAL NOT NULL,
            add_price1 REAL NOT NULL,
            reduce_price REAL NOT NULL,
            reduce_price1 REAL NOT NULL,
            close_cycle INTEGER NOT NULL,
            close_time TEXT NOT NULL,
            close_boundary_ma TEXT NOT NULL,
            exit_signal TEXT NOT NULL,
            close_emotion TEXT NOT NULL,
            close_price REAL NOT NULL,
            profit_loss REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        conn.commit()
        conn.close()
    
    def insert_trade(self, trade_data):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 计算盈亏
        pl = round(trade_data['reduce_price'], 2) + round(trade_data['reduce_price1'], 2) + round(trade_data['close_price'], 2) - \
             round(trade_data['open_price'], 2) - round(trade_data['add_price'], 2) - round(trade_data['add_price1'], 2)
        
        cursor.execute('''
        INSERT INTO trades (
            symbol, direction, open_time, open_cycle, open_boundary_ma, target_boundary_ma, 
            drive_strategy, entry_mode, entry_signal, stop_loss_rule, take_profit_rule, 
            open_emotion, open_price, drawdown, add_price, add_price1, reduce_price, reduce_price1, 
            close_cycle, close_time, close_boundary_ma, exit_signal, close_emotion, close_price, profit_loss
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            trade_data['symbol'], trade_data['direction'], trade_data['open_time'], trade_data['open_cycle'],
            trade_data['open_boundary_ma'], trade_data['target_boundary_ma'], trade_data['drive_strategy'],
            trade_data['entry_mode'], trade_data['entry_signal'], trade_data['stop_loss_rule'],
            trade_data['take_profit_rule'], trade_data['open_emotion'], trade_data['open_price'],
            trade_data['drawdown'], trade_data['add_price'], trade_data['add_price1'],
            trade_data['reduce_price'], trade_data['reduce_price1'], trade_data['close_cycle'],
            trade_data['close_time'], trade_data['close_boundary_ma'], trade_data['exit_signal'],
            trade_data['close_emotion'], trade_data['close_price'], pl
        ))
        
        conn.commit()
        conn.close()
        return pl
    
    def get_all_trades(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM trades')
        trades = cursor.fetchall()
        conn.close()
        return trades
    
    def get_trades_by_symbol(self, symbol):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM trades WHERE symbol = ?', (symbol,))
        trades = cursor.fetchall()
        conn.close()
        return trades
    
    def get_summary_by_symbol(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 使用SQL查询直接汇总数据
        cursor.execute('''
        SELECT 
            symbol, 
            COUNT(*) as total_trades, 
            SUM(profit_loss) as total_profit_loss,
            SUM(CASE WHEN profit_loss > 0 THEN 1 ELSE 0 END) as winning_trades,
            SUM(CASE WHEN profit_loss < 0 THEN 1 ELSE 0 END) as losing_trades
        FROM trades 
        GROUP BY symbol
        ''')
        
        summary = cursor.fetchall()
        conn.close()
        return summary
    
    def get_symbols(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT symbol FROM trades ORDER BY symbol')
        symbols = [row[0] for row in cursor.fetchall()]
        conn.close()
        return symbols