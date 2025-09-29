# 快速开始

本指南将帮助您快速上手小红书电商 Python SDK。

## 🎉 自动Token管理（零维护）

SDK采用全自动token管理，完全无需手动处理access_token！设置一次，终身使用。

### 快速体验

```python
from xiaohongshu_ecommerce import XhsClient, ClientConfig, FileTokenStorage

# 1. 配置客户端
config = ClientConfig(
    app_id="your_app_id",
    app_secret="your_app_secret",
    base_url="https://openapi.xiaohongshu.com",
    version="1.0",
    token_storage=FileTokenStorage("tokens.json")  # 可选：持久化存储
)
client = XhsClient.create(config)

# 2. 一次性设置token（通过授权码）
client.set_tokens_from_auth_code("your_authorization_code")

# 3. 🎉 调用API - 完全无需access_token参数！
products = client.product.get_detail_sku_list(
    page_no=1,
    page_size=20,
    buyable=True
)

orders = client.order.get_order_list(
    page_no=1,
    page_size=20
)

# SDK自动处理：
# ✅ token过期检测
# ✅ 自动刷新token
# ✅ 在请求中注入有效token
# ✅ 线程安全访问
```

**🚀 核心优势：**
- 🔄 自动刷新过期token，零维护
- 💾 支持多种存储方式（内存、文件、自定义）
- 🛡️ 线程安全，支持并发
- ⚡ 零学习成本，开箱即用

---

## 安装

### 使用 pip 安装

```bash
pip install xiaohongshu-ecommerce
```

### 使用 poetry 安装

```bash
poetry add xiaohongshu-ecommerce
```

### 使用 pdm 安装

```bash
pdm add xiaohongshu-ecommerce
```

## 配置认证

### 获取应用凭证

1. 登录小红书开放平台控制台
2. 创建应用并获取 `app_id` 和 `app_secret`
3. 配置应用权限和回调地址

### 初始化客户端

```python
from xiaohongshu_ecommerce.client import XhsClient
from xiaohongshu_ecommerce.config import ClientConfig

# 初始化客户端
config = ClientConfig(
    app_id="your_app_id",
    app_secret="your_app_secret",
    base_url="https://openapi.xiaohongshu.com",  # 生产环境
    version="1.0"
)
client = XhsClient(config=config)
```

### OAuth 授权流程

小红书电商API使用OAuth 2.0授权码模式进行认证，支持Web端和移动端两种授权方式。

```python
# 方式1: Web端授权流程
# 1. 构建授权链接，引导用户访问
auth_url = f"https://ark.xiaohongshu.com/ark/authorization?appId={config.app_id}&redirectUri=https://your-domain.com/callback&state=12345"
print(f"请访问授权链接: {auth_url}")

# 2. 用户完成授权后，授权码会回调到 redirectUri
# 回调格式: https://your-domain.com/callback?code=74afa4f59c404***089e9db87797d6cc&state=12345

# 3. 使用授权码设置token（一次性操作）
authorization_code = "code-9e28279***e6035dc686e0-7aaea***841f3b32"  # 从回调获得的授权码

tokens = client.set_tokens_from_auth_code(authorization_code)
print(f"商家 {tokens.seller_name} (ID: {tokens.seller_id}) 授权成功")
print(f"令牌过期时间: {tokens.access_token_expires_at}")

# 🎉 从此以后，所有API调用都无需传递access_token！
```

```python
# 方式2: 移动端授权流程（二维码）
# 生成二维码供小红书千帆APP扫码授权
qr_auth_url = f"https://ark.xiaohongshu.com/thor/open/authorization?fullscreen=true&appId={config.app_id}&sellerId=your_seller_id&redirectUri=https://your-domain.com/callback"
print(f"生成二维码内容: {qr_auth_url}")
# 用户扫码后同样会回调授权码，后续流程相同
```

#### Token状态管理

```python
# 检查token是否有效
if client.is_token_valid():
    print("Token有效，可以正常使用API")
else:
    print("Token无效或已过期，请重新授权")

# 获取当前token信息
tokens = client.get_current_tokens()
if tokens:
    print(f"商家: {tokens.seller_name}")
    print(f"过期时间: {tokens.access_token_expires_in_seconds}秒后")
    print(f"是否需要刷新: {tokens.should_refresh()}")

# 手动清除token（如果需要切换商家）
client.clear_tokens()
```

**重要说明:**
- 只允许店铺主账号授权，子账号无法完成授权
- 授权码有效期10分钟，过期需重新授权
- 访问令牌有效期7天，刷新令牌有效期14天
- SDK会自动在到期前刷新，无需手动处理

## 基础使用示例

### 商品管理

```python
# 查询商品列表 - 无需access_token参数！
response = client.product.get_detail_sku_list(
    page_no=1,
    page_size=20,
    buyable=True  # 只查询在售商品
)

if response.success:
    products = response.data.get("data", [])
    print(f"找到 {len(products)} 个商品")

    for product in products:
        item = product.get("item", {})
        sku = product.get("sku", {})
        print(f"商品: {item.get('name')}, 价格: {sku.get('price', 0)/100:.2f}元, 库存: {sku.get('stock', 0)}")
else:
    print(f"查询失败: {response.error_message}")
```

### 订单管理

```python
# 查询订单列表 - 无需access_token参数！
response = client.order.get_order_list(
    page_no=1,
    page_size=20,
    order_status=3  # 已支付订单
)

if response.success:
    orders = response.data.order_list
    print(f"找到 {len(orders)} 个订单")

    for order in orders:
        print(f"订单号: {order.order_no}, 状态: {order.order_status}, 金额: {order.actual_amount/100:.2f}元")
else:
    print(f"查询失败: {response.error_message}")
```

### 库存管理

```python
# 查询 SKU 库存 - 无需access_token参数！
response = client.inventory.get_sku_stock(
    sku_id="your_sku_id"
)

if response.success:
    stock_info = response.data
    print(f"SKU: {stock_info.sku_id}, 库存: {stock_info.sku_stock.available}")
else:
    print(f"查询失败: {response.error_message}")
```

## 错误处理

```python
from xiaohongshu_ecommerce import TokenManagerError

try:
    response = client.product.get_detail_sku_list(
        page_no=1,
        page_size=20
    )

    if response.success:
        # 处理成功响应
        data = response.data
    else:
        # 处理业务错误
        print(f"业务错误: {response.error_code} - {response.error_message}")

except TokenManagerError as e:
    # 处理token相关错误
    print(f"Token错误: {e}")
    print("请检查token是否设置或重新授权")

except Exception as e:
    # 处理网络或其他异常
    print(f"系统异常: {e}")
```

## 最佳实践

### 1. 存储配置

```python
# 生产环境：使用文件存储
from xiaohongshu_ecommerce import FileTokenStorage

config = ClientConfig(
    app_id="your_app_id",
    app_secret="your_app_secret",
    base_url="https://openapi.xiaohongshu.com",
    token_storage=FileTokenStorage("./tokens/seller_tokens.json"),
    token_refresh_buffer_seconds=600  # 提前10分钟刷新，更安全
)

# 开发环境：使用内存存储
from xiaohongshu_ecommerce import MemoryTokenStorage

config = ClientConfig(
    app_id="your_app_id",
    app_secret="your_app_secret",
    base_url="https://openapi.xiaohongshu.com",
    token_storage=MemoryTokenStorage()  # 程序重启后需要重新授权
)
```

### 2. 分页查询

```python
def get_all_products(client):
    """获取所有商品"""
    all_products = []
    page_no = 1
    page_size = 50

    while True:
        response = client.product.get_detail_sku_list(
            page_no=page_no,
            page_size=page_size
        )

        if not response.success:
            print(f"查询失败: {response.error_message}")
            break

        products = response.data.get("data", [])
        all_products.extend(products)

        # 检查是否还有更多数据
        if len(products) < page_size:
            break

        page_no += 1

        # 避免过于频繁的请求
        time.sleep(0.1)

    return all_products
```

### 3. 批量操作

```python
def batch_update_inventory(client, updates, batch_size=20):
    """批量更新库存"""
    import time

    for i in range(0, len(updates), batch_size):
        batch = updates[i:i + batch_size]

        for update in batch:
            response = client.inventory.sync_sku_stock(
                sku_id=update["sku_id"],
                qty=update["qty"]
            )

            if response.success:
                print(f"SKU {update['sku_id']} 更新成功")
            else:
                print(f"SKU {update['sku_id']} 更新失败: {response.error_message}")

        # 批次间延迟
        time.sleep(0.5)
```

### 4. 多商家管理

```python
from xiaohongshu_ecommerce import FileTokenStorage

def create_seller_client(seller_id: str) -> XhsClient:
    """为不同商家创建独立的客户端"""
    config = ClientConfig(
        app_id="your_app_id",
        app_secret="your_app_secret",
        base_url="https://openapi.xiaohongshu.com",
        token_storage=FileTokenStorage(f"./tokens/seller_{seller_id}.json")
    )
    return XhsClient.create(config)

# 使用示例
seller1_client = create_seller_client("seller_001")
seller2_client = create_seller_client("seller_002")

# 每个客户端独立管理自己的token
seller1_client.set_tokens_from_auth_code("seller1_auth_code")
seller2_client.set_tokens_from_auth_code("seller2_auth_code")
```

### 5. 并发安全

```python
import threading
from concurrent.futures import ThreadPoolExecutor

def fetch_products(client, page_no):
    """获取指定页的商品数据"""
    return client.product.get_detail_sku_list(page_no=page_no, page_size=50)

# TokenManager内部使用锁，多线程安全
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = []
    for page in range(1, 11):  # 获取前10页
        future = executor.submit(fetch_products, client, page)
        futures.append(future)

    # 获取结果
    all_products = []
    for future in futures:
        result = future.result()
        if result.success:
            all_products.extend(result.data.get("data", []))
```

## 下一步

- 查看 [API 参考文档](api/client.md) 了解所有可用的接口
- 浏览 [示例代码](examples.md) 学习更多使用场景
- 阅读各个模块的详细文档了解具体功能