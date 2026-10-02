package com.example.ec.controller;

import com.example.ec.config.LoginInterceptor;
import jakarta.servlet.http.HttpSession;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

/**
 * React (SPA) の画面URL。いずれも index.html を返し、画面遷移は React Router が行う。
 * ログイン必須の画面は LoginInterceptor で未ログイン時 /login にリダイレクトされる。
 */
@Controller
public class SpaController {

    @GetMapping("/")
    public String root() {
        return "redirect:/products";
    }

    @GetMapping("/login")
    public String login(HttpSession session) {
        if (session.getAttribute(LoginInterceptor.LOGIN_USER) != null) {
            return "redirect:/products";
        }
        return "forward:/index.html";
    }

    @GetMapping({"/products", "/products/{id}", "/purchase/complete"})
    public String page() {
        return "forward:/index.html";
    }
}
