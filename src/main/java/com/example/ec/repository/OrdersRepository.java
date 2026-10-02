package com.example.ec.repository;

import com.example.ec.model.Order;
import com.example.ec.model.OrderDetail;
import com.example.ec.model.OrderItem;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

@Mapper
public interface OrdersRepository {

    /** 注文を作成し、採番された id を order.id にセットする */
    int insertOrder(Order order);

    int insertOrderItem(OrderItem item);

    /** 注文 (1注文1明細) を商品名付きで取得 */
    OrderDetail findDetail(@Param("orderId") int orderId);
}
