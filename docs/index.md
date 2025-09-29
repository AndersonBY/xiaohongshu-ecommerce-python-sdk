# 小红书电商 Python SDK

欢迎使用小红书(XiaoHongShu)电商平台 Python SDK！

## 简介

本 SDK 为小红书电商开放平台提供完整的 Python 接口，支持商品管理、订单处理、库存同步、售后服务等全套电商功能。SDK 基于官方 API 文档构建，提供类型安全的接口和详细的文档说明。

## 特性

- 🚀 **完整的 API 覆盖** - 支持 91 个官方 API 中的 88 个 (96.7% 覆盖率)
- 🔄 **自动Token管理** - 自动处理token获取、刷新和注入，零维护成本
- 📝 **详细的类型注解** - 完整的 TypeScript 风格类型提示
- 🛡️ **安全的认证** - 内置 OAuth 2.0 认证流程
- 🏗️ **模块化设计** - 按功能领域划分的客户端模块
- 📚 **丰富的文档** - 基于官方文档的详细 API 说明
- ✅ **生产就绪** - 经过充分测试和验证

## 支持的功能领域

| 模块 | 功能描述 | API 数量 |
|------|----------|----------|
| 🛍️ **商品管理** | 商品创建、更新、SKU 管理、价格控制 | 15 个 |
| 📦 **订单管理** | 订单查询、发货、跟踪、跨境清关 | 17 个 |
| 🔄 **售后服务** | 退换货、审核、拒绝原因管理 | 8 个 |
| 📊 **库存管理** | 多仓库存、同步、调整、仓库配置 | 11 个 |
| 💰 **财务管理** | 结算查询、账户流水、对账单下载 | 5 个 |
| 🚚 **物流快递** | 电子面单、批量取号、模板管理 | 6 个 |
| 🏪 **公共服务** | 分类属性、物流模板、地址服务 | 18 个 |
| 🎨 **素材中心** | 数字资产、文件上传、元数据管理 | 4 个 |
| ⚡ **即时零售** | 实时配送、骑手跟踪、位置更新 | 2 个 |
| ✨ **精品模式** | 精品商品、跨境配送、税费处理 | 6 个 |

## 快速开始

### 安装

```bash
pip install xiaohongshu-ecommerce
```

### 基本使用

```python
from xiaohongshu_ecommerce import XhsClient, ClientConfig, FileTokenStorage

# 初始化客户端（自动token管理）
config = ClientConfig(
    app_id="your_app_id",
    app_secret="your_app_secret",
    base_url="https://openapi.xiaohongshu.com",
    version="1.0",
    token_storage=FileTokenStorage("tokens.json")
)
client = XhsClient.create(config)

# 一次性设置token
client.set_tokens_from_auth_code("authorization_code")

# 🚀 API调用无需access_token参数！
products = client.product.get_detail_sku_list(
    page_no=1,
    page_size=50
)

orders = client.order.get_order_list(
    page_no=1,
    page_size=20
)
```

## 文档导航

- [📖 快速开始](quickstart.md) - 安装配置和基本使用
- [🔄 自动Token管理](auto-token-management.md) - 自动token管理详细指南
- [🔧 API 参考](api/client.md) - 完整的 API 接口文档
- [💡 示例代码](examples.md) - 常见场景的示例代码
- [📝 更新日志](changelog.md) - 版本更新和变更记录

## 贡献与支持

如果您在使用过程中遇到问题或有改进建议，欢迎提交 Issue 或 Pull Request。

---

*本 SDK 基于小红书开放平台官方 API 文档构建，确保与平台功能的完整兼容性。*