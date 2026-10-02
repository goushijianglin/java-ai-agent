package com.example.ec.model;

public class Product {
    private Integer id;
    private String name;
    private String description;
    private Integer price;
    private Integer stock;

    public Integer getId() { return id; }
    public void setId(Integer id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    public Integer getPrice() { return price; }
    public void setPrice(Integer price) { this.price = price; }
    public Integer getStock() { return stock; }
    public void setStock(Integer stock) { this.stock = stock; }

    /** 商品画像 (静的リソース) のURL */
    public String getImageUrl() { return "/images/products/" + id + ".svg"; }
}
