package com.example.ec.repository;

import com.example.ec.model.Product;
import java.util.List;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

@Mapper
public interface ProductsRepository {

    List<Product> search(@Param("q") String q,
                         @Param("minPrice") Integer minPrice,
                         @Param("maxPrice") Integer maxPrice,
                         @Param("limit") int limit,
                         @Param("offset") int offset);

    int count(@Param("q") String q,
              @Param("minPrice") Integer minPrice,
              @Param("maxPrice") Integer maxPrice);

    Product findById(@Param("id") int id);

    /** 行ロックを取得して商品を取得 (購入トランザクション内で使用) */
    Product findByIdForUpdate(@Param("id") int id);

    /** 在庫が足りる場合のみ減算する。更新件数 0 = 在庫不足 */
    int decreaseStock(@Param("id") int id, @Param("quantity") int quantity);
}
