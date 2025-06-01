from datetime import datetime
from pathlib import Path
from typing import Any, Hashable

import pandas as pd
import requests
from mcp.server.fastmcp import FastMCP
from requests import Response

from mcp_server.constant_variables import COLUMNS, DATA, HEADERS, PARAMS, SCANNER_URL

mcp = FastMCP("Tradingview_mcp")

DATA_EXPORT_PATH: Path = (
    Path("src/tempDir") / f"{datetime.now().date().strftime("%Y-%m-%d")}.csv"
)


class TradingviewError(Exception):
    """Custom exception class for Tradingview-related errors."""

    pass


def _get_tradingview_response() -> Response:
    """
    Makes a POST request to the TradingView scanner API and returns the response.

    Returns:
        Response: The HTTP response object from the TradingView API.

    Raises:
        TradingviewError: If the request fails or times out, or if the server
                         returns an HTTP error status code.

    Note:
        Uses a 30-second timeout for the request. The function relies on
        module-level constants SCANNER_URL, HEADERS, DATA, and PARAMS.
    """
    try:
        response: Response = requests.post(
            url=SCANNER_URL,
            headers=HEADERS,
            data=DATA,
            params=PARAMS,
            timeout=30,
        )
        response.raise_for_status()
        return response
    except:
        raise TradingviewError("Unable to connect to Tradingview API server")


def _create_recommendation(value: float) -> str:

    if not isinstance(value, (float, int)):  # type: ignore
        raise ValueError("Unable to create recommendation")

    value_mapping: dict[str, tuple[float, float]] = {
        "strong_buy": (0.5, 1.0),
        "buy": (0.1, 0.5),
        "neutral": (-0.1, 0.1),
        "sell": (-0.5, -0.1),
        "strong_sell": (-1.0, -0.5),
    }

    for recommendation, (min_value, max_value) in value_mapping.items():
        if min_value <= value <= max_value:
            return recommendation

    raise ValueError("Unable to create recommendation column")


def _create_response_df() -> pd.DataFrame:
    """
    Create a pandas DataFrame from TradingView API response data.

    Fetches data from the TradingView API, extracts the relevant data rows,
    and constructs a DataFrame with predefined columns. Adds a 'recommendation'
    column based on the 'Recommend.All' values using the _create_recommendation
    function.

    Returns:
        pd.DataFrame: A DataFrame containing the parsed TradingView data with
                     columns defined by the COLUMNS constant, plus an additional
                     'recommendation' column with human-readable recommendations.

    Raises:
        TradingviewError: If the API response is missing the 'data' key,
                         if no valid data rows are found, or if any other
                         error occurs during data parsing.
    """
    try:
        response: Response = _get_tradingview_response()
        api_json: Any = response.json()
        api_data: Any = api_json.get("data", None)

        if not api_data:
            raise TradingviewError("Unable to find the data key to parse")

        rows: list[Any] = [row.get("d", None) for row in api_data if row.get("d", None)]

        if not rows:
            raise TradingviewError("Unable to find the rows")

        df = pd.DataFrame(rows, columns=COLUMNS)
        df["recommendation"] = df["Recommend.All"].apply(_create_recommendation)  # type: ignore

        return df
    except:
        raise TradingviewError("Unable to parse the data from API response")


def _load_df(path: Path) -> pd.DataFrame:
    """
    Load a DataFrame from a CSV file, creating it if it doesn't exist.

    This function attempts to load a pandas DataFrame from the specified CSV file path.
    If the file doesn't exist, it creates a new DataFrame using _create_response_df(),
    saves it to the specified path, and returns it.

    Args:
        path (Path): The file path to the CSV file to load or create.

    Returns:
        pd.DataFrame: The loaded DataFrame from the CSV file, or a newly created
                      DataFrame if the file didn't exist.

    Note:
        If the file doesn't exist, a new CSV file will be created at the specified path
        using the DataFrame structure from _create_response_df().
    """
    if not path.exists():
        path.mkdir(exist_ok=False)
        df: pd.DataFrame = _create_response_df()
        df.to_csv(path, index=False)
        return df

    df: pd.DataFrame = pd.read_csv(path)  # type: ignore
    return df


@mcp.tool()
def get_stock_recommendations() -> str:
    """
    Retrieve stock recommendations from the TradingView data.

    Loads stock data from the configured data export path and returns
    a list of stock recommendations with their names and recommendation values.

    Returns:
        list[dict[Hashable, Any]]: A list of dictionaries where each dictionary
            contains 'name' and 'recommendation' keys representing stock names
            and their respective recommendation values.

    Raises:
        TradingviewError: If unable to fetch or process the data from TradingView.
    """
    try:
        df: pd.DataFrame = _load_df(DATA_EXPORT_PATH)
        return (
            "The following recommendations are based on technical analysis, combining the ratings of multiple technical indicators (on a 1-day interval) to help traders and investors identify potential profitable trades more easily."
            f"{df[["name", "recommendation"]].to_dict(orient="records")}"  # type: ignore
        )
    except:
        raise TradingviewError("Unable to fetch the data from tradingview")


@mcp.tool()
def check_stock_values(tickers: list[str]) -> dict[Hashable, Any]:
    """
    Retrieve stock values for specified ticker symbols.

    Args:
        tickers (list[str]): List of stock ticker symbols to look up

    Returns:
        dict[Hashable, Any]: Dictionary containing filtered stock data for the
                           specified tickers, converted from DataFrame format

    Raises:
        TradingviewError: If unable to load or process the stock data file

    Note:
        This function loads data from DATA_EXPORT_PATH and filters it based on
        the 'name' column matching the provided ticker symbols.
    """
    try:
        df: pd.DataFrame = _load_df(DATA_EXPORT_PATH)
        df_filtered: pd.DataFrame = df[df["name"].isin(tickers)]  # type: ignore
        return df_filtered.to_dict()  # type: ignore
    except:
        raise TradingviewError("Unable to find the stock values")


if __name__ == "__main__":
    mcp.run()
