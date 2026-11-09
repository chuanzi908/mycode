package com.lab.emp.common;

/**
 * 业务异常：由业务层主动抛出，交给全局异常处理器转成 Result。
 */
public class BusinessException extends RuntimeException {

    private static final long serialVersionUID = 1L;

    public BusinessException(String message) {
        super(message);
    }
}
