import httpx


async def upload_image(image):
    async with httpx.AsyncClient() as client:
        response = await client.post('https://telegra.ph/upload', files={'file': ('file', image, 'image/jpg')})
        return response.json()
