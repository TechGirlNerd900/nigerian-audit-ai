import pandas as pd
from typing import Dict, List

class AccountMapper:
    """
    Maps General Ledger (GL) accounts to standard audit categories and IFRS/GAAP codes.
    """

    def __init__(self, mapping_file_path: str = None):
        """
        Initializes the AccountMapper.

        Args:
            mapping_file_path (str, optional): Path to a CSV file containing the account mappings.
                                                The CSV should have columns like 'gl_account', 'audit_category', 'ifrs_code'.
                                                Defaults to None.
        """
        if mapping_file_path:
            self.mapping_df = pd.read_csv(mapping_file_path)
        else:
            self.mapping_df = self._get_default_mapping()

    def _get_default_mapping(self) -> pd.DataFrame:
        """
        Provides a default mapping of GL accounts to audit categories and IFRS codes.
        This can be expanded or replaced with a more comprehensive mapping from a file.
        """
        default_mapping = {
            "gl_account": [
                "Cash and Bank", "Accounts Receivable", "Inventory", "Prepaid Expenses",
                "Property Plant Equipment", "Intangible Assets", "Goodwill",
                "Accounts Payable", "Accrued Expenses", "Short Term Loans", "Long Term Loans",
                "Share Capital", "Retained Earnings", "Sales Revenue", "Cost of Sales",
                "Operating Expenses", "Depreciation Expense", "Amortization Expense",
                "Interest Expense", "Income Tax Expense"
            ],
            "audit_category": [
                "Cash and Cash Equivalents", "Trade Receivables", "Inventories", "Other Current Assets",
                "Property, Plant and Equipment", "Intangible Assets", "Intangible Assets",
                "Trade Payables", "Other Current Liabilities", "Borrowings", "Borrowings",
                "Equity", "Equity", "Revenue", "Cost of Sales",
                "Operating Expenses", "Operating Expenses", "Operating Expenses",
                "Finance Costs", "Taxation"
            ],
            "ifrs_code": [
                "IAS 7", "IFRS 9", "IAS 2", "IAS 1",
                "IAS 16", "IAS 38", "IFRS 3",
                "IFRS 9", "IAS 37", "IFRS 9", "IFRS 9",
                "IAS 1", "IAS 1", "IFRS 15", "IAS 2",
                "IAS 1", "IAS 16", "IAS 38",
                "IAS 23", "IAS 12"
            ]
        }
        return pd.DataFrame(default_mapping)

    def map_accounts(self, trial_balance: Dict[str, float]) -> Dict[str, Dict[str, any]]:
        """
        Maps the accounts in a trial balance to their corresponding audit categories and IFRS codes.

        Args:
            trial_balance (Dict[str, float]): A dictionary representing the trial balance,
                                             with account names as keys and balances as values.

        Returns:
            Dict[str, Dict[str, any]]: A dictionary with the original account names as keys,
                                     and values containing the mapped audit category, IFRS code, and balance.
        """
        mapped_accounts = {}
        for account, balance in trial_balance.items():
            mapping = self.mapping_df[self.mapping_df['gl_account'].str.lower() == account.lower()]
            if not mapping.empty:
                mapped_accounts[account] = {
                    "audit_category": mapping.iloc[0]['audit_category'],
                    "ifrs_code": mapping.iloc[0]['ifrs_code'],
                    "balance": balance
                }
            else:
                mapped_accounts[account] = {
                    "audit_category": "Unmapped",
                    "ifrs_code": "N/A",
                    "balance": balance
                }
        return mapped_accounts

    def build_lead_schedule(self, mapped_accounts: Dict[str, Dict[str, any]]) -> pd.DataFrame:
        """
        Builds a lead schedule from the mapped accounts.

        Args:
            mapped_accounts (Dict[str, Dict[str, any]]): The output from the map_accounts method.

        Returns:
            pd.DataFrame: A pandas DataFrame representing the lead schedule,
                          grouped by audit category.
        """
        data = []
        for account, details in mapped_accounts.items():
            data.append({
                "Account": account,
                "Audit Category": details["audit_category"],
                "IFRS Code": details["ifrs_code"],
                "Balance": details["balance"]
            })
        
        df = pd.DataFrame(data)
        lead_schedule = df.groupby("Audit Category").agg({
            "Balance": "sum",
            "IFRS Code": "first"
        }).reset_index()
        
        return lead_schedule
