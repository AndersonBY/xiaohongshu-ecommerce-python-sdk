# 示例代码

本页提供了小红书电商 SDK 的常见使用场景和示例代码。

## 🎉 零Token管理体验

SDK采用全自动token管理，完全无需手动处理access_token！

### 基础配置

```python
from xiaohongshu_ecommerce import XhsClient, ClientConfig, FileTokenStorage

# 配置客户端
config = ClientConfig(
    base_url="https://openapi.xiaohongshu.com",
    app_id="your-app-id",
    app_secret="your-app-secret",
    version="1.0",
    token_storage=FileTokenStorage("tokens.json")  # 持久化存储
)

# 创建客户端实例
client = XhsClient.create(config)

# 一次性设置token
client.set_tokens_from_auth_code("your_authorization_code")

# 🎉 从此刻开始，所有API调用都无需access_token参数！
```

**🔄 自动管理优势：**
- ✅ 无需在每个API调用中传递access_token
- ✅ 自动检测token过期并刷新
- ✅ 支持多种存储方式（内存、文件、自定义）
- ✅ 线程安全，适合并发场景
- ✅ 零维护成本

## 商品管理示例

### 创建商品

```python
from xiaohongshu_ecommerce import XhsClient, ClientConfig, FileTokenStorage

# 配置客户端
config = ClientConfig(
    base_url="https://openapi.xiaohongshu.com",
    app_id="your-app-id",
    app_secret="your-app-secret",
    token_storage=FileTokenStorage("tokens.json")
)
client = XhsClient.create(config)

# 创建商品和 SKU - 无需access_token参数！
response = client.product.create_item_and_sku(
    # Item 基础信息
    name="精美口红套装",
    brand_id=12345,
    category_id="5a31****9df5",
    attributes=[
        {
            "propertyId": "color",
            "name": "颜色",
            "value": "红色",
            "valueId": "red_001"
        }
    ],
    images=[
        "https://img.example.com/lipstick1.jpg",
        "https://img.example.com/lipstick2.jpg"
    ],
    image_descriptions=[
        "https://img.example.com/detail1.jpg"
    ],
    shipping_template_id="template_123",
    # SKU 信息
    price=8800,  # 88.00 元（以分为单位）
    original_price=12800,  # 128.00 元
    stock=100,
    logistics_plan_id="logistics_456",
    variants=[
        {
            "id": "color_variant",
            "name": "颜色",
            "value": "魅力红",
            "valueId": "red_charm"
        }
    ],
    delivery_time={
        "type": "RELATIVE_TIME_NEW",
        "time": "24"  # 24小时内发货
    },
    barcode="6901234567890",
    description="高品质口红套装，持久显色"
)

if response.success:
    print(f"商品创建成功，Item ID: {response.data.item.id}")
    print(f"SKU ID: {response.data.sku.id}")
else:
    print(f"创建失败: {response.error_message}")
```

### 批量更新商品价格

```python
import time

def batch_update_prices(client, price_updates):
    """批量更新商品价格"""
    success_count = 0
    failed_count = 0

    for sku_id, new_price in price_updates.items():
        # 🎉 无需传递access_token！
        response = client.product.update_item_price(
            sku_id=sku_id,
            price=[{
                "skuId": sku_id,
                "price": int(new_price * 100)  # 转换为分
            }],
            original_price=int(new_price * 100 * 1.5)  # 市场价设为1.5倍
        )

        if response.success:
            success_count += 1
            print(f"SKU {sku_id} 价格更新成功: {new_price:.2f}元")
        else:
            failed_count += 1
            print(f"SKU {sku_id} 价格更新失败: {response.error_message}")

        # 避免请求过于频繁
        time.sleep(0.2)

    print(f"批量更新完成: 成功 {success_count} 个, 失败 {failed_count} 个")

# 使用示例
price_updates = {
    "sku_001": 88.00,
    "sku_002": 128.00,
    "sku_003": 168.00
}

batch_update_prices(client, price_updates)
```

## 订单管理示例

### 订单发货

```python
import time

def deliver_order(client, order_id, express_company_code, tracking_number):
    """订单发货"""
    response = client.order.order_deliver(
        order_id=order_id,
        express_company_code=express_company_code,
        express_no=tracking_number,
        delivering_time=int(time.time() * 1000)  # 当前时间戳（毫秒）
    )

    if response.success:
        print(f"订单 {order_id} 发货成功")
        return True
    else:
        print(f"订单 {order_id} 发货失败: {response.error_message}")
        return False

# 批量发货
orders_to_deliver = [
    {"order_id": "XHS2024001", "express_code": "SF", "tracking": "SF1234567890"},
    {"order_id": "XHS2024002", "express_code": "YTO", "tracking": "YT9876543210"},
]

for order_info in orders_to_deliver:
    deliver_order(
        client,
        order_info["order_id"],
        order_info["express_code"],
        order_info["tracking"]
    )
    time.sleep(1)  # 发货间隔
```

### 订单状态监控

```python
import time

def monitor_order_status(client):
    """监控订单状态变化"""
    # 查询最近24小时的订单
    end_time = int(time.time() * 1000)
    start_time = end_time - 24 * 60 * 60 * 1000

    response = client.order.get_order_list(
        page_no=1,
        page_size=50,
        start_time=start_time,
        end_time=end_time,
        time_type=1  # 创建时间
    )

    if response.success:
        orders = response.data.order_list

        status_counts = {}
        for order in orders:
            status = order.order_status
            status_counts[status] = status_counts.get(status, 0) + 1

        print("订单状态统计:")
        for status, count in status_counts.items():
            print(f"  状态 {status}: {count} 个")

        return orders
    else:
        print(f"查询失败: {response.error_message}")
        return []

# 定期监控
monitor_order_status(client)
```

### 订单发货

```python
import time

def deliver_order(order_id, express_company_code, tracking_number):
    """订单发货"""
    response = client.order.order_deliver(
        access_token,
        order_id=order_id,
        express_company_code=express_company_code,
        express_no=tracking_number,
        delivering_time=int(time.time() * 1000)  # 当前时间戳（毫秒）
    )

    if response.success:
        print(f"订单 {order_id} 发货成功")
        return True
    else:
        print(f"订单 {order_id} 发货失败: {response.error_message}")
        return False

# 批量发货
orders_to_deliver = [
    {"order_id": "XHS2024001", "express_code": "SF", "tracking": "SF1234567890"},
    {"order_id": "XHS2024002", "express_code": "YTO", "tracking": "YT9876543210"},
]

for order_info in orders_to_deliver:
    deliver_order(
        order_info["order_id"],
        order_info["express_code"],
        order_info["tracking"]
    )
    time.sleep(1)  # 发货间隔
```

### 订单状态监控

```python
import time

def monitor_order_status():
    """监控订单状态变化"""
    # 查询最近24小时的订单
    end_time = int(time.time() * 1000)
    start_time = end_time - 24 * 60 * 60 * 1000

    response = client.order.get_order_list(
        access_token,
        page_no=1,
        page_size=50,
        start_time=start_time,
        end_time=end_time,
        time_type=1  # 创建时间
    )

    if response.success:
        orders = response.data.order_list

        status_counts = {}
        for order in orders:
            status = order.order_status
            status_counts[status] = status_counts.get(status, 0) + 1

        print("订单状态统计:")
        for status, count in status_counts.items():
            print(f"  状态 {status}: {count} 个")

        return orders
    else:
        print(f"查询失败: {response.error_message}")
        return []

# 定期监控
monitor_order_status()
```

## 库存管理示例

### 库存预警系统

```python
def check_low_stock(threshold=10):
    """检查低库存商品"""
    low_stock_products = []
    page_no = 1

    while True:
        response = client.product.get_detail_sku_list(
            access_token,
            page_no=page_no,
            page_size=50,
            stock_lte=threshold,  # 库存小于等于阈值
            buyable=True  # 仍在销售
        )

        if not response.success:
            print(f"查询失败: {response.error_message}")
            break

        products = response.data.get("data", [])
        low_stock_products.extend(products)

        if len(products) < 50:
            break

        page_no += 1

    # 输出预警信息
    if low_stock_products:
        print(f"发现 {len(low_stock_products)} 个低库存商品:")
        for product in low_stock_products:
            item = product.get("item", {})
            sku = product.get("sku", {})
            print(f"  {item.get('name', 'Unknown')} (SKU: {sku.get('id', 'Unknown')}) - 剩余库存: {sku.get('stock', 0)}")
    else:
        print("所有商品库存充足")

    return low_stock_products

# 库存预警
low_stock_items = check_low_stock(threshold=5)
```

### 自动补货

```python
def auto_replenish_stock(replenish_rules):
    """根据规则自动补货"""
    replenish_list = []

    for sku_id, target_stock in replenish_rules.items():
        # 先查询当前库存
        response = client.product.get_detail_sku_list(
            access_token,
            id=sku_id
        )

        if response.success and response.data.get("data"):
            current_stock = response.data["data"][0]["sku"]["stock"]

            if current_stock < target_stock:
                replenish_qty = target_stock - current_stock
                replenish_list.append(sku_id)
                print(f"SKU {sku_id} 需要补货 {replenish_qty} 件 (当前: {current_stock}, 目标: {target_stock})")

                # 同步库存到目标数量
                sync_response = client.inventory.sync_sku_stock(
                    access_token,
                    sku_id=sku_id,
                    qty=target_stock
                )

                if sync_response.success:
                    print(f"  SKU {sku_id} 补货成功")
                else:
                    print(f"  SKU {sku_id} 补货失败: {sync_response.error_message}")

    print(f"补货处理完成，共处理 {len(replenish_list)} 个 SKU")

# 补货规则: SKU ID -> 目标库存
replenish_rules = {
    "sku_001": 50,
    "sku_002": 30,
    "sku_003": 20
}

auto_replenish_stock(replenish_rules)
```

## 售后管理示例

### 售后处理流程

```python
def process_after_sale_requests():
    """处理售后申请"""
    # 查询待处理的售后申请
    response = client.after_sale.list_after_sale_infos(
        access_token,
        page_no=1,
        page_size=20,
        statuses=[1]  # 待审核状态
    )

    if not response.success:
        print(f"查询售后申请失败: {response.error_message}")
        return

    after_sales = response.data.after_sale_basic_infos

    for after_sale in after_sales:
        print(f"处理售后申请: {after_sale.returns_id}")

        # 获取详细信息
        detail_response = client.after_sale.get_after_sale_info(
            access_token,
            returns_id=after_sale.returns_id
        )

        if not detail_response.success:
            print(f"  获取详情失败: {detail_response.error_message}")
            continue

        # 根据售后类型进行处理
        if after_sale.return_type == 1:  # 退货退款
            print(f"  处理退货退款申请")
            # 这里可以添加自动审核逻辑
        elif after_sale.return_type == 2:  # 换货
            print(f"  处理换货申请")
        else:
            print(f"  其他类型售后: {after_sale.return_type}")

process_after_sale_requests()
```

## 数据分析示例

### 销售数据分析

```python
from collections import defaultdict
from datetime import datetime
import time

def analyze_sales_data(days=7):
    """分析销售数据"""
    # 查询最近N天的订单
    end_time = int(time.time() * 1000)
    start_time = end_time - days * 24 * 60 * 60 * 1000

    all_orders = []
    page_no = 1

    while True:
        response = client.order.get_order_list(
            access_token,
            page_no=page_no,
            page_size=50,
            start_time=start_time,
            end_time=end_time,
            time_type=1,  # 创建时间
            order_status=3  # 已支付订单
        )

        if not response.success:
            break

        orders = response.data.order_list
        all_orders.extend(orders)

        if len(orders) < 50:
            break

        page_no += 1

    # 数据分析
    daily_sales = defaultdict(lambda: {"count": 0, "amount": 0})
    total_amount = 0

    for order in all_orders:
        # 按日期统计
        order_date = datetime.fromtimestamp(order.create_time / 1000).date()
        daily_sales[order_date]["count"] += 1
        daily_sales[order_date]["amount"] += order.actual_amount
        total_amount += order.actual_amount

    # 输出报告
    print(f"\n=== 最近 {days} 天销售报告 ===")
    print(f"总订单数: {len(all_orders)}")
    print(f"总销售额: {total_amount / 100:.2f} 元")

    print("\n每日销售:")
    for date, data in sorted(daily_sales.items()):
        print(f"  {date}: {data['count']} 单, {data['amount']/100:.2f} 元")

analyze_sales_data(days=7)
```

## 工具函数

### API 响应处理装饰器

```python
from functools import wraps

def handle_api_response(func):
    """API 响应处理装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)

            if response.success:
                return response.data
            else:
                print(f"API 调用失败: {response.error_code} - {response.error_message}")
                return None

        except Exception as e:
            print(f"系统异常: {e}")
            return None

    return wrapper

# 使用示例
@handle_api_response
def get_product_list(page_no=1, page_size=20):
    return client.product.get_detail_sku_list(
        access_token,
        page_no=page_no,
        page_size=page_size
    )

# 简化调用
products = get_product_list(1, 50)
if products:
    print(f"获取到 {len(products.get('data', []))} 个商品")
```

### 配置管理

```python
import os
from xiaohongshu_ecommerce.client import XhsClient
from xiaohongshu_ecommerce.config import ClientConfig
from dataclasses import dataclass

@dataclass
class XhsConfig:
    app_id: str
    app_secret: str
    base_url: str = "https://openapi.xiaohongshu.com"
    timeout: int = 30

    @classmethod
    def from_env(cls):
        """从环境变量加载配置"""
        return cls(
            app_id=os.getenv("XHS_APP_ID"),
            app_secret=os.getenv("XHS_APP_SECRET"),
            base_url=os.getenv("XHS_BASE_URL", "https://openapi.xiaohongshu.com"),
            timeout=int(os.getenv("XHS_TIMEOUT", "30"))
        )

# 使用配置
xhs_config = XhsConfig.from_env()
config = ClientConfig(
    app_id=xhs_config.app_id,
    app_secret=xhs_config.app_secret,
    base_url=xhs_config.base_url,
    version="1.0"
)
client = XhsClient(config=config)
```

这些示例展示了 SDK 在实际业务场景中的应用方式。您可以根据自己的业务需求调整和扩展这些代码。