from regression_model.config.core import config
from regression_model.processing.features import TemporalVariableTransformer


def test_temporal_variable_transformer(sample_input_data):
    # Dado
    transformer = TemporalVariableTransformer(
        variables=config.model_config.temporal_vars,  # YearRemodAdd
        reference_variable=config.model_config.ref_var,
    )
    assert sample_input_data["YearRemodAdd"].iat[0] == 1961

    # Cuando
    subject = transformer.fit_transform(sample_input_data)

    # Entonces
    assert subject["YearRemodAdd"].iat[0] == 49
