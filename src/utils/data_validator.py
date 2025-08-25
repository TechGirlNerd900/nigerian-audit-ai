# Path: src/utils/data_validator.py

import pandas as pd
from typing import List, Dict, Any, Union
from loguru import logger
from great_expectations.dataset import PandasDataset
from great_expectations.core import ExpectationConfiguration, ExpectationSuite
from src.utils.nigerian_standards import NigerianFinancialStandards

logger.add("file.log", rotation="500 MB") # Configure Loguru for file logging

class CustomPandasDataset(PandasDataset):
    """
    A custom PandasDataset for Great Expectations to allow for custom expectations.
    """
    _data_asset_type = "CustomPandasDataset"

    @PandasDataset.expectation(["column"])
    def expect_column_values_to_be_within_nigerian_currency_range(self, column: str) -> Dict[str, Any]:
        """
        Expects column values to be positive and within a reasonable range for Nigerian Naira.
        """
        min_val = 0.0
        max_val = 1_000_000_000_000.0 # 1 Trillion Naira (arbitrary upper limit for sanity check)
        return self.expect_column_values_to_be_between(
            column,
            min_value=min_val,
            max_value=max_val,
            result_format="SUMMARY"
        )

    @PandasDataset.expectation(["column"])
    def expect_column_values_to_conform_to_nigerian_tax_rates(self, column: str, tax_type: str) -> Dict[str, Any]:
        """
        Expects column values to conform to known Nigerian tax rates for a given tax type.
        """
        if tax_type == "VAT":
            expected_rate = NigerianFinancialStandards.VAT_RATE
        elif tax_type == "CIT":
            expected_rate = NigerianFinancialStandards.COMPANY_INCOME_TAX_RATE
        else:
            raise ValueError(f"Unknown tax type: {tax_type}")

        # This expectation assumes the column contains the *rate* itself, not the calculated tax.
        # You might need to adjust this based on your data structure.
        return self.expect_column_values_to_be_in_set(
            column,
            value_set=[expected_rate],
            result_format="SUMMARY"
        )


class DataValidator:
    """
    Handles data validation and quality checks using Great Expectations.
    """

    def __init__(self, expectation_suite_name: str = "audit_data_suite"):
        self.expectation_suite_name = expectation_suite_name
        self.expectation_suite = ExpectationSuite(expectation_suite_name=self.expectation_suite_name)
        logger.info(f"Initialized DataValidator with suite: {self.expectation_suite_name}")

    def add_expectation(self, expectation_type: str, column: str = None, **kwargs):
        """
        Adds an expectation to the current expectation suite.
        """
        config = ExpectationConfiguration(
            expectation_type=expectation_type,
            kwargs={"column": column, **kwargs} if column else kwargs
        )
        self.expectation_suite.add_expectation(config)
        logger.debug(f"Added expectation: {expectation_type} for column {column} with kwargs {kwargs}")

    def build_default_financial_expectations(self):
        """
        Builds a set of common expectations for financial datasets.
        """
        logger.info("Building default financial expectations.")
        # Common expectations for financial data
        self.add_expectation("expect_column_to_exist", column="company_id")
        self.add_expectation("expect_column_to_exist", column="year")
        self.add_expectation("expect_column_values_to_be_in_type_list", column="year", type_list=["int"])
        self.add_expectation("expect_column_values_to_not_be_null", column="company_id")
        self.add_expectation("expect_column_values_to_be_unique", column="company_id") # If company_id is unique per row

        # Example financial columns - adjust based on your actual data schema
        financial_columns = [
            "revenue", "cost_of_sales", "gross_profit", "operating_expenses",
            "profit_before_tax", "tax_expense", "profit_after_tax",
            "total_assets", "total_liabilities", "equity",
            "cash_from_operations", "cash_from_investing", "cash_from_financing"
        ]
        for col in financial_columns:
            self.add_expectation("expect_column_to_exist", column=col)
            self.add_expectation("expect_column_values_to_be_in_type_list", column=col, type_list=["numeric"])
            self.add_expectation("expect_column_values_to_be_within_nigerian_currency_range", column=col)
            self.add_expectation("expect_column_values_to_not_be_null", column=col, mostly=0.95) # Allow some nulls

        # Example for compliance data
        self.add_expectation("expect_column_to_exist", column="compliance_status")
        self.add_expectation("expect_column_values_to_be_in_set", column="compliance_status", value_set=["compliant", "non-compliant", "partial"])

        # Example for tax rates
        # Assuming you have columns like 'vat_rate_applied' or similar
        # self.add_expectation("expect_column_values_to_conform_to_nigerian_tax_rates", column="vat_rate_applied", tax_type="VAT")

    def validate_dataframe(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Validates a pandas DataFrame against the configured expectation suite.

        Args:
            df (pd.DataFrame): The DataFrame to validate.

        Returns:
            Dict[str, Any]: The validation result from Great Expectations.
        """
        logger.info(f"Starting validation for DataFrame with {len(df)} rows.")
        ge_df = CustomPandasDataset(df)
        validation_result = ge_df.validate(expectation_suite=self.expectation_suite, result_format="SUMMARY")

        if not validation_result["success"]:
            logger.warning(f"Data validation failed for suite '{self.expectation_suite_name}'.")
            for result in validation_result["results"]:
                if not result["success"]:
                    logger.warning(f"  - Failed Expectation: {result['expectation_config']['expectation_name']} "
                                   f"on column '{result['expectation_config']['kwargs'].get('column', 'N/A')}' "
                                   f"with {result['result']['unexpected_count']} unexpected values.")
        else:
            logger.info(f"Data validation successful for suite '{self.expectation_suite_name}'.")

        return validation_result

    def get_expectation_suite_json(self) -> Dict[str, Any]:
        """Returns the expectation suite as a JSON-serializable dictionary."""
        return self.expectation_suite.to_json_dict()

# Example Usage:
if __name__ == "__main__":
    # Create a dummy DataFrame
    data = {
        'company_id': [1, 2, 3, 4, 5],
        'year': [2022, 2023, 2022, 2023, 2022],
        'revenue': [1000000, 1200000, 900000, 1500000, -50000], # -50000 is an issue
        'cost_of_sales': [500000, 600000, 450000, 700000, 20000],
        'gross_profit': [500000, 600000, 450000, 800000, -70000], # -70000 is an issue
        'operating_expenses': [200000, 250000, 180000, 300000, 30000],
        'profit_before_tax': [300000, 350000, 270000, 500000, -100000],
        'tax_expense': [90000, 105000, 81000, 150000, 0],
        'profit_after_tax': [210000, 245000, 189000, 350000, -100000],
        'total_assets': [5000000, 6000000, 4800000, 7000000, 1000000],
        'total_liabilities': [2000000, 2500000, 1900000, 2800000, 400000],
        'equity': [3000000, 3500000, 2900000, 4200000, 600000],
        'cash_from_operations': [150000, 180000, 130000, 200000, 10000],
        'cash_from_investing': [-50000, -60000, -40000, -70000, -5000],
        'cash_from_financing': [20000, 30000, 15000, 40000, 2000],
        'compliance_status': ['compliant', 'compliant', 'non-compliant', 'compliant', 'partial'],
        'vat_rate_applied': [0.075, 0.075, 0.075, 0.075, 0.075] # Assuming a column for applied VAT rate
    }
    df = pd.DataFrame(data)

    validator = DataValidator()
    validator.build_default_financial_expectations()
    # Add a specific expectation for VAT rate
    validator.add_expectation("expect_column_values_to_conform_to_nigerian_tax_rates", column="vat_rate_applied", tax_type="VAT")

    validation_results = validator.validate_dataframe(df)

    print("\nValidation Results Summary:")
    print(f"Success: {validation_results['success']}")
    for result in validation_results["results"]:
        if not result["success"]:
            print(f"  - Failed Expectation: {result['expectation_config']['expectation_name']} "
                  f"on column '{result['expectation_config']['kwargs'].get('column', 'N/A')}'")
            print(f"    Details: {result['result']}")
