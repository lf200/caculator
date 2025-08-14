import os
from mcp.server.fastmcp import FastMCP
from googleapiclient.discovery import build
from typing import Dict, Any, List

# WARNING: Putting your API key directly in the code is not recommended for security reasons.
# Anyone with access to this file can use your key.
# For production environments, use environment variables as shown in the previous example.

API_KEY = "YOUR_API_KEY"

mcp = FastMCP("youtube_stats")
youtube = build('youtube', 'v3', developerKey=API_KEY)


@mcp.tool()
def get_channel_id_by_name(channel_name: str) -> List[Dict[str, str]]:
    """
    Searches for a YouTube channel by name and returns the most relevant channel IDs.

    Args:
        channel_name: The name of the YouTube channel (e.g., "PewDiePie").

    Returns:
        A list of dictionaries containing channel title and ID for the top results.
    """
    if not API_KEY or API_KEY == "YOUR_API_KEY_HERE":
        return [{"error": "API key is not set. Please replace 'YOUR_API_KEY_HERE' with your actual key."}]

    try:
        request = youtube.search().list(
            part='snippet',
            q=channel_name,
            type='channel',
            maxResults=3  # 返回最相关的3个结果
        )
        response = request.execute()

        channels = []
        if 'items' in response:
            for item in response['items']:
                channel_info = {
                    "title": item['snippet']['channelTitle'],
                    "channel_id": item['id']['channelId']
                }
                channels.append(channel_info)

        if not channels:
            return [{"error": f"No channels found for name: '{channel_name}'."}]

        return channels

    except Exception as e:
        return [{"error": f"An API error occurred: {str(e)}"}]


@mcp.tool()
def get_channel_stats(channel_id: str) -> Dict[str, Any]:
    """
    Retrieves a YouTube channel's statistics, including subscriber count and video count, using its ID.

    Args:
        channel_id: The ID of the YouTube channel (e.g., "UC-lHJZR3Gqxm24_Vd_AJtfw").

    Returns:
        A dictionary containing the channel's title, subscriber count, and other stats.
    """
    if not API_KEY or API_KEY == "YOUR_API_KEY_HERE":
        return {"error": "API key is not set. Please replace 'YOUR_API_KEY_HERE' with your actual key."}

    try:
        request = youtube.channels().list(
            part='snippet,statistics',
            id=channel_id
        )
        response = request.execute()

        if not response['items']:
            return {"error": f"No channel found for ID: {channel_id}"}

        channel = response['items'][0]

        channel_stats = {
            "title": channel['snippet']['title'],
            "subscriberCount": int(channel['statistics'].get('subscriberCount', 0)),
            "viewCount": int(channel['statistics'].get('viewCount', 0)),
            "videoCount": int(channel['statistics'].get('videoCount', 0))
        }

        return channel_stats

    except Exception as e:
        return {"error": f"An API error occurred: {str(e)}"}


if __name__ == "__main__":
    print("Starting YouTube MCP server. Waiting for Cursor to connect...")
    mcp.run(transport="stdio")
