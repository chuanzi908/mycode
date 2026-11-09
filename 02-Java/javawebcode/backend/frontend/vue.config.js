module.exports = {
  devServer: {
    port: 8081, // 固定端口，不与Tomcat冲突
    proxy: {
      '/backend': {
        target: 'http://localhost:8080', // 后端地址
        changeOrigin: true,
        pathRewrite: { '^/backend': '/backend' }
      }
    }
  }
}