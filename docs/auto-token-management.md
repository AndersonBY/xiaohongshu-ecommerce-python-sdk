# 自动Token管理

小红书电商SDK采用**纯自动token管理**，完全消除了手动管理access_token的复杂性。所有API调用都会自动处理token的获取、刷新和注入！

## 特性

- 🔄 **全自动刷新** - token过期前自动刷新，完全无感知
- 💾 **灵活存储** - 支持内存、文件或自定义存储方式
- 🔒 **线程安全** - 多线程环境下安全使用
- ⚡ **零配置** - 默认内存存储，开箱即用
- 🚀 **纯自动** - 无需手动传递access_token参数

## 快速开始

### 1. 创建客户端

```python
from xiaohongshu_ecommerce import XhsClient, ClientConfig, FileTokenStorage

# 配置客户端（自动token管理始终启用）
config = ClientConfig(
    base_url="https://openapi.xiaohongshu.com",
    app_id="your_app_id",
    app_secret="your_app_secret",
    token_storage=FileTokenStorage("tokens.json"),  # 可选：持久化存储
    token_refresh_buffer_seconds=300  # 可选：提前5分钟刷新
)

client = XhsClient.create(config)
```

### 2. 设置初始Token

**方式一：使用授权码（推荐）**
```python
# 一次性设置，后续完全自动管理
tokens = client.set_tokens_from_auth_code("your_authorization_code")
print(f"设置成功，商家: {tokens.seller_name}")
```

**方式二：手动设置**
```python
# 如果已有完整token信息
client.set_tokens_manually(
    access_token="access_token_here",
    refresh_token="refresh_token_here",
    access_token_expires_at=1640995200000,  # 毫秒时间戳
    refresh_token_expires_at=1641081600000,  # 毫秒时间戳
    seller_id="seller123",
    seller_name="商家名称"
)
```

### 3. 使用API - 完全无需Token参数！

```python
# 🎉 所有API调用都不需要access_token参数!
products = client.product.get_detail_sku_list(
    page_no=1,
    page_size=20,
    buyable=True
)

orders = client.order.get_order_list(
    page_no=1,
    page_size=20,
    order_status=3
)

inventory = client.inventory.get_sku_stock_list(
    page_no=1,
    page_size=50
)

# SDK在每次API调用时自动处理：
# ✅ 检查token是否过期
# ✅ 自动刷新即将过期的token
# ✅ 在请求中自动注入有效token
# ✅ 处理token获取失败的情况
```

## 存储选项

### 内存存储（默认）
```python
from xiaohongshu_ecommerce import MemoryTokenStorage

config = ClientConfig(
    # ... 其他配置
    token_storage=MemoryTokenStorage()  # 或者不设置，默认使用内存存储
)

# 注意：内存存储的token在程序重启后会丢失
```

### 文件存储（推荐生产环境）
```python
from xiaohongshu_ecommerce import FileTokenStorage

config = ClientConfig(
    # ... 其他配置
    token_storage=FileTokenStorage("./config/tokens.json")
)
```

### 自定义存储
```python
from xiaohongshu_ecommerce.token_manager import TokenStorage, TokenInfo
from typing import Optional

class DatabaseTokenStorage:
    """自定义数据库存储实现"""

    def __init__(self, user_id: str):
        self.user_id = user_id

    def load_tokens(self) -> Optional[TokenInfo]:
        # 从数据库加载token
        data = self.db.query("SELECT * FROM tokens WHERE user_id = ?", [self.user_id])
        if data:
            return TokenInfo(**data)
        return None

    def save_tokens(self, tokens: TokenInfo) -> None:
        # 保存token到数据库
        from dataclasses import asdict
        self.db.save("tokens", asdict(tokens))

    def clear_tokens(self) -> None:
        # 清除token
        self.db.delete("tokens", user_id=self.user_id)

# 使用自定义存储
config = ClientConfig(
    # ... 其他配置
    token_storage=DatabaseTokenStorage(user_id="user123")
)
```

## 高级用法

### Token状态管理

```python
# 检查token是否有效
if client.is_token_valid():
    print("Token有效，可以进行API调用")
else:
    print("Token无效或已过期，需要重新设置")

# 获取当前token信息
tokens = client.get_current_tokens()
if tokens:
    print(f"商家: {tokens.seller_name}")
    print(f"商家ID: {tokens.seller_id}")
    print(f"访问token剩余: {tokens.access_token_expires_in_seconds}秒")
    print(f"刷新token剩余: {tokens.refresh_token_expires_in_seconds}秒")
    print(f"是否需要刷新: {tokens.should_refresh(buffer_seconds=3600)}")

# 手动清除token（比如用户退出登录）
client.clear_tokens()
```

### 自动授权码提供

```python
def get_auth_code() -> str:
    """当refresh token也过期时，自动获取新的授权码"""
    # 可以是用户输入、从配置文件读取、调用其他API等
    return input("请输入新的授权码: ")

config = ClientConfig(
    # ... 其他配置
    auth_code_provider=get_auth_code  # 当所有token都过期时自动调用
)
```

### 错误处理

```python
from xiaohongshu_ecommerce import TokenManagerError

try:
    products = client.product.get_detail_sku_list(page_no=1, page_size=20)

    if products.success:
        print(f"获取到 {len(products.data.get('data', []))} 个商品")
    else:
        print(f"API调用失败: {products.error_message}")

except TokenManagerError as e:
    print(f"Token管理错误: {e}")
    # 可能需要重新授权
    tokens = client.set_tokens_from_auth_code(input("请输入新的授权码: "))
    print(f"重新设置token成功: {tokens.seller_name}")

except Exception as e:
    print(f"其他错误: {e}")
```

## 最佳实践

### 1. 生产环境配置

```python
import os
from xiaohongshu_ecommerce import XhsClient, ClientConfig, FileTokenStorage

# 从环境变量读取配置
config = ClientConfig(
    base_url=os.getenv("XHS_BASE_URL", "https://openapi.xiaohongshu.com"),
    app_id=os.getenv("XHS_APP_ID"),
    app_secret=os.getenv("XHS_APP_SECRET"),
    token_storage=FileTokenStorage(os.getenv("XHS_TOKEN_FILE", "./tokens.json")),
    token_refresh_buffer_seconds=600  # 提前10分钟刷新，更安全
)

client = XhsClient.create(config)

# 初始化时设置token（通常在应用启动时执行一次）
if not client.is_token_valid():
    auth_code = os.getenv("XHS_AUTH_CODE")
    if auth_code:
        client.set_tokens_from_auth_code(auth_code)
    else:
        print("需要设置XHS_AUTH_CODE环境变量")
```

### 2. 多商家支持

```python
from xiaohongshu_ecommerce import FileTokenStorage

def create_seller_client(seller_id: str) -> XhsClient:
    """为不同商家创建独立的客户端"""
    config = ClientConfig(
        base_url="https://openapi.xiaohongshu.com",
        app_id="your_app_id",
        app_secret="your_app_secret",
        token_storage=FileTokenStorage(f"./tokens/seller_{seller_id}.json")
    )
    return XhsClient.create(config)

# 使用不同的客户端管理不同商家
seller1_client = create_seller_client("seller_001")
seller2_client = create_seller_client("seller_002")

# 每个客户端独立管理各自的token
seller1_client.set_tokens_from_auth_code("seller1_auth_code")
seller2_client.set_tokens_from_auth_code("seller2_auth_code")

# 独立使用，互不影响
seller1_products = seller1_client.product.get_detail_sku_list(page_no=1, page_size=20)
seller2_orders = seller2_client.order.get_order_list(page_no=1, page_size=20)
```

### 3. 并发安全

```python
import threading
from concurrent.futures import ThreadPoolExecutor

# TokenManager内部使用锁，完全线程安全
def fetch_products(client, page_no):
    """获取指定页的商品数据"""
    return client.product.get_detail_sku_list(page_no=page_no, page_size=50)

def fetch_orders(client, page_no):
    """获取指定页的订单数据"""
    return client.order.get_order_list(page_no=page_no, page_size=50)

# 并发获取多页数据
with ThreadPoolExecutor(max_workers=10) as executor:
    # 同时获取商品和订单数据
    product_futures = [executor.submit(fetch_products, client, page) for page in range(1, 6)]
    order_futures = [executor.submit(fetch_orders, client, page) for page in range(1, 6)]

    # 获取结果
    all_products = []
    all_orders = []

    for future in product_futures:
        result = future.result()
        if result.success:
            all_products.extend(result.data.get("data", []))

    for future in order_futures:
        result = future.result()
        if result.success:
            all_orders.extend(result.data.get("order_list", []))

print(f"总共获取 {len(all_products)} 个商品，{len(all_orders)} 个订单")
```

### 4. 定时任务中的使用

```python
import time
import schedule
from xiaohongshu_ecommerce import XhsClient, ClientConfig, FileTokenStorage

# 创建长期运行的客户端
config = ClientConfig(
    base_url="https://openapi.xiaohongshu.com",
    app_id="your_app_id",
    app_secret="your_app_secret",
    token_storage=FileTokenStorage("./tokens.json"),
    token_refresh_buffer_seconds=1800  # 提前30分钟刷新
)

client = XhsClient.create(config)

def sync_products():
    """定时同步商品数据"""
    try:
        products = client.product.get_detail_sku_list(page_no=1, page_size=100)
        if products.success:
            # 处理商品数据
            print(f"同步了 {len(products.data.get('data', []))} 个商品")
        else:
            print(f"同步失败: {products.error_message}")
    except Exception as e:
        print(f"同步异常: {e}")

def sync_orders():
    """定时同步订单数据"""
    try:
        orders = client.order.get_order_list(page_no=1, page_size=100)
        if orders.success:
            order_list = orders.data.get("order_list", [])
            print(f"同步了 {len(order_list)} 个订单")
        else:
            print(f"订单同步失败: {orders.error_message}")
    except Exception as e:
        print(f"订单同步异常: {e}")

# 设置定时任务
schedule.every(10).minutes.do(sync_products)
schedule.every(5).minutes.do(sync_orders)

# 运行定时任务
print("启动定时同步服务...")
while True:
    schedule.run_pending()
    time.sleep(60)
```

## 重要说明

### 🚨 纯自动管理模式
从v2.0开始，SDK采用**纯自动token管理**模式：

- ✅ 所有API方法都**不再需要**`access_token`参数
- ✅ Token的获取、刷新、注入完全自动化
- ✅ 开发者只需要专注业务逻辑

### 🔧 初始化要求
在使用任何API之前，必须先设置token：

```python
# 方式一：使用授权码（推荐）
client.set_tokens_from_auth_code("your_auth_code")

# 方式二：手动设置完整token信息
client.set_tokens_manually(
    access_token="...",
    refresh_token="...",
    access_token_expires_at=...,
    refresh_token_expires_at=...,
    seller_id="...",
    seller_name="..."
)
```

### 📱 授权流程

**Web端授权：**
1. 引导用户访问：`https://ark.xiaohongshu.com/ark/authorization?appId=xxx&redirectUri=xxx&state=xxx`
2. 用户授权后获取code：`https://your-callback-url/?code=xxx&state=xxx`
3. 使用code设置token：`client.set_tokens_from_auth_code(code)`

**移动端授权：**
1. 生成二维码：`https://ark.xiaohongshu.com/thor/open/authorization?fullscreen=true&appId=xxx&sellerId=xxx&redirectUri=xxx`
2. 小红书千帆APP扫码授权
3. 获取code并设置token

## 常见问题

**Q: 如何处理token过期？**
A: SDK会自动处理。当access token即将过期时，会自动使用refresh token刷新。当refresh token也过期时，会抛出TokenManagerError，需要重新授权。

**Q: 多进程环境下如何使用？**
A: 建议使用共享存储（如Redis）实现自定义TokenStorage，确保多进程间token同步。

**Q: 如何监控token状态？**
A: 可以定期调用`client.get_current_tokens()`检查token状态，并设置适当的日志记录。

**Q: 性能影响如何？**
A: 非常小。token检查是轻量级操作，只有在即将过期时才会触发网络请求进行刷新。

**Q: 是否支持多商家？**
A: 支持。为每个商家创建独立的客户端实例，使用不同的token存储路径。

通过纯自动token管理，您可以专注于业务逻辑，完全不用担心token相关的复杂性！