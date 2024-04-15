import requests
from bs4 import BeautifulSoup
import wx
import webbrowser

class EventSelector(wx.Frame):
    def __init__(self):
        # 初始化 wx.Frame
        super().__init__(None, title="KKTIX Event Selector", size=(400, 200))

        # 獲取活動列表
        self.event_dict = self.get_events()

        # 建立活動選擇下拉選單
        self.event_choice = wx.Choice(self, choices=list(self.event_dict.keys()))
        self.event_choice.SetSelection(0)

        # 建立顯示售票時間的文字區域
        self.time_text = wx.StaticText(self, label="")

        # 建立顯示售票時間的按鈕，並綁定事件處理函數
        self.time_button = wx.Button(self, label="Show Time")
        self.time_button.Bind(wx.EVT_BUTTON, self.show_time)

        # 建立開啟活動網頁的按鈕，並綁定事件處理函數
        self.open_button = wx.Button(self, label="Open Event")
        self.open_button.Bind(wx.EVT_BUTTON, self.open_event)

        # 建立布局
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.event_choice, 0, wx.EXPAND, 5)
        sizer.Add(self.time_button, 0, wx.EXPAND, 5)
        sizer.Add(self.time_text, 0, wx.EXPAND, 5)
        sizer.Add(self.open_button, 0, wx.EXPAND, 5)
        self.SetSizer(sizer)

    def get_events(self):
        try:
            # 發送 GET 請求到 KKTIX 首頁
            response = requests.get("https://kktix.com/", verify=False)
            # 檢查 HTTP 響應狀態碼
            response.raise_for_status()
        except requests.RequestException as e:
            # 如果請求失敗，輸出錯誤信息並返回空字典
            print(f"Failed to get events: {e}")
            return {}

        # 解析 HTML 響應內容
        soup = BeautifulSoup(response.text, 'html.parser')
        print(soup)
        # 找到所有的活動卡片
        events = soup.find_all('div', class_='new-event')

        # 建立活動名稱和連結的字典
        event_dict = {}
        for event in events:
            title = event.find('h3').text
            link = event.find('a')['href']
            event_dict[title] = link

        # 如果字典為空，輸出警告信息
        if not event_dict:
            print("No events found.")

        return event_dict

    def show_time(self, event):
        # 獲取選擇的活動名稱
        event_title = self.event_choice.GetStringSelection()
        # 獲取活動的連結
        link = self.event_dict[event_title]
        # 發送 GET 請求到活動頁面
        response = requests.get(link, verify=False)
        # 解析 HTML 響應內容
        soup = BeautifulSoup(response.text, 'html.parser')
        # 找到售票時間
        time = soup.find('time').text
        # 顯示售票時間
        self.time_text.SetLabel(time)

    def open_event(self, event):
        # 獲取選擇的活動名稱
        event_title = self.event_choice.GetStringSelection()
        # 獲取活動的連結
        link = self.event_dict[event_title]
        # 使用預設的瀏覽器開啟活動頁面
        webbrowser.open(link)

# 建立應用程式
app = wx.App()
# 建立 EventSelector 實例
frame = EventSelector()
# 顯示視窗
frame.Show()
# 進入應用程式的主迴圈
app.MainLoop()