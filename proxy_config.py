# proxy_config.py - 通用代理配置文件
import os

def setup_proxy():
    """设置代理 - 在所有脚本开头调用这个函数"""
    
    # 常见代理软件的默认端口
    # 请根据你的代理软件选择对应的端口
    
    # Clash 代理设置
    proxy_url = "http://127.0.0.1:7890"
    
    # V2Ray 代理设置（如果你用的是V2Ray，取消下面的注释）
    # proxy_url = "http://127.0.0.1:10809"
    
    # Shadowsocks 代理设置（如果你用的是SS，取消下面的注释）
    # proxy_url = "http://127.0.0.1:1080"
    
    # 其他代理（请替换为你的代理地址和端口）
    # proxy_url = "http://你的代理IP:端口"
    
    # 设置环境变量
    os.environ['HTTP_PROXY'] = proxy_url
    os.environ['HTTPS_PROXY'] = proxy_url
    os.environ['http_proxy'] = proxy_url
    os.environ['https_proxy'] = proxy_url
    
    print(f"✓ 代理已设置: {proxy_url}")

def clear_proxy():
    """清除代理设置"""
    proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy']
    
    for var in proxy_vars:
        if var in os.environ:
            del os.environ[var]
    
    print("✓ 代理已清除")

# 自动设置代理（导入时就执行）
if __name__ != "__main__":
    setup_proxy()