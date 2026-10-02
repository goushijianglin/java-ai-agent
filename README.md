# Demo EC (Java 21 / Spring Boot 3.5 / MyBatis / PostgreSQL / Tomcat 11 / React 18)

最小構成の EC サイト。React 18 (Vite) の SPA と Spring Boot の JSON API を 1 つの `ROOT.war` にまとめ、
外部 Tomcat (`$CATALINA_HOME`) にデプロイします。

## 構成

```
frontend/                React 18 + React Router 6 + Vite
  src/pages/             LoginPage / ProductsPage / ProductDetailPage / PurchaseCompletePage
  src/api.js             API 呼び出し (fetch)
  src/auth.jsx           ログイン状態 (AuthProvider / RequireAuth)
  public/images/products 商品画像 (SVG)
src/main/java/com/example/ec/
  controller/            LoginController, ProductController, PurchaseController (JSON API)
                         SpaController (画面URL → index.html), ApiExceptionHandler
  config/                LoginInterceptor (HandlerInterceptor), WebConfig
  service/               PurchaseService (@Transactional)
  repository/            UsersRepository, ProductsRepository, OrdersRepository (MyBatis)
  tools/DbInit           DB初期化プログラム
src/main/resources/db/   schema.sql, data.sql
```

- `mvn package` の `generate-resources` フェーズで `npm install` → `npm run build` が実行され、
  ビルド結果が `target/classes/static` に出力されて WAR に同梱されます（Spring Boot の静的リソース配信）。
- 画面 URL (`/login`, `/products`, `/products/{id}`, `/purchase/complete`) は `index.html` を返し、画面遷移は React Router が行います。

## 画面 URL

| URL | 説明 |
|---|---|
| `/login` | ログイン。成功で `/products` へ。ヘッダにユーザ名表示 |
| `/products?q=&minPrice=&maxPrice=&page=` | 商品検索。10件/ページ、「前へ」「次へ」 |
| `/products/{id}` | 商品詳細・画像・購入フォーム。在庫不足/数量不正はエラー表示 |
| `/purchase/complete?orderId=` | 注文番号・商品名・数量・合計金額 |
| ヘッダの「ログアウト」 | `POST /api/logout` でセッション破棄 → `/login` へ |

## API

| メソッド・URL | 説明 |
|---|---|
| `POST /api/login` `{username, password}` | 認証。セッション属性 `loginUser` に保存。失敗は 401 |
| `GET /api/me` | ログイン中ユーザ |
| `POST /api/logout` | セッション破棄 (**ログアウトは POST のみ**) |
| `GET /api/products?q=&minPrice=&maxPrice=&page=` | 商品検索 |
| `GET /api/products/{id}` | 商品詳細 (無ければ 404) |
| `POST /api/purchase` `{productId, quantity}` | 購入 → 201 `{orderId}`。数量不正 400、在庫不足 409 |
| `GET /api/orders/{orderId}` | 注文情報 (自分の注文のみ) |

認可: `LoginInterceptor` が `/products`, `/products/**`, `/purchase/**` と `/api/**` (login 以外) を保護。
未ログインの場合、画面は `/login` にリダイレクト、API は 401 を返します（React も 401 で `/login` に遷移）。

## DB 初期化

接続先: `jdbc:postgresql://db:5432/app` (user/password = app/app)。環境変数 `DB_URL`, `DB_USER`, `DB_PASSWORD` で変更可。

```bash
mvn -q compile exec:java -Dfrontend.skip=true   # DbInit: テーブル DROP → CREATE → 初期データ投入
```

> 実行するたびに全テーブルを作り直します（注文データも消えます）。初期データ: ユーザ `demo / demo`、商品 24 件。

## ビルド・デプロイ

```bash
./scripts/deploy.sh --build   # mvn -q clean package (React ビルド含む) → Tomcat 停止 → ROOT.war 配置 → 起動 → /login 確認
./scripts/deploy.sh           # ビルド済み target/ROOT.war をデプロイだけする
```

- デプロイ先: `$CATALINA_BASE/webapps/ROOT.war`（この環境では `/workspaces/project/.tomcat-base`）
- ログ: `$CATALINA_BASE/logs/catalina.out`
- 確認: http://localhost:8080/login

### フロントエンド開発

```bash
cd frontend && npm run dev    # http://localhost:5173 (/api は Tomcat:8080 にプロキシ)
```

商品画像を作り直す場合: `python3 tools/generate_product_images.py`

## 注意

- **パスワードは平文で保存・比較しています（最小実装のため）。本番では必ず BCrypt 等でハッシュ化してください。**
- Spring Security を使っていないため CSRF 対策はありません。
