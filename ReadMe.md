# FastApi 模板
#### 2024/07/01 Jen

## 專案結構
```bash
.
├── app
│   ├── api
│   │   └── endpoints
│   │       └── api1.py
│   ├── config
│   │   └── logging_config.yaml
│   ├── core
│   ├── db
│   │   └── models.py
│   ├── schemas
│   ├── services
│   ├── utils
│   │   └── db_utils.py
│   ├── logging_config.py
│   └── main.py
└── test
```

## 說明
- `app` : 主要程式碼
- `app/api` : API 路由
- `app/config` : 設定檔
  - `logging_config.yaml`： `logging` 模組的設定檔，可分為兩種模式：    
    - `dev` :輸出至 console 與 資料庫（預設為 sql server），輸出等級為 `DEBUG`
    - `prod`：輸出至 console 與 資料庫（預設為 sql server），輸出等級為 `INFO`
  - 輸出至資料庫的方法，參考 `app.logging_config.SQLServerHandler`
    - 若要啟動，需要定義好 連線 `engine`，傳入 `app.logging_config.setup_logging`
    - 若未定義 `engine` 或找不到 `engine` ，則使用logging預設定義輸出至 Console，等級為 `INFO`
  - 連線到資料庫所有需要的參數
    - 可以定義到 `app/.env` 中。但為了避免誤將機敏資料上傳至 git，建議使用`環境變數`的方式，在linux中，可以在`~/.bashrc` 或 `~/.bash_profile` 中定義：
        ```bash
        export SQLSERVER_USER=`username`
        export SQLSERVER_PASSWORD=`password`
        export SQLSERVER_DB=`databasename`
        export SQLSERVER_HOST=`host_ip`
        export SQLSERVER_PORT=`port`
        ```
  - ...
  - `utils/db_utils.py`: 資料庫連線工具
  - `logging_config.py`: 輸出至資料庫的 logging 設定