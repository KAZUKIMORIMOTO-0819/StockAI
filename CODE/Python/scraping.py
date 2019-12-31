### 基本モジュール
import pandas as pd
import numpy as np
from datetime import datetime

### スクレイピング
from bs4 import BeautifulSoup
import requests

### 株価のスクレイピングを行うクラス
class SCRAPING_STOCK():
    def __init__(self,):
        self.year_list = [2017, 2018, 2019]     # 株価取得の年リスト
        self.code_df = pd.read_csv("./DATA/Stock_code/homeappliances.csv")
    
    ### スクレイピングを行うメソッド
    def scraping(self, stock_number):
        dfs = []
        for year in self.year_list:
            try:
                url = 'https://kabuoji3.com/stock/{}/{}/'.format(stock_number,year)
                headers = {    # ユーザエージェント情報　自分が使っているプログラムや機械の情報を示す必要がある　
                            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"
                        }
                soup = BeautifulSoup(requests.get(url, headers=headers).content,'html.parser')
                tag_tr = soup.find_all('tr')
                head = [h.text for h in tag_tr[0].find_all('th')]
                ### テーブルデータの取得
                data = []
                for i in range(1,len(tag_tr)):
                    data.append([d.text for d in tag_tr[i].find_all('td')])
                df = pd.DataFrame(data, columns = head)
                ### 型変換
                col = ['始値','高値','安値','終値','出来高','終値調整']
                for c in col:
                    df[c] = df[c].astype(float)
                df['日付'] = [datetime.strptime(i,'%Y-%m-%d') for i in df['日付']]
                dfs.append(df)
            except IndexError:
                print('No data')
        return dfs
    
    ### 株価を一つのDataFrameに変換する
    def concatenate(self, dfs):
        df_stock = pd.concat(dfs,axis=0)
        df_stock = df_stock.reset_index(drop=True)
        col = ['始値','高値','安値','終値','出来高','終値調整']
        for c in col:
            df_stock[c] = df_stock[c].astype(float)
        return df_stock
    
    ### DataFrameの保存
    def save_df_stock(self):
        #複数のデータフレームをcsvで保存
        for i in range(len(self.code_df)):
            code = self.code_df.loc[i,'code']
            name = self.code_df.loc[i,'name']
            print(code,name)
            dfs = self.scraping(code)    # スクレイピング開始、リストのなかに年ごとのDataFrame
            df_stock = self.concatenate(dfs)     # リスト⇒DataFrame
            df_stock.to_csv('./DATA/Stock/{}-{}.csv'.format(code,name))

    ### 実行
    def execute(self):
        self.save_df_stock()

if __name__ == '__main__':
    print("----- Start scraping stock -----")
    scraping_stock = SCRAPING_STOCK()
    scraping_stock.execute()
