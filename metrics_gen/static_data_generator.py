from typing import Union
from dataclasses import dataclass
import random
import pandas as pd


@dataclass
class Static_data_configuration_level:
    name: str
    options: Union[str, list]


class Static_data_generator:
    def __init__(self, deployment: pd.DataFrame, configuration: dict) -> None:
        """Creates a static data generator according to givein configuration

        Parameters
        ----------
        deployment : pd.DataFrame
            Deployment dataframe, generated by the `deployment_generator`
        configuration : dict
            Configuration dictionary of static data or containing such at `static` entry
            Each entry can hold:
            - A list of optional values ex: [model_a, model_b, model_c], [1, 3, 5, 7, 11, 13]
            - A range string ex: range(10)
        """
        self.deployment = deployment.copy(deep=True)
        self.configuration: list[
            Static_data_configuration_level
        ] = self._get_or_create_static_data_configuration(configuration)

    def _get_or_create_static_data_configuration(
        self, static_data_configuration: dict
    ) -> list[Static_data_configuration_level]:
        """Converts a static data configuration dictionary to a list of `Static_data_configuration_level`

        Parameters
        ----------
        static_data_configuration : dict
            Static data configuration

        Returns
        -------
        list[Static_data_configuration_level]
            a list of parsed `Static_data_configuration_level`
        """
        configuration = []
        for feature_name, options in static_data_configuration.items():
            configuration.append(Static_data_configuration_level(feature_name, options))
        return configuration

    def generate_static_data(self) -> pd.DataFrame:
        deployment = self.deployment.copy()
        for static_feature in self.configuration:
            if str(static_feature.options).startswith("range"):
                deployment[static_feature.name] = [
                    random.choice(eval(static_feature.options))
                    for i in range(self.deployment.shape[0])
                ]
            else:
                deployment[static_feature.name] = [
                    random.choice(static_feature.options)
                    for i in range(self.deployment.shape[0])
                ]
        return deployment

    @staticmethod
    def _get_static_feature(feature: Static_data_configuration_level):
        if str(feature).startswith("range"):
            return random.choice(eval(feature))
        return random.choice(feature)