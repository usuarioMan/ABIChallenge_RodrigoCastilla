from typing import List

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

class TemporalVariableTransformer(BaseEstimator, TransformerMixin):
    """Transformador de tiempo temporal transcurrido."""

    def __init__(self, variables: List[str], reference_variable: str):

        if not isinstance(variables, list):
            raise ValueError("variables debe ser una lista")

        self.variables = variables
        self.reference_variable = reference_variable

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        # Necesitamos este paso para ajustarse al pipeline de sklearn
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:

        # Para no sobrescribir el dataframe original
        X = X.copy()

        for feature in self.variables:
            X[feature] = X[self.reference_variable] - X[feature]

        return X

class Mapper(BaseEstimator, TransformerMixin):
    """Mapper de variables categóricas."""

    def __init__(self, variables: List[str], mappings: dict):

        if not isinstance(variables, list):
            raise ValueError("variables debe ser una lista")

        self.variables = variables
        self.mappings = mappings

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        # Necesitamos el ajuste para acomodar al pipeline de sklearn
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X = X.copy()
        for feature in self.variables:
            X[feature] = X[feature].map(self.mappings)

        return X
