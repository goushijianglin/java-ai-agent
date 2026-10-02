package com.example.ec.controller;

import com.example.ec.config.LoginInterceptor;
import com.example.ec.model.LoginUser;
import com.example.ec.model.OrderDetail;
import com.example.ec.repository.OrdersRepository;
import com.example.ec.service.PurchaseService;
import jakarta.servlet.http.HttpSession;
import java.time.format.DateTimeFormatter;
import java.util.LinkedHashMap;
import java.util.Map;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
public class PurchaseController {

    public record PurchaseRequest(Integer productId, Integer quantity) {
    }

    private static final DateTimeFormatter DATE_FORMAT = DateTimeFormatter.ofPattern("yyyy/MM/dd HH:mm:ss");

    private final PurchaseService purchaseService;
    private final OrdersRepository ordersRepository;

    public PurchaseController(PurchaseService purchaseService, OrdersRepository ordersRepository) {
        this.purchaseService = purchaseService;
        this.ordersRepository = ordersRepository;
    }

    /**
     * 購入。成功時は 201 {orderId}。
     * 数量不正は 400、在庫不足は 409、商品なしは 404 (ApiExceptionHandler)。
     */
    @PostMapping("/purchase")
    public ResponseEntity<Map<String, Object>> purchase(@RequestBody PurchaseRequest req, HttpSession session) {
        LoginUser loginUser = (LoginUser) session.getAttribute(LoginInterceptor.LOGIN_USER);
        if (req.productId() == null) {
            throw new IllegalArgumentException("商品が指定されていません");
        }
        if (req.quantity() == null || req.quantity() < 1) {
            throw new IllegalArgumentException("数量は1以上で入力してください");
        }
        int orderId = purchaseService.purchase(loginUser.id(), req.productId(), req.quantity());
        return ResponseEntity.status(HttpStatus.CREATED).body(Map.of("orderId", orderId));
    }

    /** 購入完了画面用の注文情報 (自分の注文のみ) */
    @GetMapping("/orders/{orderId}")
    public ResponseEntity<Map<String, Object>> order(@PathVariable String orderId, HttpSession session) {
        LoginUser loginUser = (LoginUser) session.getAttribute(LoginInterceptor.LOGIN_USER);
        OrderDetail detail = null;
        try {
            detail = ordersRepository.findDetail(Integer.parseInt(orderId));
        } catch (NumberFormatException ignored) {
            // 不正な注文番号は「見つからない」扱い
        }
        if (detail == null || detail.getUserId() != loginUser.id()) {
            return ApiExceptionHandler.error(HttpStatus.NOT_FOUND, "注文が見つかりません");
        }

        Map<String, Object> order = new LinkedHashMap<>();
        order.put("orderId", detail.getOrderId());
        order.put("productId", detail.getProductId());
        order.put("productName", detail.getProductName());
        order.put("quantity", detail.getQuantity());
        order.put("unitPrice", detail.getUnitPrice());
        order.put("totalPrice", detail.getTotalPrice());
        order.put("createdAt", detail.getCreatedAt().format(DATE_FORMAT));
        return ResponseEntity.ok(order);
    }
}
