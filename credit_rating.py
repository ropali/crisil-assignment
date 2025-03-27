from abc import ABC, abstractmethod
from typing import List, Dict, Union
from dataclasses import dataclass
from enum import Enum
import json


class LoanType(str, Enum):
    FIXED = "fixed"
    ADJUSTABLE = "adjustable"


class PropertyType(str, Enum):
    SINGLE_FAMILY = "single_family"
    CONDO = "condo"


@dataclass
class Mortgage:
    """
    Represents a single mortgage
    """
    credit_score: int
    loan_amount: float
    property_value: float
    annual_income: float
    debt_amount: float
    loan_type: LoanType
    property_type: PropertyType



class RiskStrategy(ABC):
    """
    Interface for risk calculation strategies.
    """
    @abstractmethod
    def calculate(self, mortgage: Mortgage) -> int:
        pass


class LTVRiskStrategy(RiskStrategy):
    def calculate(self, mortgage: Mortgage) -> int:
        ltv_ratio = mortgage.loan_amount / mortgage.property_value * 100
        if ltv_ratio > 90:
            return 2
        if ltv_ratio > 80:
            return 1
        return 0


class DTIRiskStrategy(RiskStrategy):
    def calculate(self, mortgage: Mortgage) -> int:
        dti_ratio = mortgage.debt_amount / mortgage.annual_income * 100
        if dti_ratio > 50:
            return 2
        if dti_ratio > 40:
            return 1
        return 0


class CreditScoreRiskStrategy(RiskStrategy):
    def calculate(self, mortgage: Mortgage) -> int:
        if mortgage.credit_score < 650:
            return 1
        if mortgage.credit_score >= 700:
            return -1
        return 0


class LoanTypeRiskStrategy(RiskStrategy):
    def calculate(self, mortgage: Mortgage) -> int:
        return 1 if mortgage.loan_type == LoanType.ADJUSTABLE else -1


class PropertyTypeRiskStrategy(RiskStrategy):
    def calculate(self, mortgage: Mortgage) -> int:
        return 1 if mortgage.property_type == PropertyType.CONDO else 0


class CreditRatingCalculator:
    def __init__(self, risk_strategies: List[RiskStrategy]):
        self.risk_strategies = risk_strategies

    def calculate_credit_rating(self, mortgages: List[Mortgage]) -> str:
        if not mortgages:
            raise ValueError("No mortgages provided")

        # Calculate individual mortgage risks
        mortgage_risks = []
        for mortgage in mortgages:
            risk_score = sum(strategy.calculate(mortgage) for strategy in self.risk_strategies)
            mortgage_risks.append(risk_score)

        # Calculate average credit score adjustment
        avg_credit_score = sum(m.credit_score for m in mortgages) / len(mortgages)
        score_adjustment = (
            -1 if avg_credit_score >= 700 else
            1 if avg_credit_score < 650 else
            0
        )

        # Calculate total risk score
        total_risk_score = sum(mortgage_risks) + score_adjustment

        # Assign credit rating
        if total_risk_score <= 2:
            return "AAA"
        elif 3 <= total_risk_score <= 5:
            return "BBB"
        else:
            return "C"


def parse_rmbs_json(rmbs_json: Dict) -> List[Mortgage]:

    return [
        Mortgage(
            credit_score=mortgage.get('credit_score'),
            loan_amount=mortgage.get('loan_amount'),
            property_value=mortgage.get('property_value'),
            annual_income=mortgage.get('annual_income'),
            debt_amount=mortgage.get('debt_amount'),
            loan_type=mortgage.get('loan_type'),
            property_type=mortgage.get('property_type')
        )
        for mortgage in rmbs_json.get('mortgages', [])
    ]

def load_rmbs_from_file(file_path: str) -> List[Mortgage]:
    try:
        with open(file_path, 'r') as file:
            rmbs_data = json.load(file)
        return parse_rmbs_json(rmbs_data)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in file: {file_path}")


if __name__ == "__main__":
    input_file = "rmbs.json"
    try:
        mortgages = load_rmbs_from_file(input_file)
        # Initialize risk strategies
        risk_strategies = [
            LTVRiskStrategy(),
            DTIRiskStrategy(),
            CreditScoreRiskStrategy(),
            LoanTypeRiskStrategy(),
            PropertyTypeRiskStrategy()
        ]

        # Calculate credit rating
        calculator = CreditRatingCalculator(risk_strategies)
        credit_rating = calculator.calculate_credit_rating(mortgages)
        print(f"Credit Rating: {credit_rating}")
    except Exception as e:
        print(f"Error: {e}")