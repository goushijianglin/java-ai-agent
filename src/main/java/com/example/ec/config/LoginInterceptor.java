package com.example.ec.config;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;
import java.nio.charset.StandardCharsets;
import org.springframework.http.MediaType;
import org.springframework.web.servlet.HandlerInterceptor;

/**
 * 未ログインのアクセスを拒否する。
 * 画面 (React の各ページ) は /login へリダイレクト、API (/api/**) は 401 を返す。
 */
public class LoginInterceptor implements HandlerInterceptor {

    public static final String LOGIN_USER = "loginUser";

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler)
            throws Exception {
        HttpSession session = request.getSession(false);
        if (session != null && session.getAttribute(LOGIN_USER) != null) {
            return true;
        }
        if (request.getRequestURI().startsWith(request.getContextPath() + "/api/")) {
            response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
            response.setCharacterEncoding(StandardCharsets.UTF_8.name());
            response.setContentType(MediaType.APPLICATION_JSON_VALUE);
            response.getWriter().write("{\"message\":\"ログインしてください\"}");
        } else {
            response.sendRedirect(request.getContextPath() + "/login");
        }
        return false;
    }
}
