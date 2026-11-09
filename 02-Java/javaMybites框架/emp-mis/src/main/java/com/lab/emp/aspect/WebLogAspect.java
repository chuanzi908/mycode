package com.lab.emp.aspect;

import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Pointcut;
import org.springframework.stereotype.Component;

import java.util.Arrays;

/**
 * 请求日志切面：记录 Controller 的入参、耗时与异常。
 */
@Aspect
@Component
public class WebLogAspect {

    @Pointcut("execution(* com.lab.emp.controller..*(..))")
    public void pointcut() {
    }

    @Around("pointcut()")
    public Object around(ProceedingJoinPoint joinPoint) throws Throwable {
        long start = System.currentTimeMillis();
        String method = joinPoint.getSignature().toShortString();
        System.out.println("[REQ] " + method + " 参数：" + Arrays.toString(joinPoint.getArgs()));
        try {
            Object result = joinPoint.proceed();
            System.out.println("[RESP] " + method + " 耗时：" + (System.currentTimeMillis() - start) + "ms");
            return result;
        } catch (Throwable t) {
            System.err.println("[ERR] " + method + " 异常：" + t.getMessage());
            throw t;
        }
    }
}
