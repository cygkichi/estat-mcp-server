"""
E-Stat MCP Server
"""
import os
import httpx
from typing import Optional
from mcp.server.fastmcp import FastMCP

mcp_server = FastMCP("EStatServer")
E_STAT_API_BASE_URL = "https://api.e-stat.go.jp/rest/3.0/app/"
E_STAT_APP_ID = os.getenv("E_STAT_APP_ID")

@mcp_server.tool()
async def search_e_stat_tables(
        search_word: str,
        surveyYears	: str,
        startPosition: int = 1,
        limit: int = 100
    ) -> str:
    """
    Retrieves a list of statistics tables from the E-Stat API.
    名称:統計表情報取得
    政府統計の総合窓口（e-Stat）で提供している統計表の情報を取得します。
    リクエストパラメータの指定により条件を絞った情報の取得も可能です。

    Args:
        search_word (str): Search keyword for statistics tables.
            Use "AND", "OR", or "NOT" to specify multiple words for search.
            Examples:
                - "東京 AND 人口"
                - "東京 OR 大阪"
        surveyYears (str): Survey years for the statistics tables.
            Must be in one of the following formats:
                - yyyy: Unified year.
                - yyyymm: Unified month.
                - yyyymm-yyyymm: Unified month range.
            Example: "2023" or "202301-202312" or "202301"
        startPosition (int, optional): Start position for the search results.
            Defaults to 1. For example:
                - To get the first 100 results, set startPosition to 1.
                - To get the next 100 results, set startPosition to 101.
        limit (int, optional): Maximum number of results to retrieve. Defaults to 100.
    Example:
        search_word = "東京 AND 人口"
        surveyYears = "2023"
        startPosition = 1
        limit = 100

    Returns:
        str: The response text from the E-Stat API.
    """
    url = (
        f"{E_STAT_API_BASE_URL}getStatsList?appId={E_STAT_APP_ID}"
        f"&searchWord={search_word}&limit={limit}"
        f"&surveyYears={surveyYears}&startPosition={startPosition}"
    )
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text



@mcp_server.tool()
async def get_e_stat_meta_info(
        stats_data_id: str
    ) -> str:
    """
    Retrieves meta information from the E-Stat API.
    機能名:メタ情報取得
    指定した統計表IDに対応するメタ情報（表章事項、分類事項、地域事項等）を取得します。

    Args:
        stats_data_id (str): The ID of the statistics data(統計表ID).
            Example: "0000010201".

    Returns:
        str: The response text from the E-Stat API.
    """
    url = (
        f"{E_STAT_API_BASE_URL}getMetaInfo?appId={E_STAT_APP_ID}"
        f"&statsDataId={stats_data_id}"
    )
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text


@mcp_server.tool()
async def get_specific_e_stat_data(
        data_set_id: Optional[str] = None,
        stats_data_id: Optional[str] = None,
        startPosition: int = 1,
        limit: int = 100
    ) -> str:
    """
    Retrieves specific statistics data from the E-Stat API.
    機能名:統計データ取得
    指定した統計表ID又はデータセットIDに対応する統計データ（数値データ）を取得します。

    Args:
        data_set_id (str or None): The ID of the dataset(データセットID).
        stats_data_id (str or None): The ID of the statistics data(統計表ID).
        # Ensure that either data_set_id or stats_data_id is provided, but not both
        if not data_set_id and not stats_data_id:
            raise ValueError("Either 'data_set_id' or 'stats_data_id' must be provided.")
        if data_set_id and stats_data_id:
            raise ValueError("Only one of 'data_set_id' or 'stats_data_id' should be provided.")

        startPosition (int): The starting position for the search results.
            Defaults to 1. For example:
                - To get the first 100 results, set startPosition to 1.
                - To get the next 100 results, set startPosition to 101.
        limit (int): The maximum number of results to retrieve.
            Defaults to 100.

    Returns:
        str: The response text from the E-Stat API.
    """
    url = (
        f"{E_STAT_API_BASE_URL}getStatsData?appId={E_STAT_APP_ID}"
        f"&startPosition={startPosition}&limit={limit}"
    )
    if data_set_id and not stats_data_id:
        url += f"&dataSetId={data_set_id}"
    elif stats_data_id and not data_set_id:
        url += f"&statsDataId={stats_data_id}"
    else:
        raise ValueError("Either 'data_set_id' or 'stats_data_id' must be provided, but not both.")

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text


@mcp_server.tool()
async def get_e_stat_ref_dataset(
        data_set_id: str,
    ) -> str:
    """
    Retrieves the reference dataset from the E-Stat API.
    機能名:データセット参照
    登録されているデータセットの絞り込み条件等を参照します。
    データセットIDが指定されていない場合は、利用者が使用できるデータセットの一覧が参照可能です。

    Args:
        data_set_id (str): The ID of the dataset to retrieve(データセットID).

    Returns:
        str: The response text from the E-Stat API.
    """
    url = (
        f"{E_STAT_API_BASE_URL}refDataset?appId={E_STAT_APP_ID}"
    )
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text


@mcp_server.tool()
async def get_e_stat_data_catalog(
        search_word: str,
        surveyYears: str,
        startPosition: int = 1,
        limit: int = 100
    ) -> str:
    """
    Retrieves the data catalog from the E-Stat API.
    機能名:データカタログ情報取得
    政府統計の総合窓口（e-Stat）で提供している統計表ファイルおよび統計データベースの情報を取得できます。
    統計表情報取得機能同様に、リクエストパラメータの指定により条件を絞った情報の取得も可能です。


    Args:
        search_word (str): Search keyword for statistics tables.
            Use "AND", "OR", or "NOT" to specify multiple words for search.
            Examples:
                - "東京 AND 人口"
                - "東京 OR 大阪"
        surveyYears (str): The survey years for the statistics tables.
            Must be in one of the following formats:
                - yyyy: Unified year.
                - yyyymm: Unified month.
                - yyyymm-yyyymm: Unified month range.
            Example: "2023" or "202301-202312" or "202301"
        startPosition (int, optional): Start position for the search results.
            Defaults to 1. For example:
                - To get the first 100 results, set startPosition to 1.
                - To get the next 100 results, set startPosition to 101.
        limit (int, optional): Maximum number of results to retrieve. Defaults to 100.
    Example:
        search_word = "東京 AND 人口"
        surveyYears = "2023"
        startPosition = 1
        limit = 100

    Returns:
        str: The response text from the E-Stat API.
    """
    url = (
        f"{E_STAT_API_BASE_URL}getDataCatalog?appId={E_STAT_APP_ID}"
        f"&searchWord={search_word}&surveyYears={surveyYears}"
        f"&startPosition={startPosition}&limit={limit}"
    )
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text

if __name__ == "__main__":
    mcp_server.run()
