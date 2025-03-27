import unittest
from credit_rating import (
    LoanType,
    Mortgage,
    PropertyType,
    LTVRiskStrategy,
    DTIRiskStrategy,
    CreditScoreRiskStrategy,
    LoanTypeRiskStrategy,
    PropertyTypeRiskStrategy,
    CreditRatingCalculator,
)

def create_sample_mortgage(
    credit_score=700,
    loan_amount=200000,
    property_value=250000,
    annual_income=60000,
    debt_amount=20000,
    loan_type=LoanType.FIXED,
    property_type=PropertyType.SINGLE_FAMILY
):
    """
    Helper function to create consistent test mortgages with default values.
    This reduces duplication and makes test creation more flexible.
    """
    return Mortgage(
        credit_score=credit_score,
        loan_amount=loan_amount,
        property_value=property_value,
        annual_income=annual_income,
        debt_amount=debt_amount,
        loan_type=loan_type,
        property_type=property_type
    )

class TestCreditRating(unittest.TestCase):

    def test_ltv_risk_high_ratio(self):
        """
        Test LTV risk calculation for high loan-to-value ratios.
        Verifies correct risk points are assigned.
        """
        strategy = LTVRiskStrategy()
        high_ltv_mortgage = create_sample_mortgage(loan_amount=240000, property_value=250000)
        self.assertEqual(strategy.calculate(high_ltv_mortgage), 2)

    def test_ltv_risk_moderate_ratio(self):
        """
        Test LTV risk calculation for moderate loan-to-value ratios.
        Checks boundary conditions for risk scoring.
        """
        strategy = LTVRiskStrategy()
        moderate_ltv_mortgage = create_sample_mortgage(loan_amount=210000, property_value=250000)
        self.assertEqual(strategy.calculate(moderate_ltv_mortgage), 1)

    def test_ltv_risk_low_ratio(self):
        """
        Test LTV risk calculation for low loan-to-value ratios.
        Ensures no risk points for favorable ratios.
        """
        strategy = LTVRiskStrategy()
        low_ltv_mortgage = create_sample_mortgage(loan_amount=150000, property_value=250000)
        self.assertEqual(strategy.calculate(low_ltv_mortgage), 0)

    def test_dti_risk_high_ratio(self):
        """
        Test debt-to-income risk calculation for high DTI.
        Validates risk scoring for borrowers with significant debt.
        """
        strategy = DTIRiskStrategy()
        high_dti_mortgage = create_sample_mortgage(annual_income=40000, debt_amount=25000)
        self.assertEqual(strategy.calculate(high_dti_mortgage), 2)

    def test_dti_risk_moderate_ratio(self):
        """
        Test debt-to-income risk calculation for moderate DTI.
        Checks boundary conditions for risk scoring.
        """
        strategy = DTIRiskStrategy()
        moderate_dti_mortgage = create_sample_mortgage(annual_income=50000, debt_amount=22000)
        self.assertEqual(strategy.calculate(moderate_dti_mortgage), 1)

    def test_dti_risk_low_ratio(self):
        """
        Test debt-to-income risk calculation for low DTI.
        Ensures no risk points for favorable debt levels.
        """
        strategy = DTIRiskStrategy()
        low_dti_mortgage = create_sample_mortgage(annual_income=60000, debt_amount=10000)
        self.assertEqual(strategy.calculate(low_dti_mortgage), 0)

    def test_credit_rating_aaa_scenario(self):
        """
        Test credit rating calculation for AAA (low-risk) scenario.
        Validates rating for high-quality mortgages.
        """
        risk_strategies = [
            LTVRiskStrategy(),
            DTIRiskStrategy(),
            CreditScoreRiskStrategy(),
            LoanTypeRiskStrategy(),
            PropertyTypeRiskStrategy()
        ]
        calculator = CreditRatingCalculator(risk_strategies)
        low_risk_mortgages = [
            create_sample_mortgage(credit_score=750, loan_amount=200000, property_value=250000),
            create_sample_mortgage(credit_score=720, loan_amount=180000, property_value=220000)
        ]
        self.assertEqual(calculator.calculate_credit_rating(low_risk_mortgages), "AAA")

    def test_credit_rating_bbb_scenario(self):
        """
        Test credit rating calculation for BBB (medium-risk) scenario.
        Validates rating for mixed-quality mortgages.
        """
        risk_strategies = [
            LTVRiskStrategy(),
            DTIRiskStrategy(),
            CreditScoreRiskStrategy(),
            LoanTypeRiskStrategy(),
            PropertyTypeRiskStrategy()
        ]
        calculator = CreditRatingCalculator(risk_strategies)
        medium_risk_mortgages = [
            create_sample_mortgage(
                credit_score=680, 
                loan_amount=230000,  
                property_value=250000, 
                loan_type=LoanType.ADJUSTABLE
            ),
            create_sample_mortgage(
                credit_score=650, 
                debt_amount=30000,
                annual_income=60000, 
                property_type=PropertyType.CONDO
            )
        ]
        self.assertEqual(calculator.calculate_credit_rating(medium_risk_mortgages), "BBB")

    def test_credit_rating_c_scenario(self):
        """
        Test credit rating calculation for C (high-risk) scenario.
        Validates rating for low-quality mortgages.
        """
        risk_strategies = [
            LTVRiskStrategy(),
            DTIRiskStrategy(),
            CreditScoreRiskStrategy(),
            LoanTypeRiskStrategy(),
            PropertyTypeRiskStrategy()
        ]
        calculator = CreditRatingCalculator(risk_strategies)
        high_risk_mortgages = [
            create_sample_mortgage(credit_score=600, loan_type=LoanType.ADJUSTABLE, property_type=PropertyType.CONDO),
            create_sample_mortgage(credit_score=620, loan_amount=240000, property_value=250000)
        ]
        self.assertEqual(calculator.calculate_credit_rating(high_risk_mortgages), "C")

    def test_empty_mortgages_raises_error(self):
        """
        Verify that attempting to calculate rating with no mortgages raises an error.
        """
        risk_strategies = [
            LTVRiskStrategy(),
            DTIRiskStrategy(),
            CreditScoreRiskStrategy(),
            LoanTypeRiskStrategy(),
            PropertyTypeRiskStrategy()
        ]
        calculator = CreditRatingCalculator(risk_strategies)
        with self.assertRaises(ValueError):
            calculator.calculate_credit_rating([])

if __name__ == "__main__":
    unittest.main()
