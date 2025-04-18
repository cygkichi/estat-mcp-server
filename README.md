# e-Stat MCP server

[Model Context Protocol](https://modelcontextprotocol.io/introduction) (MCP) サーバーで、日本の政府統計ポータルサイト「e-Stat」のAPIにアクセスするための機能を提供します。言語モデルが統計データを検索・取得できるようになります。


## ツール

このサーバーは以下のツールを提供しています：

- `search_e_stat_tables` : キーワードと調査年で統計表を検索します
- `get_e_stat_meta_info` : 統計表IDに対応するメタ情報を取得します
- `get_specific_e_stat_data` : 統計表IDまたはデータセットIDに対応する統計データを取得します
-  `get_e_stat_ref_dataset` : データセットの絞り込み条件等を参照します
- `get_e_stat_data_catalog` : 統計表ファイルおよび統計データベースの情報を取得します

## 使い方
このサーバーを使用するには、e-Stat APIのアプリケーションIDが必要です。以下の手順で取得できます：
1. [e-Stat API機能](https://www.e-stat.go.jp/api/)にアクセス
2. ユーザ登録を行う
3. 利用規約に同意してアプリケーションIDを取得


#### Claude Desktop

- On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
- On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
    "mcpServers": {
        "e-stat": {
            "command": "uv",
            "args": [
                "--directory",
                "/path/to/estat-mcp-server",
                "run",
                "server.py"
            ],
            "env": {
                "E_STAT_APP_ID": "YOUR_E_STAT_APP_ID"
            }
        }
    }
}
```

```json
{
    "mcpServers": {
        "e-stat": {
            "command": "uvx",
            "args": [
                "estat-mcp-server"
            ],
            "env": {
                "E_STAT_APP_ID": "YOUR_E_STAT_APP_ID"
            }
        }
    }
}
```



## 使用例

接続後、Claudeに以下のような質問ができます：

- "2023年の東京都の人口統計を検索して"
- "アイスクリームの需要に関する統計を取得して"
- "都道府県別の高齢化率を比較して"


## ライセンス

このプロジェクトはMITライセンスの下で提供されています
 - 詳細はLICENSEファイルを参照してください。