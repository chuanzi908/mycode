package com.lab.emp.common;

import org.springframework.validation.BindException;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

/**
 * 全局异常处理：参数校验失败、业务异常、未知异常统一转为 Result。
 */
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(BusinessException.class)
    public Result<Void> handleBusiness(BusinessException e) {
        return Result.fail(e.getMessage());
    }

    @ExceptionHandler({MethodArgumentNotValidException.class, BindException.class})
    public Result<Void> handleValidation(Exception e) {
        FieldError fieldError = null;
        if (e instanceof MethodArgumentNotValidException) {
            fieldError = ((MethodArgumentNotValidException) e).getBindingResult().getFieldError();
        } else if (e instanceof BindException) {
            fieldError = ((BindException) e).getBindingResult().getFieldError();
        }
        String message = fieldError == null ? "参数校验失败" : fieldError.getDefaultMessage();
        return Result.fail(message);
    }

    @ExceptionHandler(Exception.class)
    public Result<Void> handleOther(Exception e) {
        e.printStackTrace();
        return Result.fail("系统繁忙，请稍后重试");
    }
}
