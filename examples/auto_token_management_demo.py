"""示例：自动Token管理使用演示"""

from xiaohongshu_ecommerce import (
    XhsClient,
    ClientConfig,
    FileTokenStorage,
    MemoryTokenStorage,
    TokenManagerError,
)


def example_auto_token_management():
    """演示自动token管理的使用方式"""

    print("=== 小红书电商SDK - 全自动Token管理示例 ===\n")

    # 1. 配置客户端（默认启用自动token管理）
    print("1. 配置客户端...")
    config = ClientConfig(
        base_url="https://openapi.xiaohongshu.com",
        app_id="your_app_id",
        app_secret="your_app_secret",
        token_storage=FileTokenStorage("example_tokens.json"),  # 文件存储
        token_refresh_buffer_seconds=300,  # 提前5分钟刷新
    )

    client = XhsClient.create(config)
    print("✅ 客户端配置完成（自动token管理已启用）")

    # 2. 设置初始token（仅需一次）
    print("\n2. 设置初始token...")
    try:
        # 方式一：使用授权码（推荐）
        auth_code = input("请输入授权码（或按回车跳过演示）: ").strip()
        if auth_code:
            tokens = client.set_tokens_from_auth_code(auth_code)
            print(f"✅ Token设置成功，商家: {tokens.seller_name}")
        else:
            # 方式二：演示手动设置（仅用于演示）
            print("⚠️  演示模式：手动设置token...")
            client.set_tokens_manually(
                access_token="demo_access_token",
                refresh_token="demo_refresh_token",
                access_token_expires_at=1640995200000,
                refresh_token_expires_at=1641081600000,
                seller_id="demo_seller",
                seller_name="演示商家",
            )
            print("✅ 演示token设置完成")
    except Exception as e:
        print(f"❌ Token设置失败: {e}")
        return

    # 3. 检查token状态
    print("\n3. 检查token状态...")
    if client.is_token_valid():
        tokens = client.get_current_tokens()
        print("✅ Token有效")
        print(f"   商家: {tokens.seller_name}")
        print(f"   商家ID: {tokens.seller_id}")
        print(f"   访问token剩余: {tokens.access_token_expires_in_seconds}秒")
        print(f"   刷新token剩余: {tokens.refresh_token_expires_in_seconds}秒")
    else:
        print("❌ Token无效或已过期")
        return

    # 4. 使用API - 无需手动传递token！
    print("\n4. 调用API（完全无需access_token参数）...")

    try:
        # 🎉 不需要传递access_token参数！
        print("   获取商品列表...")
        products = client.product.get_detail_sku_list(
            page_no=1, page_size=5, buyable=True
        )

        if products.success:
            print(
                f"   ✅ 获取商品成功，找到 {len(products.data.get('data', []))} 个商品"
            )
        else:
            print(f"   ❌ 获取商品失败: {products.error_message}")

        print("   获取订单列表...")
        orders = client.order.get_order_list(page_no=1, page_size=5)

        if orders.success:
            order_list = orders.data.order_list or []
            print(f"   ✅ 获取订单成功，找到 {len(order_list)} 个订单")
        else:
            print(f"   ❌ 获取订单失败: {orders.error_message}")

    except TokenManagerError as e:
        print(f"   ❌ Token管理错误: {e}")
        print("      请检查token是否有效或重新授权")
    except Exception as e:
        print(f"   ❌ API调用失败: {e}")

    # 5. Token管理操作
    print("\n5. Token管理操作...")

    # 检查是否需要刷新
    tokens = client.get_current_tokens()
    if tokens and tokens.should_refresh(buffer_seconds=3600):  # 1小时内过期
        print("   ⚠️  Token将在1小时内过期，建议刷新")
    else:
        print("   ✅ Token状态良好，无需刷新")

    # 演示清除token
    print("\n6. 清理演示...")
    choice = input("是否清除演示token？(y/N): ").strip().lower()
    if choice == "y":
        client.clear_tokens()
        print("   ✅ Token已清除")
    else:
        print("   ℹ️  Token保留，下次运行可继续使用")

    print("\n=== 演示完成 ===")


def example_memory_storage():
    """演示内存存储的使用"""

    print("\n=== 内存存储示例 ===")

    config = ClientConfig(
        base_url="https://openapi.xiaohongshu.com",
        app_id="your_app_id",
        app_secret="your_app_secret",
        token_storage=MemoryTokenStorage(),  # 使用内存存储
    )

    _client = XhsClient.create(config)  # Create client but mark as intentionally unused
    print("✅ 使用内存存储的客户端创建成功")
    print("ℹ️  注意：内存存储的token在程序重启后会丢失")


def example_custom_storage():
    """演示自定义存储的实现"""

    print("\n=== 自定义存储示例 ===")

    from xiaohongshu_ecommerce.token_manager import TokenStorage, TokenInfo
    from typing import Optional
    import json
    import os

    class DatabaseTokenStorage(TokenStorage):
        """模拟数据库存储"""

        def __init__(self, user_id: str):
            self.user_id = user_id
            self.db_file = f"user_{user_id}_tokens.json"

        def load_tokens(self) -> Optional[TokenInfo]:
            """从模拟数据库加载token"""
            if not os.path.exists(self.db_file):
                return None

            try:
                with open(self.db_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return TokenInfo(**data)
            except Exception:
                return None

        def save_tokens(self, tokens: TokenInfo) -> None:
            """保存token到模拟数据库"""
            from dataclasses import asdict

            with open(self.db_file, "w", encoding="utf-8") as f:
                json.dump(asdict(tokens), f, ensure_ascii=False, indent=2)

        def clear_tokens(self) -> None:
            """清除token"""
            if os.path.exists(self.db_file):
                os.remove(self.db_file)

    # 使用自定义存储
    config = ClientConfig(
        base_url="https://openapi.xiaohongshu.com",
        app_id="your_app_id",
        app_secret="your_app_secret",
        token_storage=DatabaseTokenStorage(user_id="user123"),
    )

    _client = XhsClient.create(config)  # Create client but mark as intentionally unused
    print("✅ 使用自定义数据库存储的客户端创建成功")


def example_advanced_usage():
    """演示高级用法"""

    print("\n=== 高级用法示例 ===")

    # 多商家管理
    print("1. 多商家管理...")

    def create_seller_client(seller_id: str) -> XhsClient:
        """为不同商家创建独立的客户端"""
        config = ClientConfig(
            base_url="https://openapi.xiaohongshu.com",
            app_id="your_app_id",
            app_secret="your_app_secret",
            token_storage=FileTokenStorage(f"seller_{seller_id}_tokens.json"),
        )
        return XhsClient.create(config)

    _seller1_client = create_seller_client(
        "seller_001"
    )  # Create but mark as intentionally unused
    _seller2_client = create_seller_client(
        "seller_002"
    )  # Create but mark as intentionally unused
    print("✅ 为多个商家创建了独立的客户端")

    # 并发安全演示
    print("\n2. 并发安全...")

    def fetch_products(client, page_no):
        """获取指定页的商品数据"""
        return client.product.get_detail_sku_list(page_no=page_no, page_size=10)

    print("✅ SDK内置线程安全，可以安全地在多线程环境中使用")


if __name__ == "__main__":
    print("小红书电商SDK - 全自动Token管理演示\n")

    while True:
        print("请选择演示内容:")
        print("1. 完整自动token管理演示")
        print("2. 内存存储示例")
        print("3. 自定义存储示例")
        print("4. 高级用法示例")
        print("0. 退出")

        choice = input("\n请输入选择 (0-4): ").strip()

        if choice == "1":
            example_auto_token_management()
        elif choice == "2":
            example_memory_storage()
        elif choice == "3":
            example_custom_storage()
        elif choice == "4":
            example_advanced_usage()
        elif choice == "0":
            print("退出演示")
            break
        else:
            print("无效选择，请重试")

        print("\n" + "=" * 50 + "\n")
