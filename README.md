# xiaohongshu-ecommerce

[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

🚀 **小红书电商开放API的Python SDK**

## ✨ 特性

- 🔄 **全自动Token管理** - 自动获取、刷新、注入access_token，完全无感知
- 🏗️ **完整API覆盖** - 支持商品、订单、库存、物流、财务等全部电商API
- 💾 **灵活Token存储** - 支持内存、文件、数据库等多种存储方式
- 🔒 **线程安全设计** - 支持多线程并发，内置锁机制保证安全
- 🎯 **类型安全** - 完整的类型注解，支持IDE智能提示
- 📚 **详细文档** - 丰富的示例和API文档
- 🧪 **完整测试** - 高测试覆盖率，保证代码质量

## 📦 安装

```bash
pip install xiaohongshu-ecommerce
```

## 🚀 快速开始

### 1. 基础配置

```python
from xiaohongshu_ecommerce import XhsClient, ClientConfig, FileTokenStorage

# 创建客户端配置
config = ClientConfig(
    base_url="https://openapi.xiaohongshu.com",
    app_id="your_app_id",
    app_secret="your_app_secret",
    token_storage=FileTokenStorage("tokens.json")  # 持久化存储token
)

# 创建客户端
client = XhsClient.create(config)
```

### 2. 设置Token（仅需一次）

```python
# 方式一：使用授权码（推荐）
tokens = client.set_tokens_from_auth_code("your_authorization_code")
print(f"授权成功，商家：{tokens.seller_name}")

# 方式二：手动设置（如果已有token信息）
client.set_tokens_manually(
    access_token="your_access_token",
    refresh_token="your_refresh_token",
    access_token_expires_at=1640995200000,
    refresh_token_expires_at=1641081600000,
    seller_id="your_seller_id",
    seller_name="your_seller_name"
)
```

### 3. 使用API（完全无需传递Token！）

```python
# 🎉 所有API调用都无需access_token参数
# SDK会自动处理token的获取、刷新和注入

# 获取商品列表
products = client.product.get_detail_sku_list(
    page_no=1,
    page_size=20,
    buyable=True
)

if products.success:
    print(f"获取到 {len(products.data.get('data', []))} 个商品")
    for product in products.data.get('data', []):
        print(f"商品：{product.get('title')}")

# 获取订单列表
orders = client.order.get_order_list(
    page_no=1,
    page_size=20
)

if orders.success:
    order_list = orders.data.get('order_list', [])
    print(f"获取到 {len(order_list)} 个订单")

# 查询库存
inventory = client.inventory.get_sku_stock_list(
    page_no=1,
    page_size=50
)

# SDK自动处理：
# ✅ 检查token是否过期
# ✅ 自动刷新即将过期的token
# ✅ 在每个请求中自动注入有效token
# ✅ 处理token获取失败等异常情况
```

## 📋 支持的API模块

| 模块 | 说明 | 主要功能 |
|------|------|----------|
| `client.oauth` | OAuth认证 | 获取/刷新access_token |
| `client.product` | 商品管理 | 商品创建、更新、查询、上下架 |
| `client.order` | 订单管理 | 订单查询、发货、退款处理 |
| `client.inventory` | 库存管理 | 库存查询、更新、预警设置 |
| `client.finance` | 财务管理 | 账单查询、结算、提现 |
| `client.express` | 物流管理 | 快递单号、物流轨迹查询 |
| `client.after_sale` | 售后服务 | 退货退款、售后处理 |
| `client.data` | 数据分析 | 销售数据、流量分析 |
| `client.material` | 素材管理 | 图片、视频素材上传管理 |

## 🛠️ 高级用法

### 多商家支持

```python
def create_seller_client(seller_id: str) -> XhsClient:
    """为不同商家创建独立的客户端"""
    config = ClientConfig(
        base_url="https://openapi.xiaohongshu.com",
        app_id="your_app_id",
        app_secret="your_app_secret",
        token_storage=FileTokenStorage(f"./tokens/seller_{seller_id}.json")
    )
    return XhsClient.create(config)

# 使用独立客户端管理不同商家
seller1_client = create_seller_client("seller_001")
seller2_client = create_seller_client("seller_002")

# 独立设置各自的token
seller1_client.set_tokens_from_auth_code("seller1_auth_code")
seller2_client.set_tokens_from_auth_code("seller2_auth_code")
```

### 自定义Token存储

```python
from xiaohongshu_ecommerce.token_manager import TokenStorage, TokenInfo
from typing import Optional

class DatabaseTokenStorage:
    """数据库Token存储示例"""

    def __init__(self, user_id: str):
        self.user_id = user_id

    def load_tokens(self) -> Optional[TokenInfo]:
        # 从数据库加载token
        data = db.get_user_tokens(self.user_id)
        return TokenInfo(**data) if data else None

    def save_tokens(self, tokens: TokenInfo) -> None:
        # 保存token到数据库
        from dataclasses import asdict
        db.save_user_tokens(self.user_id, asdict(tokens))

    def clear_tokens(self) -> None:
        # 清除token
        db.delete_user_tokens(self.user_id)

# 使用自定义存储
config = ClientConfig(
    # ... 其他配置
    token_storage=DatabaseTokenStorage(user_id="user123")
)
```

### 错误处理

```python
from xiaohongshu_ecommerce import TokenManagerError

try:
    products = client.product.get_detail_sku_list(page_no=1, page_size=20)

    if products.success:
        print("获取商品成功")
    else:
        print(f"API错误：{products.error_message}")

except TokenManagerError as e:
    print(f"Token管理错误：{e}")
    # 需要重新授权
    client.set_tokens_from_auth_code(input("请输入新的授权码："))

except Exception as e:
    print(f"其他错误：{e}")
```

### 并发使用

```python
import threading
from concurrent.futures import ThreadPoolExecutor

def fetch_products(page_no):
    """获取指定页的商品"""
    return client.product.get_detail_sku_list(page_no=page_no, page_size=50)

# 并发获取多页数据（完全线程安全）
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(fetch_products, page) for page in range(1, 11)]

    all_products = []
    for future in futures:
        result = future.result()
        if result.success:
            all_products.extend(result.data.get("data", []))

print(f"总共获取 {len(all_products)} 个商品")
```

## 🔐 OAuth授权流程

### Web端授权

1. **引导用户访问授权页面：**
   ```
   https://ark.xiaohongshu.com/ark/authorization?appId={your_app_id}&redirectUri={your_redirect_uri}&state=12345
   ```

2. **用户授权后获取code：**
   ```
   https://your-callback-url/?code=xxx&state=12345
   ```

3. **使用code设置token：**
   ```python
   tokens = client.set_tokens_from_auth_code(code)
   ```

### 移动端授权

1. **生成二维码：**
   ```
   https://ark.xiaohongshu.com/thor/open/authorization?fullscreen=true&appId={your_app_id}&sellerId={seller_id}&redirectUri={your_redirect_uri}
   ```

2. **小红书千帆APP扫码授权**

3. **获取code并设置token**

## 📊 Token管理

```python
# 检查token状态
if client.is_token_valid():
    print("Token有效")

    # 获取token详细信息
    tokens = client.get_current_tokens()
    print(f"商家：{tokens.seller_name}")
    print(f"访问token剩余：{tokens.access_token_expires_in_seconds}秒")
    print(f"刷新token剩余：{tokens.refresh_token_expires_in_seconds}秒")

    # 检查是否需要刷新
    if tokens.should_refresh(buffer_seconds=3600):  # 1小时内过期
        print("建议刷新token")
else:
    print("Token无效，需要重新设置")

# 清除token（如用户退出登录）
client.clear_tokens()
```

## 🧪 开发和测试

### 环境要求

- Python 3.12+
- httpx >= 0.28.1

### 本地开发

```bash
# 克隆项目
git clone https://github.com/AndersonBY/xiaohongshu-ecommerce-python-sdk.git
cd xiaohongshu-ecommerce-python-sdk

# 安装依赖
pdm install

# 运行测试
pdm run pytest

# 代码检查
pdm run lint

# 类型检查
pdm run typecheck

# 代码格式化
pdm run format
```

### 运行示例

```bash
# 运行自动token管理示例
python examples/auto_token_management_demo.py
```

## 📝 更新日志

### v2.0.0
- 🎉 重大重构：采用纯自动token管理模式
- ❌ 移除所有手动access_token参数
- ✨ 新增灵活的token存储接口
- 🔒 增强线程安全性
- 📦 重命名包为 `xiaohongshu-ecommerce`

### v1.x.x
- 🏗️ 基础API客户端实现
- 🔧 手动token管理模式

## 🤝 贡献

欢迎提交Issue和Pull Request！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🔗 相关链接

- [小红书开放平台](https://developers.xiaohongshu.com/)
- [官方API文档](https://developers.xiaohongshu.com/docs/ecommerce)
- [问题反馈](https://github.com/AndersonBY/xiaohongshu-ecommerce-python-sdk/issues)

## ⭐ 支持项目

如果这个项目对你有帮助，请给一个 ⭐️ Star 支持一下！

---

**Made with ❤️ by [AndersonBY](https://github.com/AndersonBY)**