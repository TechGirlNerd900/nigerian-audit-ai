import pandas as pd
from typing import Dict, List

class SubstantiveTester:
    """
    Prepares for substantive testing by generating sampling suggestions and audit working papers.
    """

    def __init__(self):
        pass

    def suggest_sampling(self, trial_balance: Dict[str, float], materiality: float, risk_level: str = "medium") -> Dict[str, any]:
        """
        Suggests items for sampling based on materiality and risk level.

        Args:
            trial_balance (Dict[str, float]): The trial balance.
            materiality (float): The calculated materiality for the audit.
            risk_level (str, optional): The risk level ('low', 'medium', 'high'). Defaults to "medium".

        Returns:
            Dict[str, any]: A dictionary containing sampling suggestions.
        """
        
        high_risk_accounts = ["Revenue", "Accounts Receivable", "Inventory"]
        
        suggestions = {
            "material_items": [],
            "high_risk_samples": [],
            "random_samples": []
        }
        
        df = pd.DataFrame(list(trial_balance.items()), columns=['Account', 'Balance'])
        df['AbsoluteBalance'] = df['Balance'].abs()

        # Material items
        suggestions['material_items'] = df[df['AbsoluteBalance'] >= materiality].to_dict(orient='records')
        
        # High-risk sampling
        risk_multiplier = {"low": 0.1, "medium": 0.2, "high": 0.4}
        sample_size = int(len(df) * risk_multiplier.get(risk_level, 0.2))

        for acc in high_risk_accounts:
            if acc in df['Account'].values:
                high_risk_df = df[df['Account'] == acc]
                suggestions['high_risk_samples'].extend(high_risk_df.head(sample_size).to_dict(orient='records'))

        # Random sampling
        suggestions['random_samples'] = df.sample(n=min(sample_size, len(df))).to_dict(orient='records')

        return suggestions

    def generate_working_paper(self, account_name: str, transactions: List[Dict[str, any]]) -> pd.DataFrame:
        """
        Generates a simple working paper for a given account.

        Args:
            account_name (str): The name of the account for the working paper.
            transactions (List[Dict[str, any]]): A list of transactions for the account.
                                                 Each transaction should be a dictionary with keys like
                                                 'date', 'description', 'debit', 'credit'.

        Returns:
            pd.DataFrame: A pandas DataFrame representing the working paper.
        """
        
        df = pd.DataFrame(transactions)
        df['balance'] = df['debit'].fillna(0) - df['credit'].fillna(0)
        df['cumulative_balance'] = df['balance'].cumsum()
        
        working_paper = pd.DataFrame({
            "Date": df.get("date", pd.Series(dtype='str')),
            "Description": df.get("description", pd.Series(dtype='str')),
            "Debit": df.get("debit", pd.Series(dtype='float')),
            "Credit": df.get("credit", pd.Series(dtype='float')),
            "Running Balance": df['cumulative_balance']
        })
        
        working_paper.attrs['title'] = f"Working Paper for {account_name}"
        
        return working_paper
