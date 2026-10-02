package com.example.ec.service;

public class ProductNotFoundException extends RuntimeException {
    public ProductNotFoundException(int productId) {
        super("商品が見つかりません（ID: " + productId + "）");
    }
}
