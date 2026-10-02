package com.example.ec.controller;

import com.example.ec.config.LoginInterceptor;
import com.example.ec.model.LoginUser;
import com.example.ec.model.User;
import com.example.ec.repository.UsersRepository;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpSession;
import java.util.Map;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
public class LoginController {

    public record LoginRequest(String username, String password) {
    }

    private final UsersRepository usersRepository;

    public LoginController(UsersRepository usersRepository) {
        this.usersRepository = usersRepository;
    }


    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody LoginRequest req, HttpServletRequest request) {
        String username = req.username() == null ? "" : req.username().trim();
        String password = req.password() == null ? "" : req.password();
        User user = username.isEmpty() ? null : usersRepository.findByUsername(username);
        // 最小実装のためパスワードは平文比較
        if (user == null || !user.getPassword().equals(password)) {
            return ApiExceptionHandler.error(HttpStatus.UNAUTHORIZED, "ユーザ名またはパスワードが正しくありません");
        }

        // セッション固定化対策: 既存セッションを破棄して新しく作る
        HttpSession old = request.getSession(false);
        if (old != null) {
            old.invalidate();
        }
        LoginUser loginUser = new LoginUser(user.getId(), user.getUsername(), user.getDisplayName());
        request.getSession(true).setAttribute(LoginInterceptor.LOGIN_USER, loginUser);
        return ResponseEntity.ok(loginUser);
    }

    /** ログイン中のユーザ (未ログインは LoginInterceptor が 401) */
    @GetMapping("/me")
    public LoginUser me(HttpSession session) {
        return (LoginUser) session.getAttribute(LoginInterceptor.LOGIN_USER);
    }

    /** ログアウト。セッションを破棄する (画面は /login へ遷移) */
    @PostMapping("/logout")
    public Map<String, String> logout(HttpServletRequest request) {
        HttpSession session = request.getSession(false);
        if (session != null) {
            session.invalidate();
        }
        return Map.of("redirect", "/login");
    }
}
