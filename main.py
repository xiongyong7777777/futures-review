from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.resources import resource_find
from data_model import DataModel
import os
import sys

# 尝试多种字体路径，确保找到支持中文的字体
def get_font_path():
    # 尝试系统字体目录
    font_paths = []
    
    # 检测是否为Android环境
    is_android = 'ANDROID_ROOT' in os.environ
    
    if is_android:
        # Android系统字体路径
        font_paths.extend([
            '/system/fonts/DroidSansFallback.ttf',  # Android默认中文字体
            '/system/fonts/NotoSansSC-Regular.ttf',  #  noto字体
            '/system/fonts/NotoSansCJK-Regular.ttc',  # CJK字体
        ])
    else:
        # Windows系统字体
        font_paths.extend([
            os.path.join(os.environ.get('WINDIR', 'C:\Windows'), 'Fonts', 'msyh.ttf'),  # 微软雅黑
            os.path.join(os.environ.get('WINDIR', 'C:\Windows'), 'Fonts', 'simsun.ttc'),  # 宋体
        ])
    
    # 通用字体路径
    font_paths.extend([
        # Kivy内置字体
        resource_find('fonts/Roboto-Regular.ttf'),
        # 相对路径
        'msyh.ttf',
        'simsun.ttc',
        'DroidSansFallback.ttf'
    ])
    
    for path in font_paths:
        if path and os.path.exists(path):
            return path
    return None

# 获取可用的字体路径
font_path = get_font_path()

# 设置中文字体
if font_path:
    LabelBase.register(name='ChineseFont', fn_regular=font_path)
    # 设置默认字体
    Window.default_font = ['ChineseFont', font_path]
else:
    # 如果找不到字体，使用Kivy默认字体
    print("警告: 未找到支持中文的字体，可能会导致中文字符显示异常")
    LabelBase.register(name='Roboto', fn_regular=resource_find('fonts/Roboto-Regular.ttf'))
    Window.default_font = ['Roboto', 'Roboto-Regular.ttf']

# 加载Kivy语言定义
Builder.load_string('''
<MainScreen>:
    name: 'main'
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: '期货复盘APP'
            font_size: '24sp'
            size_hint_y: 0.1
            halign: 'center'
            valign: 'middle'
            font_name: 'ChineseFont'
        BoxLayout:
            orientation: 'horizontal'
            padding: 10
            spacing: 10
            Button:
                text: '数据录入'
                on_release: root.manager.current = 'input'
                font_name: 'ChineseFont'
            Button:
                text: '数据分析'
                on_release: root.manager.current = 'analysis'
                font_name: 'ChineseFont'
            Button:
                text: '图表分析'
                on_release: root.manager.current = 'charts'
                font_name: 'ChineseFont'

<InputScreen>:
    name: 'input'
    ScrollView:
        GridLayout:
            cols: 1
            spacing: 10
            padding: 10
            size_hint_y: None
            height: self.minimum_height
            
            # 基本信息
            Label:
                text: '基本信息'
                font_size: '20sp'
                size_hint_y: None
                height: 40
                font_name: 'ChineseFont'
            TextInput:
                id: symbol
                hint_text: '品种'
                size_hint_y: None
                height: 40
                font_name: 'ChineseFont'
            TextInput:
                id: direction
                hint_text: '交易方向'
                size_hint_y: None
                height: 40
                font_name: 'ChineseFont'
            TextInput:
                id: open_time
                hint_text: '开仓时间'
                size_hint_y: None
                height: 40
                font_name: 'ChineseFont'
            TextInput:
                id: open_cycle
                hint_text: '开仓操作周期（整数）'
                size_hint_y: None
                height: 40
                font_name: 'ChineseFont'
            TextInput:
                id: open_boundary_ma
                hint_text: '开仓起始边界均线'
                size_hint_y: None
                height: 40
                font_name: 'ChineseFont'
            TextInput:
                id: target_boundary_ma
                hint_text: '预期目标边界均线'
                size_hint_y: None
                height: 40
                font_name: 'ChineseFont'
            TextInput:
                id: drive_strategy
                hint_text: '驱动策略'
                size_hint_y: None
                height: 40
                font_name: 'ChineseFont'
            TextInput:
                id: entry_mode
                hint_text: '入场模式'
                size_hint_y: None
                height: 40
                font_name: 'ChineseFont'
            TextInput:
                id: entry_signal
                hint_text: '入场信号'
                size_hint_y: None
                height: 40
                font_name: 'ChineseFont'
            TextInput:
                id: stop_loss_rule
                hint_text: '止损规则'
                size_hint_y: None
                height: 40
                font_name: 'ChineseFont'
            TextInput:
                id: take_profit_rule
                hint_text: '止盈规则'
                size_hint_y: None
                height: 40
                font_name: 'ChineseFont'
            TextInput:
                id: open_emotion
                hint_text: '开仓情绪'
                size_hint_y: None
                height: 40
                font_name: 'ChineseFont'
            TextInput:
                id: open_price
                hint_text: '开仓价格'
                size_hint_y: None
                height: 40
                font_name: 'ChineseFont'
            TextInput:
                id: drawdown
                hint_text: '回撤幅度'
                size_hint_y: None
                height: 40
                font_name: 'ChineseFont'
            TextInput:
                id: add_price
                hint_text: '增仓价格'
                size_hint_y: None
                height: 40
                font_name: 'ChineseFont'
            TextInput:
                id: add_price1
                hint_text: '增仓价格1'
                size_hint_y: None
                height: 40
                font_name: 'ChineseFont'
            TextInput:
                id: reduce_price
                hint_text: '减仓价格'
                size_hint_y: None
                height: 40
                font_name: 'ChineseFont'
            TextInput:
                id: reduce_price1
                hint_text: '减仓价格1'
                size_hint_y: None
                height: 40
                font_name: 'ChineseFont'
            TextInput:
                id: close_cycle
                hint_text: '平仓操作周期'
                size_hint_y: None
                height: 40
                font_name: 'ChineseFont'
            TextInput:
                id: close_time
                hint_text: '平仓时间'
                size_hint_y: None
                height: 40
                font_name: 'ChineseFont'
            TextInput:
                id: close_boundary_ma
                hint_text: '平仓边界均线'
                size_hint_y: None
                height: 40
                font_name: 'ChineseFont'
            TextInput:
                id: exit_signal
                hint_text: '离场信号'
                size_hint_y: None
                height: 40
                font_name: 'ChineseFont'
            TextInput:
                id: close_emotion
                hint_text: '平仓情绪'
                size_hint_y: None
                height: 40
                font_name: 'ChineseFont'
            TextInput:
                id: close_price
                hint_text: '平仓价格'
                size_hint_y: None
                height: 40
                font_name: 'ChineseFont'
            
            Button:
                text: '提交数据'
                on_release: root.submit_data()
                size_hint_y: None
                height: 50
                font_name: 'ChineseFont'
            Button:
                text: '返回主页'
                on_release: root.manager.current = 'main'
                size_hint_y: None
                height: 50
                font_name: 'ChineseFont'

<AnalysisScreen>:
    name: 'analysis'
    ScrollView:
        GridLayout:
            cols: 1
            spacing: 10
            padding: 10
            size_hint_y: None
            height: self.minimum_height
            
            Label:
                text: '数据分析'
                font_size: '20sp'
                size_hint_y: None
                height: 40
                font_name: 'ChineseFont'
            
            BoxLayout:
                id: analysis_content
                orientation: 'vertical'
                spacing: 10
                size_hint_y: None
                height: self.minimum_height
            
            Button:
                text: '返回主页'
                on_release: root.manager.current = 'main'
                size_hint_y: None
                height: 50
                font_name: 'ChineseFont'

<ChartsScreen>:
    name: 'charts'
    ScrollView:
        GridLayout:
            cols: 1
            spacing: 10
            padding: 10
            size_hint_y: None
            height: self.minimum_height
            
            Label:
                text: '图表分析'
                font_size: '20sp'
                size_hint_y: None
                height: 40
                font_name: 'ChineseFont'
            
            BoxLayout:
                id: charts_content
                orientation: 'vertical'
                spacing: 20
                size_hint_y: None
                height: self.minimum_height
            
            Button:
                text: '返回主页'
                on_release: root.manager.current = 'main'
                size_hint_y: None
                height: 50
                font_name: 'ChineseFont'
''')

class MainScreen(Screen):
    pass

class InputScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_model = DataModel()
    
    def submit_data(self):
        # 表单验证
        try:
            # 收集表单数据
            trade_data = {
                'symbol': self.ids.symbol.text,
                'direction': self.ids.direction.text,
                'open_time': self.ids.open_time.text,
                'open_cycle': int(self.ids.open_cycle.text) if self.ids.open_cycle.text else 0,
                'open_boundary_ma': self.ids.open_boundary_ma.text,
                'target_boundary_ma': self.ids.target_boundary_ma.text,
                'drive_strategy': self.ids.drive_strategy.text,
                'entry_mode': self.ids.entry_mode.text,
                'entry_signal': self.ids.entry_signal.text,
                'stop_loss_rule': self.ids.stop_loss_rule.text,
                'take_profit_rule': self.ids.take_profit_rule.text,
                'open_emotion': self.ids.open_emotion.text,
                'open_price': float(self.ids.open_price.text) if self.ids.open_price.text else 0.0,
                'drawdown': float(self.ids.drawdown.text) if self.ids.drawdown.text else 0.0,
                'add_price': float(self.ids.add_price.text) if self.ids.add_price.text else 0.0,
                'add_price1': float(self.ids.add_price1.text) if self.ids.add_price1.text else 0.0,
                'reduce_price': float(self.ids.reduce_price.text) if self.ids.reduce_price.text else 0.0,
                'reduce_price1': float(self.ids.reduce_price1.text) if self.ids.reduce_price1.text else 0.0,
                'close_cycle': int(self.ids.close_cycle.text) if self.ids.close_cycle.text else 0,
                'close_time': self.ids.close_time.text,
                'close_boundary_ma': self.ids.close_boundary_ma.text,
                'exit_signal': self.ids.exit_signal.text,
                'close_emotion': self.ids.close_emotion.text,
                'close_price': float(self.ids.close_price.text) if self.ids.close_price.text else 0.0
            }
            
            # 插入数据并计算盈亏
            pl = self.data_model.insert_trade(trade_data)
            
            # 显示成功对话框
            popup_content = BoxLayout(orientation='vertical', padding=10, spacing=10)
            popup_content.add_widget(Label(text=f"盈亏: {pl:.2f}", font_name='ChineseFont'))
            ok_button = Button(text="确定", size_hint_y=None, height=40, font_name='ChineseFont')
            popup = Popup(title="提交成功", content=popup_content, size_hint=(0.6, 0.4))
            ok_button.bind(on_release=popup.dismiss)
            popup_content.add_widget(ok_button)
            popup.open()
            
            # 清空表单
            self.clear_form()
        except Exception as e:
            # 显示错误对话框
            popup_content = BoxLayout(orientation='vertical', padding=10, spacing=10)
            popup_content.add_widget(Label(text=f"错误: {str(e)}", font_name='ChineseFont'))
            ok_button = Button(text="确定", size_hint_y=None, height=40, font_name='ChineseFont')
            popup = Popup(title="提交失败", content=popup_content, size_hint=(0.6, 0.4))
            ok_button.bind(on_release=popup.dismiss)
            popup_content.add_widget(ok_button)
            popup.open()
    
    def clear_form(self):
        for key, widget in self.ids.items():
            if isinstance(widget, TextInput):
                widget.text = ""

class AnalysisScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_model = DataModel()
    
    def on_enter(self, *args):
        # 清空现有内容
        content = self.ids.analysis_content
        content.clear_widgets()
        
        # 获取所有交易数据
        trades = self.data_model.get_all_trades()
        
        if not trades:
            content.add_widget(Label(text="暂无交易数据", font_name='ChineseFont'))
            return
        
        # 显示交易记录
            for trade in trades:
                trade_box = BoxLayout(orientation='vertical', spacing=5, padding=10)
                # 确保索引在范围内
                trade_id = trade[0] if len(trade) > 0 else 'N/A'
                symbol = trade[1] if len(trade) > 1 else 'N/A'
                open_time = trade[3] if len(trade) > 3 else 'N/A'
                close_time = trade[20] if len(trade) > 20 else 'N/A'
                profit_loss = trade[24] if len(trade) > 24 else 0.0
                
                trade_box.add_widget(Label(text=f"交易 #{trade_id} - {symbol}", font_size='16sp', bold=True, font_name='ChineseFont'))
                trade_box.add_widget(Label(text=f"开仓时间: {open_time} | 平仓时间: {close_time}", font_name='ChineseFont'))
                trade_box.add_widget(Label(text=f"盈亏: {profit_loss:.2f}", font_name='ChineseFont'))
                content.add_widget(trade_box)
        
        # 按品种汇总
        summary = self.data_model.get_summary_by_symbol()
        if summary:
            content.add_widget(Label(text="\n品种汇总", font_size='18sp', bold=True, font_name='ChineseFont'))
            for item in summary:
                summary_box = BoxLayout(orientation='vertical', spacing=5, padding=10)
                summary_box.add_widget(Label(text=f"品种: {item[0]}", font_size='16sp', bold=True, font_name='ChineseFont'))
                summary_box.add_widget(Label(text=f"总交易次数: {item[1]}", font_name='ChineseFont'))
                summary_box.add_widget(Label(text=f"总盈亏: {item[2]:.2f}", font_name='ChineseFont'))
                content.add_widget(summary_box)

class ChartsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_model = DataModel()
    
    def on_enter(self, *args):
        # 清空现有内容
        content = self.ids.charts_content
        content.clear_widgets()
        
        # 获取汇总数据
        summary = self.data_model.get_summary_by_symbol()
        
        if not summary:
            content.add_widget(Label(text="暂无交易数据", font_name='ChineseFont'))
            return
        
        # 显示简单的文本汇总
        content.add_widget(Label(text="\n品种汇总", font_size='16sp', bold=True, font_name='ChineseFont'))
        for item in summary:
            summary_box = BoxLayout(orientation='vertical', spacing=5, padding=10)
            summary_box.add_widget(Label(text=f"品种: {item[0]}", font_size='14sp', bold=True, font_name='ChineseFont'))
            summary_box.add_widget(Label(text=f"总交易次数: {item[1]}", font_name='ChineseFont'))
            summary_box.add_widget(Label(text=f"总盈亏: {item[2]:.2f}", font_name='ChineseFont'))
            content.add_widget(summary_box)

class FuturesReviewApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen())
        sm.add_widget(InputScreen())
        sm.add_widget(AnalysisScreen())
        sm.add_widget(ChartsScreen())
        return sm

if __name__ == "__main__":
    FuturesReviewApp().run()