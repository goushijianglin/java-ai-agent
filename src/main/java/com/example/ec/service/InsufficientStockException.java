package com.example.ec.service;

/** 在庫不足。購入トランザクションをロールバックさせるため RuntimeException */
public class InsufficientStockException extends RuntimeException {
    private final int stock;
    private final int requested;

    public InsufficientStockException(String productName, int stock, int requested) {
        super("「" + productName + "」の在庫が不足しています（在庫: " + stock + " 個 / ご希望: " + requested + " 個）");
        this.stock = stock;
        this.requested = requested;
    }

    public int getStock() { return stock; }
    public int getRequested() { return requested; }
}
