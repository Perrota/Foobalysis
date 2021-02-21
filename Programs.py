import pyautogui as pya
import pyperclip
import pandas as pd

class foobar2000():

    def __init__(self, OpenDelay):
        self.OpenDelay = OpenDelay
        self.open()

    def open(self):
        pya.press('win', pause=self.OpenDelay/2)
        pya.typewrite('foobar2000', pause=self.OpenDelay)
        pya.press('enter', pause=self.OpenDelay*2)

    def max_window(self):
        pya.hotkey('alt', 'space')
        pya.press('x')

    def activate_playing_tab(self):
        pya.click(x=1590, y=444)

    def get_duration(self):
        pya.click(x=1560, y=608)
        pya.hotkey('ctrl', 'c')
        strDuration = pyperclip.paste()
        return strDuration[:strDuration.find('.')]

    def get_artist(self):
        pya.click(x=1560, y=540)
        pya.hotkey('ctrl', 'c')
        strArtist = pyperclip.paste()
        return strArtist

    def get_title(self):
        pya.click(x=1560, y=490)
        pya.hotkey('ctrl', 'c')
        strTitle = pyperclip.paste()
        return strTitle

    def select_all(self):
        pya.hotkey('ctrl', 'shift', 'a')

    def open_text_utilities(self):
        pya.hotkey('shift', 'f10')
        pya.hotkey('U', 'T', 'D')

    def get_tag_info(self, FoobarTags):
        pyperclip.copy(FoobarTags)
        pya.hotkey('ctrl', 'v', pause=self.OpenDelay)
        pya.press('tab', presses=4)
        pya.press('enter', pause=self.OpenDelay/2)

    def get_statistics(self):
        self.select_all()
        self.open_text_utilities()
        self.get_tag_info(r'%album%;$ifequal($len(%length%),4,00:0%length%,00:%length%);%date%;%title%;%rating%;%genre%;%album artist%;$date(%added%);%play_count%;%artist%')
        self.close()
        pdSongs = pd.read_clipboard(
            sep=';',
            encoding='utf-8'
        )

        return pdSongs

    def close(self):
        for x in range(2):
            pya.hotkey('alt', 'f4')

    def play_video(self):

        import requests
        import time
        from datetime import datetime
        import os
        import re

        while True:

            Time1_Datetime = datetime.now()
            
            self.max_window()
            self.activate_playing_tab()
            Playing_String = self.get_artist() + ' ' + self.get_title()
            Duration_String = self.get_duration()
            Duration_Datetime = datetime.strptime(Duration_String, '%M:%S')
            SecondsOfDuration_Integer = int((Duration_Datetime-datetime(1900,1,1)).total_seconds())

            HTML_String = requests.get(f'https://www.youtube.com/results?search_query={Playing_String}').text
            ExtractedID_String = re.findall(r'"videoId":"[A-Za-z_0-9]+"', HTML_String)[0]
            RefinedID_String = str(ExtractedID_String).split(":")[1].replace('"', "")

            Time2_Datetime = datetime.now()
            TimeElapsed1_Datetime = Time2_Datetime - Time1_Datetime
            os.popen(f"start microsoft-edge:https://youtu.be/{RefinedID_String}?t={TimeElapsed1_Datetime.seconds+5}")
            
            time.sleep(4)
            pya.hotkey('shift', 'alt', 'm')
            time.sleep(4)
            pya.click(10, 900)
            pya.press('f')
            pya.moveTo(1919, 900)

            Time3_Datetime = datetime.now()
            TimeElapsed2_Datetime = Time3_Datetime - Time1_Datetime
            time.sleep(int(SecondsOfDuration_Integer-TimeElapsed2_Datetime.seconds+1))
            pya.hotkey('ctrl', 'w')
