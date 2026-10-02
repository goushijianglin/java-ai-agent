package com.example.ec.model;

import java.io.Serializable;

/** セッション (属性名 loginUser) に保存するログインユーザ情報。パスワードは持たない。 */
public record LoginUser(int id, String username, String displayName) implements Serializable {
}
