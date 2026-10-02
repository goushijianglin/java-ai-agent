package com.example.ec.service;

import com.example.ec.model.Order;
import com.example.ec.model.OrderItem;
import com.example.ec.model.Product;
import com.example.ec.repository.OrdersRepository;
import com.example.ec.repository.ProductsRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class PurchaseService {

    private final ProductsRepository productsRepository;
    private final OrdersRepository ordersRepository;

    public PurchaseService(ProductsRepository productsRepository, OrdersRepository ordersRepository) {
        this.productsRepository = productsRepository;
        this.ordersRepository = ordersRepository;
    }

    /**
     * 在庫減算と注文作成を同一トランザクションで行う。
     * いずれかで例外が発生した場合は全てロールバックされる。
     *
     * @return 作成した注文ID
     */
    @Transactional
    public int purchase(int userId, int productId, int quantity) {
        if (quantity < 1) {
            throw new IllegalArgumentException("数量は1以上で指定してください");
        }

        // 行ロックを取って在庫を確認 (同時購入でも在庫がマイナスにならない)
        Product product = productsRepository.findByIdForUpdate(productId);
        if (product == null) {
            throw new ProductNotFoundException(productId);
        }
        if (product.getStock() < quantity) {
            throw new InsufficientStockException(product.getName(), product.getStock(), quantity);
        }

        // 在庫減算 (条件付き UPDATE でも二重に保護)
        if (productsRepository.decreaseStock(productId, quantity) != 1) {
            throw new InsufficientStockException(product.getName(), product.getStock(), quantity);
        }

        // 注文作成
        Order order = new Order();
        order.setUserId(userId);
        ordersRepository.insertOrder(order);

        OrderItem item = new OrderItem();
        item.setOrderId(order.getId());
        item.setProductId(productId);
        item.setQuantity(quantity);
        item.setUnitPrice(product.getPrice());
        ordersRepository.insertOrderItem(item);

        return order.getId();
    }
}
