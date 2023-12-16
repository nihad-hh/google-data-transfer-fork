from abc import ABC, abstractmethod

import gspread
import pandas as pd

from google_data_transfer.commons import PathType


class Sheet(ABC):
    """A class to represent a sheet in a Google Spreadsheet.

    Attributes:
        spreadsheet_url : The URL of the Google Spreadsheet
        spreadsheet_id : The ID of the Google Spreadsheet
        name : The name of the sheet

    !!! note

        The above docstring is autogenerated by docstring-gen library (https://docstring-gen.airt.ai)
    """

    def __init__(self, spreadsheet_url: str, sheet_name: str):
        """
        Args:
            spreadsheet_url: URL of the spreadsheet
            sheet_name: Name of the sheet

        Returns:
            The spreadsheet_id and the name of the sheet

        Raises:
            ValueError: If spreadsheet_url or sheet_name is None

        !!! note

            The above docstring is autogenerated by docstring-gen library (https://docstring-gen.airt.ai)
        """
        self.spreadsheet_url = spreadsheet_url
        self.spreadsheet_id = spreadsheet_url.split("/")[-2]
        self.name = sheet_name

    @abstractmethod
    def to_df(self) -> pd.DataFrame:
        """!!! note

        Failed to generate docs

        !!! note

            The above docstring is autogenerated by docstring-gen library (https://docstring-gen.airt.ai)
        """
        ...

    @abstractmethod
    def write_col(self, col_name: str, col_values: list) -> None:
        """Write a column to a file.

        Args:
            col_name: The name of the column
            col_values: The values of the column

        Returns:
            None

        Raises:
            ValueError: If col_name is None

        !!! note

            The above docstring is autogenerated by docstring-gen library (https://docstring-gen.airt.ai)
        """
        ...


class GSpreadSheet(Sheet):
    """A class to represent a Google Spreadsheet.

    Attributes:
        spreadsheet_url : URL of the spreadsheet
        sheet_name : name of the sheet
        creds_path : path to the credentials file

    !!! note

        The above docstring is autogenerated by docstring-gen library (https://docstring-gen.airt.ai)
    """

    def __init__(
        self,
        spreadsheet_url: str,
        sheet_name: str,
        gspread_client: gspread.client.Client,
    ):
        """A class to represent a person.

        Attributes:
            spreadsheet_url : URL of the spreadsheet
            sheet_name : name of the sheet
            creds_path : path to the credentials file

        !!! note

            The above docstring is autogenerated by docstring-gen library (https://docstring-gen.airt.ai)
        """
        super().__init__(spreadsheet_url, sheet_name)
        self._gc = gspread_client
        self._spreadsheet = self._gc.open_by_url(spreadsheet_url)
        self._sheet = self._spreadsheet.worksheet(sheet_name)
        self._df = self._to_df()

    @classmethod
    def from_creds_file(
        cls, creds_path: PathType, spreadsheet_url: str, sheet_name: str
    ):
        # TODO: re-use auth token from auth.py
        """Create a new Spreadsheet from a credentials file.

        Args:
            creds_path: Path to the credentials file.
            spreadsheet_url: URL of the spreadsheet.
            sheet_name: Name of the sheet.

        Returns:
            A new Spreadsheet object.

        !!! note

            The above docstring is autogenerated by docstring-gen library (https://docstring-gen.airt.ai)
        """
        gspread_client = gspread.oauth(credentials_filename=creds_path)
        return cls(spreadsheet_url, sheet_name, gspread_client)

    @classmethod
    def from_creds(
        cls, json_token: Any, spreadsheet_url: str, sheet_name: str
    ):
        # TODO: re-use auth token from auth.py
        """Create a new Spreadsheet from a credentials file.

        Args:
            json_token: Authentication token
            spreadsheet_url: URL of the spreadsheet.
            sheet_name: Name of the sheet.

        Returns:
            A new Spreadsheet object.

        !!! note

            The above docstring is autogenerated by docstring-gen library (https://docstring-gen.airt.ai)
        """
        gspread_client, authorized_user = gspread.oauth_from_dict(json_token)
        return cls(spreadsheet_url, sheet_name, gspread_client)

    def find_cells(self, query: str) -> list[gspread.Cell]:
        """Find all cells matching the query.

        Args:
            query: The query to search for.

        Returns:
            A list of gspread.Cell objects.

        !!! note

            The above docstring is autogenerated by docstring-gen library (https://docstring-gen.airt.ai)
        """
        return self._sheet.findall(query)

    def _to_df(self) -> pd.DataFrame:
        """!!! note

        Failed to generate docs

        !!! note

            The above docstring is autogenerated by docstring-gen library (https://docstring-gen.airt.ai)
        """
        return pd.DataFrame(self._sheet.get_all_records())

    def to_df(self) -> pd.DataFrame:
        """!!! note

        Failed to generate docs

        !!! note

            The above docstring is autogenerated by docstring-gen library (https://docstring-gen.airt.ai)
        """
        return self._df

    @property
    def columns(self) -> list[str]:
        return self.to_df().columns

    def write_col(self, col_name: str, col_values: list) -> None:
        """Write a column to a Google sheet.

        Args:
            col_name: The name of the column to write to.
            col_values: The values to write to the column.

        Raises:
            ValueError: If col_name is not found in the sheet.

        !!! note

            The above docstring is autogenerated by docstring-gen library (https://docstring-gen.airt.ai)
        """
        col_header_cells = self.find_cells(col_name)
        if len(col_header_cells) != 1:
            raise ValueError(
                f"Found {len(col_header_cells)} cells with name {col_name}."
            )
        col_header_cell = col_header_cells.pop()
        # Compute range in A1 notation
        col_a1 = col_header_cell.address.replace(str(col_header_cell.row), "")

        first_row_a1 = str(col_header_cell.row + 1)
        first_cell = col_a1 + first_row_a1

        num_rows = len(self._df)
        last_row_a1 = str(num_rows + 1)
        last_cell = col_a1 + last_row_a1

        update_range = first_cell + ":" + last_cell
        # Process col_values for gspread update
        update_values = [[el] for el in col_values]

        self._sheet.update(update_range, update_values)
