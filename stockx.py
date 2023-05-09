import aiohttp
import asyncio
import json
from bs4 import BeautifulSoup

stockxurl = "https://stockx.com/search/recent-asks?s="

async def init():
  await print("init!")