id="1-z8W6FjibtSqCDE4mFuBQskVveLr8FZNTAw89_TEX-Y"

import gspread as gs
import pandas as pd

gc = gs.service_account(filename='service_account1.json')
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1-z8W6FjibtSqCDE4mFuBQskVveLr8FZNTAw89_TEX-Y/edit#gid=1699052667')
ws = sh.worksheet('Attendees')
ws.get_all_records()
df = pd.DataFrame(ws.get_all_records())
df.head()
