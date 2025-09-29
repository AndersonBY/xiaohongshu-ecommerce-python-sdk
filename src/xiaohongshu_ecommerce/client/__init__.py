"""Synchronous clients for Xiaohongshu E-commerce APIs.

This module provides synchronous client implementations for all Xiaohongshu
(Little Red Book) e-commerce platform APIs. The clients are organized by
functional domain to provide intuitive access to various platform capabilities.

Available Clients:
    XhsClient: Main client providing access to all sub-clients
    OauthClient: Authentication and authorization management
    CommonClient: Common APIs for categories, attributes, logistics, etc.
    ProductClient: Product and inventory management (items, SKUs, pricing)
    OrderClient: Order lifecycle management and tracking
    AfterSaleClient: Returns, refunds, and after-sale service management
    InventoryClient: Stock management and warehouse operations
    FinanceClient: Financial operations, settlements, and billing
    PackageClient: Logistics and shipping management
    ExpressClient: Electronic waybill and express services
    MaterialClient: Digital asset and media management
    InvoiceClient: Electronic invoice management
    DeliveryVoucherClient: Shipping voucher and discount management
    InstantShoppingClient: Real-time delivery and instant shopping services
    BoutiqueClient: Premium product management with enhanced features
    DataClient: Data privacy, encryption, and security services

Usage:
    >>> from xiaohongshu_ecommerce.client import XhsClient
    >>> client = XhsClient(app_id="your_app_id", app_secret="your_secret")
    >>>
    >>> # Product management
    >>> products = client.product.get_detail_sku_list(request, access_token)
    >>>
    >>> # Order management
    >>> orders = client.order.get_order_list(request, access_token)
    >>>
    >>> # Inventory management
    >>> stock = client.inventory.get_sku_stock(request, access_token)

All clients follow consistent patterns:
    - Request/response model-based API calls
    - Comprehensive error handling and validation
    - Type hints for better IDE support
    - Detailed documentation with examples
    - OAuth 2.0 authentication support
"""

from .base import SyncSubClient, XhsClient
from .common import CommonClient
from .data import DataClient
from .inventory import InventoryClient
from .oauth import OauthClient
from .after_sale import AfterSaleClient
from .boutique import BoutiqueClient
from .product import ProductClient
from .order import OrderClient
from .package import PackageClient
from .express import ExpressClient
from .finance import FinanceClient
from .invoice import InvoiceClient
from .material import MaterialClient
from .delivery_voucher import DeliveryVoucherClient
from .instant_shopping import InstantShoppingClient

__all__ = [
    "XhsClient",
    "SyncSubClient",
    "OauthClient",
    "DataClient",
    "InventoryClient",
    "CommonClient",
    "AfterSaleClient",
    "BoutiqueClient",
    "ProductClient",
    "OrderClient",
    "PackageClient",
    "ExpressClient",
    "FinanceClient",
    "InvoiceClient",
    "MaterialClient",
    "DeliveryVoucherClient",
    "InstantShoppingClient",
]
