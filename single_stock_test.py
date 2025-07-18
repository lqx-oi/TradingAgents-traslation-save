# single_stock_test.py - 单只股票数据获取测试
# 运行代码
# python single_stock_test.py
import yfinance as yf
import pandas as pd
import os
import time
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

proxy = 'http://127.0.0.1:7890' # 代理设置，此处修改
os.environ['HTTP_PROXY'] = proxy
os.environ['HTTPS_PROXY'] = proxy

def test_single_stock(ticker="AAPL", days_back=30, output_dir="F:\\TradingAgents\\stock_data"):
    """
    测试单只股票数据获取
    """
    print("=" * 50)
    print(f"测试获取 {ticker} 股票数据")
    print("=" * 50)
    
    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"创建目录: {output_dir}")
    
    # 计算日期范围
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    
    print(f"股票代码: {ticker}")
    print(f"时间范围: {start_date_str} 到 {end_date_str}")
    print(f"获取天数: {days_back} 天")
    print("-" * 30)
    
    try:
        print("开始获取数据...")
        
        # 创建 yfinance Ticker 对象
        stock = yf.Ticker(ticker)
        
        # 先获取股票基本信息
        try:
            info = stock.info
            print(f"股票名称: {info.get('longName', 'N/A')}")
            print(f"当前价格: ${info.get('currentPrice', 'N/A')}")
            print(f"市场: {info.get('exchange', 'N/A')}")
        except:
            print("无法获取股票基本信息")
        
        print("\n获取历史数据...")
        
        # 获取历史数据
        data = stock.history(
            start=start_date_str,
            end=end_date_str,
            interval="1d",
            auto_adjust=True,
            prepost=False,
        )
        
        if data is not None and not data.empty:
            print(f"✓ 成功获取数据!")
            print(f"数据条数: {len(data)}")
            print(f"数据列: {list(data.columns)}")
            print(f"日期范围: {data.index[0].strftime('%Y-%m-%d')} 到 {data.index[-1].strftime('%Y-%m-%d')}")
            
            # 显示前几行数据
            print("\n前5行数据:")
            print(data.head())
            
            # 显示基本统计信息
            print(f"\n价格统计:")
            print(f"最高价: ${data['High'].max():.2f}")
            print(f"最低价: ${data['Low'].min():.2f}")
            print(f"平均收盘价: ${data['Close'].mean():.2f}")
            print(f"总成交量: {data['Volume'].sum():,}")
            
            # 保存到文件
            file_path = os.path.join(output_dir, f"{ticker}_test.csv")
            data.to_csv(file_path)
            print(f"\n✓ 数据已保存到: {file_path}")
            
            return True, data
            
        else:
            print("✗ 获取的数据为空")
            return False, None
            
    except Exception as e:
        print(f"✗ 获取数据时出错: {e}")
        return False, None

def test_multiple_methods(ticker="AAPL", days_back=30):
    """
    测试多种获取方法
    """
    print("=" * 60)
    print(f"测试多种方法获取 {ticker} 数据")
    print("=" * 60)
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    
    results = {}
    
    # 方法1: 标准 yfinance
    print("\n方法1: 标准 yfinance")
    print("-" * 30)
    try:
        stock = yf.Ticker(ticker)
        data1 = stock.history(start=start_date_str, end=end_date_str)
        if not data1.empty:
            results['method1'] = data1
            print(f"✓ 成功 - 获取 {len(data1)} 条数据")
        else:
            print("✗ 数据为空")
    except Exception as e:
        print(f"✗ 失败: {e}")
    
    time.sleep(3)  # 延迟3秒
    
    # 方法2: yfinance download
    print("\n方法2: yfinance download")
    print("-" * 30)
    try:
        data2 = yf.download(
            ticker, 
            start=start_date_str, 
            end=end_date_str,
            progress=False
        )
        if not data2.empty:
            results['method2'] = data2
            print(f"✓ 成功 - 获取 {len(data2)} 条数据")
        else:
            print("✗ 数据为空")
    except Exception as e:
        print(f"✗ 失败: {e}")
    
    time.sleep(3)  # 延迟3秒
    
    # 方法3: 尝试 akshare (如果可用)
    print("\n方法3: akshare")
    print("-" * 30)
    try:
        import akshare as ak
        start_ymd = start_date_str.replace("-", "")
        end_ymd = end_date_str.replace("-", "")
        
        data3 = ak.stock_us_hist(
            symbol=ticker,
            period="daily",
            start_date=start_ymd,
            end_date=end_ymd,
            adjust="qfq"
        )
        
        if not data3.empty:
            results['method3'] = data3
            print(f"✓ 成功 - 获取 {len(data3)} 条数据")
            print(f"列名: {list(data3.columns)}")
        else:
            print("✗ 数据为空")
    except ImportError:
        print("✗ akshare 未安装")
    except Exception as e:
        print(f"✗ 失败: {e}")
    
    # 比较结果
    print(f"\n结果汇总:")
    print("-" * 30)
    for method, data in results.items():
        print(f"{method}: {len(data)} 条数据")
    
    return results

def interactive_test():
    """
    交互式测试
    """
    print("股票数据获取测试工具")
    print("=" * 40)
    
    # 获取用户输入
    ticker = input("请输入股票代码 (默认 AAPL): ").strip().upper()
    if not ticker:
        ticker = "AAPL"
    
    days_input = input("请输入获取天数 (默认 30): ").strip()
    try:
        days_back = int(days_input) if days_input else 30
    except:
        days_back = 30
    
    print(f"\n开始测试 {ticker}，获取 {days_back} 天数据...")
    
    # 单一方法测试
    success, data = test_single_stock(ticker, days_back)
    
    if success:
        print(f"\n✓ 单一方法测试成功!")
        
        # 询问是否进行多方法测试
        multi_test = input("\n是否进行多方法对比测试? (y/n, 默认 n): ").strip().lower()
        if multi_test == 'y':
            test_multiple_methods(ticker, days_back)
    else:
        print(f"\n✗ 单一方法测试失败，尝试多方法测试...")
        test_multiple_methods(ticker, days_back)

def quick_test_popular_stocks():
    """
    快速测试几只热门股票
    """
    popular_stocks = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA"]
    
    print("快速测试热门股票")
    print("=" * 40)
    
    results = {}
    
    for ticker in popular_stocks:
        print(f"\n测试 {ticker}...")
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(period="5d")  # 只获取5天数据
            
            if not data.empty:
                results[ticker] = len(data)
                print(f"✓ {ticker}: {len(data)} 条数据")
            else:
                results[ticker] = 0
                print(f"✗ {ticker}: 无数据")
                
        except Exception as e:
            results[ticker] = -1
            print(f"✗ {ticker}: 错误 - {e}")
        
        time.sleep(2)  # 短延迟
    
    print(f"\n测试结果汇总:")
    print("-" * 20)
    for ticker, count in results.items():
        if count > 0:
            status = f"✓ {count} 条数据"
        elif count == 0:
            status = "✗ 无数据"
        else:
            status = "✗ 错误"
        print(f"{ticker}: {status}")

if __name__ == "__main__":
    print("选择测试模式:")
    print("1. 交互式测试 (推荐)")
    print("2. 快速测试热门股票")
    print("3. 直接测试 AAPL")
    
    choice = input("请选择 (1/2/3, 默认 1): ").strip()
    
    if choice == "2":
        quick_test_popular_stocks()
    elif choice == "3":
        test_single_stock("AAPL", 30)
    else:
        interactive_test()
    
    print("\n测试完成!")