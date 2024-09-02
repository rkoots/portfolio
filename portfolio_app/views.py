from django.shortcuts import render
from .models import *

from datetime import datetime, timedelta
from django.db.models import Sum

def portfolio_chart(request):
    return render(request, 'chart.html')

def portfolio_list(request):
    now = datetime.now()
    current_year = now.year
    current_month = now.month
    if current_month == 1:
        target_year = current_year - 1
        target_month = 12
    else:
        target_year = current_year
        target_month = current_month - 1

    mutual_funds = MutualFund.objects.all()
    transaction = Investments.objects.all()
    pan_summary = MutualFund.objects.values('pan_user').annotate(total_invested=Sum('investment_amount'),total_returns=Sum('returns')).order_by('pan_user')
    total_invested = MutualFund.objects.filter(status='ACTIVE').aggregate(total_invested=Sum('investment_amount'))
    total_returns = MutualFund.objects.filter(status='ACTIVE').aggregate(total_returns=Sum('returns'))
    total_invested_amount = total_invested['total_invested'] or 0
    total_return_amount = total_returns['total_returns'] or 0
    total_bank = AllAccount.objects.last()
    Stock_funds = StockPortfolio.objects.last()
    total_assets_all_account = total_bank.total_assets
    total_assets_stock_portfolio = Stock_funds.total_assets
    first_record_last_month_sp = StockPortfolio.objects.filter(created_at__year=target_year,created_at__month=target_month).first()
    first_record_last_month_aa =     AllAccount.objects.filter(created_at__year=target_year,created_at__month=target_month).first()
    first_record_last_month_investments = Investments.objects.filter(created_at__year=target_year,created_at__month=target_month).first()
    total_assets_sp_last_month = first_record_last_month_sp.total_assets if first_record_last_month_sp else Decimal('0')
    total_assets_aa_last_month = first_record_last_month_aa.total_assets if first_record_last_month_aa else Decimal('0')
    total_assets_investments_last_month = first_record_last_month_investments.investment_amount if first_record_last_month_investments else Decimal('0')
    total_investment_last_month = Investments.objects.filter(investment_date__year=target_year, investment_date__month=target_month).aggregate(total_invested_last=Sum('investment_amount'))['total_invested_last'] or Decimal('0')
    total_ret_last_month = Investments.objects.filter(investment_date__year=target_year,investment_date__month=target_month).aggregate(total_return_last=Sum('investment_amount'))['total_return_last'] or Decimal('0')
    sav_bank = (
            total_bank.Bank_kotak_RK_Sav +
            total_bank.Bank_kotak_RK_Curr +
            total_bank.Bank_kotak_Aad +
            total_bank.Bank_idfc_RK +
            total_bank.Bank_sbi_RK +
            total_bank.Bank_sbi_PD +
            total_bank.Bank_sbi_VK +
            total_bank.Bank_kotak_VK +
            total_bank.Bank_indian_SR +
            total_bank.Bank_kotak_SR
    )
    fd_bank = (
        total_bank.FD_sbi_PD +
        total_bank.FD_sbi_VK +
        total_bank.FD_kotak_VK +
        total_bank.FD_sbi_RK +
        total_bank.FD_indian_SR +
        total_bank.FD_kotak_SR +
        total_bank.FD_kotak_RK_Sav +
        total_bank.FD_idfc_RK
    )
    rk_bank = (
        total_bank.Bank_sbi_RK +
        total_bank.Bank_kotak_RK_Sav +
        total_bank.Bank_kotak_RK_Curr +
        total_bank.Bank_idfc_RK +
        total_bank.Bank_sbi_RK +
        total_bank.FD_sbi_RK +
        total_bank.FD_kotak_RK_Sav +
        total_bank.FD_idfc_RK
    )
    sr_bank = (
        total_bank.Bank_indian_SR +
        total_bank.Bank_kotak_SR +
        total_bank.Bank_kotak_Aad +
        total_bank.FD_indian_SR +
        total_bank.FD_kotak_SR
    )
    vk_bank = (
        total_bank.Bank_sbi_VK +
        total_bank.Bank_kotak_VK +
        total_bank.FD_sbi_VK +
        total_bank.FD_kotak_VK
    )
    pd_bank = total_bank.Bank_sbi_PD + total_bank.FD_sbi_PD
    stx_upx = Stock_funds.UPX_MX_balance + Stock_funds.UPX_balance + Stock_funds.UPX_funds + Stock_funds.UPX_MX_funds
    stx_ptm = Stock_funds.paytm_balance + Stock_funds.paytm_funds
    stx_z = Stock_funds.Zerodha_balance + Stock_funds.Zerodha_MX_balance + Stock_funds.Zerodha_funds + Stock_funds.Zerodha_MX_funds
    denominator = Decimal('0.001') + total_assets_investments_last_month + total_assets_sp_last_month + total_assets_aa_last_month
    if denominator == Decimal('0'):
        growth_monthly = Decimal('0')
    else:
        growth_monthly = ((total_return_amount + total_assets_all_account + total_assets_stock_portfolio) - (total_assets_investments_last_month + total_assets_sp_last_month + total_assets_aa_last_month)) * Decimal('100') / denominator

    return render(request, 'index.html', {
        'mutual_funds': mutual_funds,
        'RK_bank': round(rk_bank,1),
        'SR_bank': round(sr_bank,1),
        'VK_bank': round(vk_bank,1),
        'PD_bank': round(pd_bank,1),
        'SAV_bank': round(sav_bank,1),
        'FD_bank': round(fd_bank,1),
        'total_bank': total_bank,
        'Stock_funds': Stock_funds,
        'pan_summary' : pan_summary,
        'stx_upx' : round(stx_upx,1),
        'stx_ptm' : round(stx_ptm,1),
        'stx_z' : round(stx_z,1),
        'hold_z' : round(Stock_funds.Zerodha_holding,1),
        'hold_upx' : round(Stock_funds.UPX_holding,1),
        'hold_ptm' : round(Stock_funds.paytm_holding,1),
        'Total_bank_asset': total_bank.total_assets,
        'Total_bank_asset_date':total_bank.created_at,
        'Total_stock_asset' : Stock_funds.total_assets,
        'Total_stock_asset_date' : Stock_funds.created_at,
        'Total_mf_asset' : total_invested_amount,
        'Total_mf_asset_return' : total_return_amount,
        'total_assets_all_account':total_assets_all_account,
        'total_assets_stock_portfolio':total_assets_stock_portfolio,
        'total_assets_sp_last_month':total_assets_sp_last_month,
        'total_assets_aa_last_month':total_assets_aa_last_month,
        'total_assets_investments_last_month': total_assets_investments_last_month,
        'CM': total_return_amount + total_assets_all_account + total_assets_stock_portfolio,
        'LM': total_assets_investments_last_month +  total_assets_sp_last_month +  total_assets_aa_last_month,
        'Growth_monthly' : growth_monthly,
        'transaction':transaction,
        })
