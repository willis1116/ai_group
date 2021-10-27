# source from https://github.com/BingHongLi/ncu_gcp_ai_project
# 課程專題開發使用

# 環境準備
建置 Project
建置 cloud storage
建置 firestore


# 將訓練好的模型放入 converted_savedmodel資料夾

# 將要回應的json放入line_message_json資料夾

# 構建程式碼

```
gcloud config set project YOUR-PROJECT-ID
gcloud builds submit  --tag gcr.io/$GOOGLE_CLOUD_PROJECT/ai-group-dev:0.0.1
```

# 部署

指定環境變數

```
USER_INFO_GS_BUCKET_NAME:  剛剛建立的資料桶子
LINE_CHANNEL_ACCESS_TOKEN: 課程內述說
LINE_CHANNEL_SECRET: 課程內述說
```
# 將生成的網址追加callback 貼回line網站的webhook
