import requests
import re
import pandas as pd
from sqlalchemy import create_engine

headers = {
    'authority': 'pf2.easytool.es',
    'accept': '*/*',
    'x-requested-with': 'XMLHttpRequest',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://pf2.easytool.es',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://pf2.easytool.es/spellbook/',
    'accept-language': 'en-US,en;q=0.9,nl;q=0.8',
    'cookie': 'PHPSESSID=k5bds782h4d77fma3drk8f1o6r',
}

data = {
    'caca': '{"traditions":["1182","1184","1183","1185"],"schools":["25","56","70","84","88","114","139","179"],"actions":["Reaction","action1","action2","action3","1 minute","5 minutes","10 minutes","1 hour"],"traits":["26","28","38","39","1426","48","50","57","61","62","63","66","69","78","79","83","87","90","91","95","98","99","100","105","111","115","122","123","128","132","135","136","140","1202","147","148","149","150","151","154","160","163","165","167","169","178","185","187"],"rarity":["0","181","159"],"target":["0","1","2","3"],"level":["0","1","2","3","4","5","6","7","8","9","10"],"sources":["5","8194","9","4306","9957","12","4795","4796","4797","4798","6726","7292","7509","7511"],"text":""}',
    'H': 'false',
    'Traits': '0',
    'Checked': '[]',
    'FocusSpell': '0',
    'cantripLvl': '1'
}

response = requests.post('https://pf2.easytool.es/spellbook/table.php', headers=headers, data=data)
response.encoding = 'utf-8'
fix_actions = re.compile(
    r'<i class="pf2 (?:Reaction|action\d)" data-toggle="tooltip" title="(Reaction|Single Action|Two-Action Activity|Three-Action Activity)"></i>')
fixed_table = fix_actions.sub(r'\1', response.text)
df = pd.read_html(fixed_table, index_col=1)[0].dropna(how='all', axis='columns')
engine = create_engine('sqlite:///spellbook.db', echo=False)
df.to_sql('spells', con=engine, if_exists='replace')
