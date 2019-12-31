##################################################################
# Dockerfile
# イメージの作成 docker build -t test_images .
# コンテナの起動 docker run -it --name test_container test_imgaes bash
##################################################################

# ベースイメージの作成
FROM python:3.6

# メモ情報
LABEL version="1.0"
LABEL description="StockAI test environment"
LABEL maintainer="marimorimo0819@gmail.com"

# 同じディレクトリ内のファイルをコンテナ内に追加する
ADD . /stockai
WORKDIR /stockai
RUN pip install -r requirements.txt