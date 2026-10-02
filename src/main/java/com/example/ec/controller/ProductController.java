package com.example.ec.controller;

import com.example.ec.model.Product;
import com.example.ec.repository.ProductsRepository;
import com.example.ec.service.ProductNotFoundException;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/products")
public class ProductController {

    static final int PAGE_SIZE = 10;

    private final ProductsRepository productsRepository;

    public ProductController(ProductsRepository productsRepository) {
        this.productsRepository = productsRepository;
    }

    /** 商品検索 (商品名部分一致・価格範囲)。1ページ10件 */
    @GetMapping
    public ResponseEntity<Map<String, Object>> search(@RequestParam(required = false) String q,
                                                      @RequestParam(required = false) String minPrice,
                                                      @RequestParam(required = false) String maxPrice,
                                                      @RequestParam(required = false) String page) {
        List<String> errors = new ArrayList<>();
        String keyword = (q == null || q.isBlank()) ? null : q.trim();
        Integer min = parseNonNegative(minPrice, "最低価格", errors);
        Integer max = parseNonNegative(maxPrice, "最高価格", errors);
        if (min != null && max != null && min > max) {
            errors.add("最低価格は最高価格以下で指定してください");
        }
        Integer pageNo = parseNonNegative(page, "ページ", errors);
        if (!errors.isEmpty()) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                    .body(Map.of("message", String.join(" / ", errors), "errors", errors));
        }

        int total = productsRepository.count(keyword, min, max);
        int totalPages = Math.max(1, (total + PAGE_SIZE - 1) / PAGE_SIZE);
        int current = Math.min(Math.max(pageNo == null ? 1 : pageNo, 1), totalPages);

        Map<String, Object> body = new LinkedHashMap<>();
        body.put("products", productsRepository.search(keyword, min, max, PAGE_SIZE, (current - 1) * PAGE_SIZE));
        body.put("total", total);
        body.put("pageSize", PAGE_SIZE);
        body.put("currentPage", current);
        body.put("totalPages", totalPages);
        return ResponseEntity.ok(body);
    }

    @GetMapping("/{id}")
    public Product detail(@PathVariable String id) {
        int pid;
        try {
            pid = Integer.parseInt(id);
        } catch (NumberFormatException e) {
            throw new IllegalArgumentException("商品IDが正しくありません");
        }
        Product product = productsRepository.findById(pid);
        if (product == null) {
            throw new ProductNotFoundException(pid);
        }
        return product;
    }

    private static Integer parseNonNegative(String value, String label, List<String> errors) {
        if (value == null || value.isBlank()) {
            return null;
        }
        try {
            int n = Integer.parseInt(value.trim());
            if (n < 0) {
                errors.add(label + "は0以上の整数で指定してください");
                return null;
            }
            return n;
        } catch (NumberFormatException e) {
            errors.add(label + "は整数で指定してください");
            return null;
        }
    }
}
