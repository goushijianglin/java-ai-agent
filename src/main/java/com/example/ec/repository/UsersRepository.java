package com.example.ec.repository;

import com.example.ec.model.User;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

@Mapper
public interface UsersRepository {
    User findByUsername(@Param("username") String username);
}
