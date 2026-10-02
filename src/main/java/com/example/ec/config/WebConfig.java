package com.example.ec.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class WebConfig implements WebMvcConfigurer {

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(new LoginInterceptor())
                .addPathPatterns(
                        // 画面
                        "/products", "/products/**", "/purchase", "/purchase/**",
                        // API
                        "/api/me", "/api/logout", "/api/products", "/api/products/**",
                        "/api/purchase", "/api/purchase/**", "/api/orders/**");
    }
}
