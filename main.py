import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.spinner import Spinner

from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.graphics import Color, Rectangle
import sqlite3
import os
from datetime import datetime
import matplotlib.pyplot as plt
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

kivy.require('2.1.0')

class DataEntryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def get_varieties(self):
        conn = sqlite3.connect('futures_review.db')
        c = conn.cursor()
        c.execute('SELECT DISTINCT variety FROM trades')
        varieties = [row[0] for row in c.fetchall()]
        conn.close()
        return ['全部'] + varieties
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 标题
        title = Label(text='期货复盘数据录入', font_size='24sp', size_hint_y=None, height=50)
        layout.add_widget(title)
        
        # 滚动视图
        scroll = ScrollView()
        form = GridLayout(cols=2, spacing=10, size_hint_y=None)
        form.bind(minimum_height=form.setter('height'))
        
        # 品种
        form.add_widget(Label(text='品种:'))
        self.variety = TextInput(multiline=False)
        form.add_widget(self.variety)
        
        # 品种选择器（用于后续扩展，当前未使用）
        self.variety_spinner = Spinner(text='全部', values=self.get_varieties())
        # form.add_widget(self.variety_spinner)  # 暂时隐藏，可根据需要取消注释
        
        # 交易方向
        form.add_widget(Label(text='交易方向:'))
        direction_layout = BoxLayout(orientation='horizontal', spacing=10)
        self.direction = StringProperty('多')
        long_btn = Button(text='多', on_press=lambda x: setattr(self, 'direction', '多'))
        short_btn = Button(text='空', on_press=lambda x: setattr(self, 'direction', '空'))
        direction_layout.add_widget(long_btn)
        direction_layout.add_widget(short_btn)
        form.add_widget(direction_layout)
        
        # 开仓时间
        form.add_widget(Label(text='开仓时间:'))
        self.open_time = TextInput(multiline=False, hint_text='XXXX年XX月XX日XX时XX分')
        form.add_widget(self.open_time)
        
        # 开仓操作周期
        form.add_widget(Label(text='开仓操作周期:'))
        self.open_cycle = TextInput(multiline=False, input_filter='int')
        form.add_widget(self.open_cycle)
        
        # 开仓起始边界均线
        form.add_widget(Label(text='开仓起始边界均线:'))
        self.open_start_ma = TextInput(multiline=False, input_filter='int')
        form.add_widget(self.open_start_ma)
        
        # 预期目标边界均线
        form.add_widget(Label(text='预期目标边界均线:'))
        self.target_ma = TextInput(multiline=False, input_filter='int')
        form.add_widget(self.target_ma)
        
        # 驱动策略
        form.add_widget(Label(text='驱动策略:'))
        self.drive_strategy = TextInput(multiline=False)
        form.add_widget(self.drive_strategy)
        
        # 入场模式
        form.add_widget(Label(text='入场模式:'))
        self.entry_mode = TextInput(multiline=False)
        form.add_widget(self.entry_mode)
        
        # 入场信号
        form.add_widget(Label(text='入场信号:'))
        self.entry_signal = TextInput(multiline=False)
        form.add_widget(self.entry_signal)
        
        # 自损规则
        form.add_widget(Label(text='自损规则:'))
        self.stop_loss_rule = TextInput(multiline=False)
        form.add_widget(self.stop_loss_rule)
        
        # 止盈规则
        form.add_widget(Label(text='止盈规则:'))
        self.take_profit_rule = TextInput(multiline=False)
        form.add_widget(self.take_profit_rule)
        
        # 开仓情绪
        form.add_widget(Label(text='开仓情绪:'))
        self.open_emotion = TextInput(multiline=False)
        form.add_widget(self.open_emotion)
        
        # 开仓价格
        form.add_widget(Label(text='开仓价格:'))
        self.open_price = TextInput(multiline=False, input_filter='float', hint_text='带两位小数')
        form.add_widget(self.open_price)
        
        # 回撤幅度
        form.add_widget(Label(text='回撤幅度:'))
        self.drawdown = TextInput(multiline=False, input_filter='float', hint_text='带两位小数')
        form.add_widget(self.drawdown)
        
        # 增仓价格
        form.add_widget(Label(text='增仓价格:'))
        self.add_price = TextInput(multiline=False, input_filter='float', hint_text='带两位小数')
        form.add_widget(self.add_price)
        
        # 增仓价格1
        form.add_widget(Label(text='增仓价格1:'))
        self.add_price1 = TextInput(multiline=False, input_filter='float', hint_text='带两位小数')
        form.add_widget(self.add_price1)
        
        # 减仓价格
        form.add_widget(Label(text='减仓价格:'))
        self.reduce_price = TextInput(multiline=False, input_filter='float', hint_text='带两位小数')
        form.add_widget(self.reduce_price)
        
        # 减仓价格1
        form.add_widget(Label(text='减仓价格1:'))
        self.reduce_price1 = TextInput(multiline=False, input_filter='float', hint_text='带两位小数')
        form.add_widget(self.reduce_price1)
        
        # 平仓操作周期
        form.add_widget(Label(text='平仓操作周期:'))
        self.close_cycle = TextInput(multiline=False, input_filter='int')
        form.add_widget(self.close_cycle)
        
        # 平仓时间
        form.add_widget(Label(text='平仓时间:'))
        self.close_time = TextInput(multiline=False, hint_text='XXXX年XX月XX日XX时XX分')
        form.add_widget(self.close_time)
        
        # 平仓边界均线
        form.add_widget(Label(text='平仓边界均线:'))
        self.close_ma = TextInput(multiline=False, input_filter='int')
        form.add_widget(self.close_ma)
        
        # 离场信号
        form.add_widget(Label(text='离场信号:'))
        self.exit_signal = TextInput(multiline=False)
        form.add_widget(self.exit_signal)
        
        # 平仓情绪
        form.add_widget(Label(text='平仓情绪:'))
        self.close_emotion = TextInput(multiline=False)
        form.add_widget(self.close_emotion)
        
        # 平仓价格
        form.add_widget(Label(text='平仓价格:'))
        self.close_price = TextInput(multiline=False, input_filter='float', hint_text='带两位小数')
        form.add_widget(self.close_price)
        
        scroll.add_widget(form)
        layout.add_widget(scroll)
        
        # 保存按钮
        save_btn = Button(text='保存数据', size_hint_y=None, height=50, on_press=self.save_data)
        layout.add_widget(save_btn)
        
        # 切换到分析界面按钮
        analyze_btn = Button(text='数据分析', size_hint_y=None, height=50, on_press=self.switch_to_analyze)
        layout.add_widget(analyze_btn)
        
        self.add_widget(layout)
    
    def save_data(self, instance):
        conn = sqlite3.connect('futures_review.db')
        c = conn.cursor()
        
        # 创建表
        c.execute('''CREATE TABLE IF NOT EXISTS trades
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      variety TEXT,
                      direction TEXT,
                      open_time TEXT,
                      open_cycle INTEGER,
                      open_start_ma INTEGER,
                      target_ma INTEGER,
                      drive_strategy TEXT,
                      entry_mode TEXT,
                      entry_signal TEXT,
                      stop_loss_rule TEXT,
                      take_profit_rule TEXT,
                      open_emotion TEXT,
                      open_price REAL,
                      drawdown REAL,
                      add_price REAL,
                      add_price1 REAL,
                      reduce_price REAL,
                      reduce_price1 REAL,
                      close_cycle INTEGER,
                      close_time TEXT,
                      close_ma INTEGER,
                      exit_signal TEXT,
                      close_emotion TEXT,
                      close_price REAL)''')
        
        # 插入数据
        c.execute('''INSERT INTO trades (variety, direction, open_time, open_cycle, open_start_ma, target_ma, 
                                         drive_strategy, entry_mode, entry_signal, stop_loss_rule, take_profit_rule, 
                                         open_emotion, open_price, drawdown, add_price, add_price1, reduce_price, 
                                         reduce_price1, close_cycle, close_time, close_ma, exit_signal, close_emotion, 
                                         close_price)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (self.variety.text,
                   self.direction,
                   self.open_time.text,
                   int(self.open_cycle.text) if self.open_cycle.text else None,
                   int(self.open_start_ma.text) if self.open_start_ma.text else None,
                   int(self.target_ma.text) if self.target_ma.text else None,
                   self.drive_strategy.text,
                   self.entry_mode.text,
                   self.entry_signal.text,
                   self.stop_loss_rule.text,
                   self.take_profit_rule.text,
                   self.open_emotion.text,
                   float(self.open_price.text) if self.open_price.text else None,
                   float(self.drawdown.text) if self.drawdown.text else None,
                   float(self.add_price.text) if self.add_price.text else None,
                   float(self.add_price1.text) if self.add_price1.text else None,
                   float(self.reduce_price.text) if self.reduce_price.text else None,
                   float(self.reduce_price1.text) if self.reduce_price1.text else None,
                   int(self.close_cycle.text) if self.close_cycle.text else None,
                   self.close_time.text,
                   int(self.close_ma.text) if self.close_ma.text else None,
                   self.exit_signal.text,
                   self.close_emotion.text,
                   float(self.close_price.text) if self.close_price.text else None))
        
        conn.commit()
        conn.close()
        
        # 清空表单
        self.variety.text = ''
        self.direction = '多'
        self.open_time.text = ''
        self.open_cycle.text = ''
        self.open_start_ma.text = ''
        self.target_ma.text = ''
        self.drive_strategy.text = ''
        self.entry_mode.text = ''
        self.entry_signal.text = ''
        self.stop_loss_rule.text = ''
        self.take_profit_rule.text = ''
        self.open_emotion.text = ''
        self.open_price.text = ''
        self.drawdown.text = ''
        self.add_price.text = ''
        self.add_price1.text = ''
        self.reduce_price.text = ''
        self.reduce_price1.text = ''
        self.close_cycle.text = ''
        self.close_time.text = ''
        self.close_ma.text = ''
        self.exit_signal.text = ''
        self.close_emotion.text = ''
        self.close_price.text = ''
    
    def switch_to_analyze(self, instance):
        self.manager.current = 'analyze'

class DataAnalyzeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 标题
        title = Label(text='期货复盘数据分析', font_size='24sp', size_hint_y=None, height=50)
        layout.add_widget(title)
        
        # 品种选择
        variety_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        variety_layout.add_widget(Label(text='选择品种:'))
        self.variety_spinner = Spinner(text='全部', values=self.get_varieties(), on_text=self.update_analysis)
        variety_layout.add_widget(self.variety_spinner)
        layout.add_widget(variety_layout)
        
        # 分析结果
        self.result_layout = BoxLayout(orientation='vertical', spacing=10)
        layout.add_widget(self.result_layout)
        
        # 图表区域
        self.chart_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=2)
        layout.add_widget(self.chart_layout)
        
        # 返回按钮
        back_btn = Button(text='返回数据录入', size_hint_y=None, height=50, on_press=self.switch_to_entry)
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
        self.update_analysis(None)
    
    def get_varieties(self):
        conn = sqlite3.connect('futures_review.db')
        c = conn.cursor()
        c.execute('SELECT DISTINCT variety FROM trades')
        varieties = [row[0] for row in c.fetchall()]
        conn.close()
        return ['全部'] + varieties
    
    def calculate_profit(self, row):
        open_price = row[13] or 0
        add_price = row[15] or 0
        add_price1 = row[16] or 0
        reduce_price = row[17] or 0
        reduce_price1 = row[18] or 0
        close_price = row[24] or 0
        return reduce_price + reduce_price1 + close_price - open_price - add_price - add_price1
    
    def update_analysis(self, instance):
        # 清空之前的结果和图表
        self.result_layout.clear_widgets()
        self.chart_layout.clear_widgets()
        
        conn = sqlite3.connect('futures_review.db')
        c = conn.cursor()
        
        # 查询数据
        variety = self.variety_spinner.text
        if variety == '全部':
            c.execute('SELECT * FROM trades')
        else:
            c.execute('SELECT * FROM trades WHERE variety=?', (variety,))
        
        trades = c.fetchall()
        
        # 计算每个交易的盈亏
        trade_results = []
        for trade in trades:
            profit = self.calculate_profit(trade)
            trade_results.append((trade[1], profit))
        
        # 计算总盈亏和胜率
        total_profit = sum(p for v, p in trade_results)
        win_count = sum(1 for v, p in trade_results if p > 0)
        lose_count = sum(1 for v, p in trade_results if p < 0)
        win_rate = (win_count / lose_count * 100) if lose_count > 0 else 0
        
        # 按品种汇总
        variety_profits = {}
        for v, p in trade_results:
            if v not in variety_profits:
                variety_profits[v] = {'total': 0, 'win': 0, 'lose': 0}
            variety_profits[v]['total'] += p
            if p > 0:
                variety_profits[v]['win'] += 1
            elif p < 0:
                variety_profits[v]['lose'] += 1
        
        # 显示结果
        for v in variety_profits:
            v_total = variety_profits[v]['total']
            v_win = variety_profits[v]['win']
            v_lose = variety_profits[v]['lose']
            v_win_rate = (v_win / v_lose * 100) if v_lose > 0 else 0
            
            result_box = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=40)
            result_box.add_widget(Label(text=f'品种: {v}'))
            result_box.add_widget(Label(text=f'总盈亏: {v_total:.2f}'))
            result_box.add_widget(Label(text=f'胜率: {v_win_rate:.2f}%'))
            self.result_layout.add_widget(result_box)
        
        # 显示总结果
        total_box = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=40)
        total_box.add_widget(Label(text='总盈亏:', font_size='16sp', bold=True))
        total_box.add_widget(Label(text=f'{total_profit:.2f}', font_size='16sp', bold=True))
        total_box.add_widget(Label(text='总胜率:', font_size='16sp', bold=True))
        total_box.add_widget(Label(text=f'{win_rate:.2f}%', font_size='16sp', bold=True))
        self.result_layout.add_widget(total_box)
        
        # 生成图表
        self.generate_charts(variety_profits)
        
        conn.close()
    
    def generate_charts(self, variety_profits):
        # 总盈亏图表
        fig1, ax1 = plt.subplots(figsize=(8, 4))
        varieties = list(variety_profits.keys())
        profits = [v['total'] for v in variety_profits.values()]
        
        ax1.bar(varieties, profits, color=['green' if p > 0 else 'red' for p in profits])
        ax1.set_title('各品种总盈亏')
        ax1.set_xlabel('品种')
        ax1.set_ylabel('总盈亏')
        ax1.tick_params(axis='x', rotation=45)
        
        # 胜率图表
        fig2, ax2 = plt.subplots(figsize=(8, 4))
        win_rates = [(v['win'] / v['lose'] * 100) if v['lose'] > 0 else 0 for v in variety_profits.values()]
        
        ax2.bar(varieties, win_rates, color='blue')
        ax2.set_title('各品种胜率')
        ax2.set_xlabel('品种')
        ax2.set_ylabel('胜率(%)')
        ax2.tick_params(axis='x', rotation=45)
        
        # 添加图表到界面
        canvas1 = FigureCanvasKivyAgg(fig1)
        canvas2 = FigureCanvasKivyAgg(fig2)
        
        self.chart_layout.add_widget(canvas1)
        self.chart_layout.add_widget(canvas2)
    
    def switch_to_entry(self, instance):
        self.manager.current = 'entry'
        # 刷新品种列表
        self.manager.get_screen('entry').variety_spinner.values = self.manager.get_screen('entry').get_varieties()

class FuturesReviewApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(DataEntryScreen(name='entry'))
        sm.add_widget(DataAnalyzeScreen(name='analyze'))
        return sm

if __name__ == '__main__':
    FuturesReviewApp().run()

# Remove this line (it's not being used):
from kivy.uix.datepicker import DatePicker
