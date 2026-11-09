package com.lab.emp.controller;

import com.lab.emp.common.Result;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * 整合验证用的临时接口。
 * 4.4 节用它验证「请求链路是否畅通」：浏览器访问 /hello 能返回 ok，
 * 说明 DispatcherServlet、组件扫描、消息转换器这条链路都是通的。
 * 正式功能开发完成后可以按报告要求删除本类。
 */
@RestController
public class SystemController {

    @GetMapping("/hello")
    public String hello() {
        return "ok";
    }

    /** 返回 JSON 版本，用来验证 Jackson 消息转换器 */
    @GetMapping("/hello.json")
    public Result<String> helloJson() {
        return Result.ok("hello");
    }
}
