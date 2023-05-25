from package.constants import *
from package.log import *
from package.pnmHeader_class import PnmHeader
from typing import Union, List
import json


class RxMerDataValue:
    """
    Represents a single RxMER value for a subcarrier.
    """

    NO_MEASUREMENT: int = 0xFF
    MAX_REPORTED_VALUE: float = 63.5

    def __init__(self, value: Union[float, int]) -> None:
        """
        Initialize a RxMerDataValue.

        Args:
            value (float or int): RxMER value as a float or byte value.
        """
        self.value: float = self._validate_value(value)

    @staticmethod
    def _validate_value(value: Union[float, int]) -> float:
        """
        Validate and convert the RxMER value.

        Args:
            value (float or int): RxMER value as a float or byte value.

        Returns:
            float: Converted RxMER value.
        """
        if isinstance(value, int):
            if value == RxMerDataValue.NO_MEASUREMENT:
                return RxMerDataValue.NO_MEASUREMENT
            value = min(max(value, 0), int(RxMerDataValue.MAX_REPORTED_VALUE * 4))
            return value / 4.0

        if isinstance(value, float):
            value = min(max(value, 0.0), RxMerDataValue.MAX_REPORTED_VALUE)
            return value

        raise ValueError("Invalid RxMER value")

    def isMaxValue(self) -> bool:
        """
        Check if the RxMER value is the maximum reported value.

        Returns:
            bool: True if the RxMER value is the maximum reported value, False otherwise.
        """
        return self.value == RxMerDataValue.MAX_REPORTED_VALUE

    def getRxMER(self) -> float:
        """
        Get the RxMER value.

        Returns:
            float: The RxMER value.
        """
        return self.value

    def isMeasurement(self) -> bool:
        """
        Check if a measurement is available for the RxMER value.

        Returns:
            bool: True if a measurement is available, False otherwise.
        """
        return self.value != RxMerDataValue.NO_MEASUREMENT

    def toJson(self) -> str:
        """
        Convert the RxMerDataValue to a JSON string.

        Returns:
            str: JSON representation of the RxMerDataValue.
        """
        return json.dumps({
            "value": self.value,
            "isMaxValue": self.isMaxValue(),
            "isMeasurement": self.isMeasurement()
        })


class RxMerData:
    """
    Represents a sequence of received modulation error ratio (RxMER) values for a downstream OFDM channel.
    """

    def __init__(self, values: List[RxMerDataValue]) -> None:
        """
        Initialize RxMerData.

        Args:
            values (list): List of RxMerDataValues.
        """
        self.values: List[RxMerDataValue] = values

    def toJson(self) -> str:
        """
        Convert the RxMerData to a JSON string.

        Returns:
            str: JSON representation of the RxMerData.
        """
        return json.dumps({
            "values": [value.toJson() for value in self.values]
        })


class RX_MER:
    def __init__(self, pnm_header: PnmHeader):
        """
        Initialize the RX_MER object.

        Args:
            pnm_header (PnmHeader): Instance of the PnmHeader class.
        """
        self.pnm_header = pnm_header

    def process_data(self):
        """
       Process the data received from PNM_HEADER.

        This method can be modified to perform the desired operations on the data.

        """
        pnm_data = self.pnm_header.getPnmData()

        Log.debug("PMN-Data-Len:" + str(pnm_data.__sizeof__()))

        Log.debug("Processing data from PNM_HEADER: " + str(pnm_data))
        # Perform the desired operations on the data here

    def get_rxmer_data(self) -> RxMerData:
        """
        Get the RxMER data.

        Returns:
            RxMerData: The RxMER data.
        """
        # Modify this method to return the desired RxMER data
        values = [RxMerDataValue(1.2), RxMerDataValue(2.3), RxMerDataValue(3.4)]  # Example values
        return RxMerData(values)

    def run(self):
        """
        Run the RX_MER processing.

        This method can be modified to fit the desired workflow.

        """
        self.process_data()



