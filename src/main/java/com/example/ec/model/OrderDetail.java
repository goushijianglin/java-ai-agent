package com.example.ec.model;

import java.time.LocalDateTime;

/** 購入完了画面用: 注文 + 明細 + 商品名 */
public class OrderDetail {
    private Integer orderId;
    private Integer userId;
    private LocalDateTime createdAt;
    private Integer productId;
    private String productName;
    private Integer quantity;
    private Integer unitPrice;

    public Integer getOrderId() { return orderId; }
    public void setOrderId(Integer orderId) { this.orderId = orderId; }
    public Integer getUserId() { return userId; }
    public void setUserId(Integer userId) { this.userId = userId; }
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
    public Integer getProductId() { return productId; }
    public void setProductId(Integer productId) { this.productId = productId; }
    public String getProductName() { return productName; }
    public void setProductName(String productName) { this.productName = productName; }
    public Integer getQuantity() { return quantity; }
    public void setQuantity(Integer quantity) { this.quantity = quantity; }
    public Integer getUnitPrice() { return unitPrice; }
    public void setUnitPrice(Integer unitPrice) { this.unitPrice = unitPrice; }

    public int getTotalPrice() { return quantity * unitPrice; }
}
