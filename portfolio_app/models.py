from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
class AllAccount(models.Model):
    id = models.AutoField(primary_key=True)
    Bank_sbi_PD = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    FD_sbi_PD = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    Bank_sbi_VK = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    FD_sbi_VK = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    Bank_kotak_VK = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    FD_kotak_VK = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    Bank_sbi_RK = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    FD_sbi_RK = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    Bank_indian_SR = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    FD_indian_SR = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    Bank_kotak_SR = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    FD_kotak_SR = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    Bank_kotak_RK_Sav = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    FD_kotak_RK_Sav = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    Bank_kotak_RK_Curr = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    Bank_kotak_Aad = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    Bank_idfc_RK = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    FD_idfc_RK = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    lending = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    liquid_credit_due = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    lending_comm = models.CharField(max_length=50, default='')
    total_assets = models.DecimalField(max_digits=15, decimal_places=3, editable=False, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Sum all decimal fields to calculate the total assets
        self.total_assets = (
                self.Bank_sbi_PD + self.FD_sbi_PD +
                self.Bank_sbi_VK + self.FD_sbi_VK +
                self.Bank_sbi_RK + self.FD_sbi_RK +
                self.Bank_idfc_RK + self.FD_idfc_RK +
                self.Bank_indian_SR + self.FD_indian_SR +
                self.Bank_kotak_SR + self.FD_kotak_SR +
                self.Bank_kotak_RK_Sav + self.FD_kotak_RK_Sav +
                self.Bank_kotak_RK_Curr + self.Bank_kotak_Aad +
                self.lending - self.liquid_credit_due
        )
        super(AllAccount, self).save(*args, **kwargs)

    def __str__(self):
        return f'Account {self.pk} - Total Assets: {self.total_assets}'

class StockPortfolio(models.Model):
    id = models.AutoField(primary_key=True)
    UPX_balance = models.DecimalField(max_digits=15, decimal_places=3, default=Decimal('0'))
    UPX_MX_balance = models.DecimalField(max_digits=15, decimal_places=3, default=Decimal('0'))
    UPX_funds = models.DecimalField(max_digits=15, decimal_places=3, default=Decimal('0'))
    UPX_MX_funds = models.DecimalField(max_digits=15, decimal_places=3, default=Decimal('0'))
    UPX_holding = models.DecimalField(max_digits=15, decimal_places=3, default=Decimal('0'))
    Zerodha_balance = models.DecimalField(max_digits=15, decimal_places=3, default=Decimal('0'))
    Zerodha_MX_balance = models.DecimalField(max_digits=15, decimal_places=3, default=Decimal('0'))
    Zerodha_funds = models.DecimalField(max_digits=15, decimal_places=3, default=Decimal('0'))
    Zerodha_MX_funds = models.DecimalField(max_digits=15, decimal_places=3, default=Decimal('0'))
    Zerodha_holding = models.DecimalField(max_digits=15, decimal_places=3, default=Decimal('0'))
    paytm_balance = models.DecimalField(max_digits=15, decimal_places=3, default=Decimal('0'))
    paytm_funds = models.DecimalField(max_digits=15, decimal_places=3, default=Decimal('0'))
    paytm_holding = models.DecimalField(max_digits=15, decimal_places=3, default=Decimal('0'))
    total_assets = models.DecimalField(max_digits=15, decimal_places=3, editable=False, default=Decimal('0'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Calculate total_assets
        self.total_assets = (
                self.UPX_balance +
                self.UPX_MX_balance +
                self.UPX_funds +
                self.UPX_MX_funds +
                self.UPX_holding +
                self.Zerodha_balance +
                self.Zerodha_MX_balance +
                self.Zerodha_funds +
                self.Zerodha_MX_funds +
                self.Zerodha_holding +
                self.paytm_balance +
                self.paytm_funds +
                self.paytm_holding
        )
        super().save(*args, **kwargs)

class MutualFund(models.Model):
    FUND_TYPE_CHOICES = [
        ('EQUITY', 'Equity'),
        ('DEBT', 'Debt'),
        ('HYBRID', 'Hybrid'),
        ('LIQUID', 'Liquid'),
        ('INDEX', 'Index'),
        ('ELSS', 'ELSS'),
    ]

    PAN_USER_CHOICES = [
        ('RK', 'RK'),
        ('SS', 'SS'),
        ('VK', 'VK'),
        ('PD', 'PD'),
    ]

    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('CLOSED', 'Closed'),
        ('PENDING', 'Pending'),
    ]

    id = models.AutoField(primary_key=True)
    app = models.CharField(max_length=50, verbose_name="Application")
    pan_user = models.CharField(max_length=20, choices=PAN_USER_CHOICES, verbose_name="PAN User")
    fund_name = models.CharField(max_length=255, verbose_name="Fund Name")
    fund_type = models.CharField(max_length=20, choices=FUND_TYPE_CHOICES, verbose_name="Fund Type")
    investment_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Investment Amount")
    units_purchased = models.DecimalField(max_digits=12, decimal_places=4, default=0, verbose_name="Units Purchased")
    returns = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, default=0, verbose_name="Returns")
    cagr = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        verbose_name="CAGR (%)"
    )
    xirr = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True,
        validators=[MinValueValidator(-100.0), MaxValueValidator(100.0)],
        verbose_name="XIRR (%)"
    )
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, verbose_name="Status")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
        return f"{self.fund_name} ({self.pan_user})"

    def update_investment_amount(self):
        self.investment_amount = self.investments.aggregate(total=models.Sum('investment_amount'))['total'] or 0
        self.units_purchased = self.investments.aggregate(total=models.Sum('units_purchased'))['total'] or 0
        self.save()

class Investments(models.Model):
    id = models.AutoField(primary_key=True)
    INVESTMENT_TYPE_CHOICES = [
        ('Onetime', 'Onetime'),
        ('SIP', 'SIP'),
    ]
    fund = models.ForeignKey(MutualFund, on_delete=models.CASCADE, related_name='investments')
    investment_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Investment Amount")
    units_purchased = models.DecimalField(max_digits=12, decimal_places=4, default=0, verbose_name="Units Purchased")
    NAV = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    investment_date = models.DateTimeField(auto_now_add=True, verbose_name="Investment Date")
    investment_type = models.CharField(max_length=20, choices=INVESTMENT_TYPE_CHOICES, verbose_name="Investment Type")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
        return f"Investment in {self.fund.fund_name} ({self.investment_type})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.fund.update_investment_amount()