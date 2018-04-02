import re
from bs4 import BeautifulSoup

soup = BeautifulSoup(open('./tmp/record.html'), 'html.parser')
div1 = soup.find(class_='page_content_ctn')
wallet_table_rows = div1.find_all('tr', class_='wallet_table_row')
dates = []
accounts = []
res = {}
for wallet_table_row in wallet_table_rows:
    wht_date = wallet_table_row.find('td', class_='wht_date').stripped_strings
    wht_items = wallet_table_row.find('td', class_='wht_items').stripped_strings
    tmp = wallet_table_row.find('td', class_='wht_wallet_change')
    if tmp:
        tp = list(tmp.stripped_strings)
    wht_total = wallet_table_row.find('td', class_='wht_total').stripped_strings
    wht_num = re.search(r'(.*)¥ (.*)', list(wht_total)[0]).groups()
    if not tp or tp[0][0] != '+':
        account = float(wht_num[1])
        date = list(wht_date)[0]
        if date in res:
            res[date] += account
        else:
            res[date] = account
key_lst = sorted(res.keys())
val_lst = [int(res[key]*100)/100.0 for key in key_lst]
print(key_lst)
print(val_lst)
# accounts.append(account)
# dates.append(list(wht_date)[0])
