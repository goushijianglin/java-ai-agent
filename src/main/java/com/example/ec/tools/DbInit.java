package com.example.ec.tools;

import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

/**
 * DB初期化プログラム。classpath の db/schema.sql (DDL) と db/data.sql (初期データ) を
 * 1トランザクションで実行する。
 *
 * <pre>
 * mvn -q compile exec:java
 * </pre>
 *
 * 接続先は環境変数 DB_URL / DB_USER / DB_PASSWORD で上書き可能。
 */
public final class DbInit {

    private DbInit() {
    }

    public static void main(String[] args) throws Exception {
        String url = env("DB_URL", "jdbc:postgresql://db:5432/app");
        String user = env("DB_USER", "app");
        String password = env("DB_PASSWORD", "app");

        System.out.println("[DbInit] connect: " + url);
        try (Connection con = DriverManager.getConnection(url, user, password)) {
            con.setAutoCommit(false);
            try (Statement st = con.createStatement()) {
                System.out.println("[DbInit] execute db/schema.sql");
                st.execute(readResource("db/schema.sql"));
                System.out.println("[DbInit] execute db/data.sql");
                st.execute(readResource("db/data.sql"));
                con.commit();
            } catch (SQLException e) {
                con.rollback();
                throw e;
            }
            printCount(con, "users");
            printCount(con, "products");
            printCount(con, "orders");
            printCount(con, "order_items");
        }
        System.out.println("[DbInit] done");
    }

    private static void printCount(Connection con, String table) throws SQLException {
        try (Statement st = con.createStatement();
             ResultSet rs = st.executeQuery("SELECT count(*) FROM " + table)) {
            rs.next();
            System.out.println("[DbInit] " + table + ": " + rs.getInt(1) + " rows");
        }
    }

    private static String readResource(String path) throws IOException {
        try (InputStream in = DbInit.class.getClassLoader().getResourceAsStream(path)) {
            if (in == null) {
                throw new IOException("resource not found: " + path);
            }
            return new String(in.readAllBytes(), StandardCharsets.UTF_8);
        }
    }

    private static String env(String key, String def) {
        String v = System.getenv(key);
        return (v == null || v.isBlank()) ? def : v;
    }
}
