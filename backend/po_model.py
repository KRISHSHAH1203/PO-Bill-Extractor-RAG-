from pydantic import BaseModel, Field
from typing import List, Optional


class VendorInfo(BaseModel):
    """Vendor details for the PO or Bill document."""
    name: Optional[str] = Field(None, description="Vendor name", example="ABC Suppliers Pvt. Ltd.")
    address: Optional[str] = Field(None, description="Vendor address", example="123 Street, City, State, PIN")
    contact: Optional[str] = Field(None, description="Vendor contact info", example="+91-9876543210")


class BuyerInfo(BaseModel):
    """Buyer details in the document."""
    name: Optional[str] = Field(None, description="Buyer name", example="XYZ Corporation Ltd.")
    address: Optional[str] = Field(None, description="Buyer address", example="456 Road, City, State, PIN")
    contact: Optional[str] = Field(None, description="Buyer contact info", example="+91-9123456780")


class LineItem(BaseModel):
    """Individual line item in the PO or invoice."""
    name: Optional[str] = Field(None, description="Product or service name", example="Printer Cartridge")
    description: Optional[str] = Field(None, description="Line item description", example="Black Ink - HP 802")
    quantity: Optional[int] = Field(None, description="Quantity ordered", example=10)
    unit_price: Optional[float] = Field(None, description="Unit price of the item", example=150.00)
    total_price: Optional[float] = Field(None, description="Total price (quantity x unit price)", example=1500.00)


class POBillData(BaseModel):
    """
    Structured data extracted from a Purchase Order or Bill PDF.
    Fields include metadata, vendor/buyer info, addresses, line items, and totals.
    """
    po_number: Optional[str] = Field(None, description="Purchase Order number", example="PO-2023-4567")
    po_date: Optional[str] = Field(None, description="Date of the PO", example="2023-08-01")

    vendor: Optional[VendorInfo] = Field(None, description="Details of the vendor")
    buyer: Optional[BuyerInfo] = Field(None, description="Details of the buyer")

    shipping_address: Optional[str] = Field(None, description="Shipping address", example="789 Shipping Ln, State, PIN")
    billing_address: Optional[str] = Field(None, description="Billing address", example="321 Billing Rd, State, PIN")

    line_items: List[LineItem] = Field(default_factory=list, description="List of items in the PO or Bill")

    subtotal: Optional[float] = Field(None, description="Subtotal before tax", example=1500.00)
    tax: Optional[float] = Field(None, description="Tax amount", example=270.00)
    total_amount: Optional[float] = Field(None, description="Total amount including tax", example=1770.00)

    terms_and_conditions: Optional[str] = Field(None, description="Terms and conditions", example="Payment due in 30 days.")

    class Config:
        title = "POBillData"
        anystr_strip_whitespace = True  # Optional: trims whitespace from strings automatically
        extra = "forbid"  # Optional: forbids unknown fields in the parsed JSON to avoid silent errors
