import pathlib
import asyncio
from typing import List, Tuple

import playwright

from playwright import async_playwright
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__package__)

# My inrnet is terribly slow, so I use these variables to limit number of running browsers.
# Otherwise playwright commands fails on timeout or the screenshots are taken when the picture is being loaded.
number_of_running_tasks = 2
time_in_ms_between_every_screenshot = 5000


async def download(urls: List[str]) -> None:
    semaphore = asyncio.Semaphore(number_of_running_tasks)
    tasks_download_offer = [
        asyncio.create_task(download_offer(url, semaphore)) for url in urls
    ]
    await asyncio.gather(*tasks_download_offer)


async def get_current_image_order(page: playwright) -> Tuple[int, int]:
    number_of_pictures_element = await page.querySelector(
        "//span[contains(@class,'image-order')]"
    )
    number_of_pictures_element_text = await number_of_pictures_element.innerText()
    number_of_pictures_element_text = number_of_pictures_element_text.split("/")
    return (
        int(number_of_pictures_element_text[0]),
        int(number_of_pictures_element_text[1]),
    )


async def download_offer(url: str, semaphore: asyncio.Semaphore) -> None:

    async with semaphore:
        # create folder for output files
        _path = pathlib.Path(f"{url.replace('/','.')}/")
        _path.mkdir(parents=True, exist_ok=True)

        async with async_playwright() as p:
            browser_type = p.chromium
            browser = await browser_type.launch()
            page = await browser.newPage()
            await page.goto(url, timeout=0)

            # save the offer to PDF file
            fn = "offer.pdf"  # I don't know what is your fn
            filepath = _path / fn
            filepath.open("w", encoding="utf-8")
            await page.pdf(format="A4", path=filepath)
            await browser.close()

        async with async_playwright() as p:
            browser_type = p.chromium
            browser = await browser_type.launch(headless=False)
            page = await browser.newPage()
            await page.goto(url, timeout=0)

            # click on the main picture
            await page.click(
                "//div[contains(@class,'download-cover')][contains(@ng-click,'showEntity(SHOW_ENTITY.FULLSCREEN)')]",
                timeout=0,
            )

            # get current location in pictures
            current, num_of_pictures = await get_current_image_order(page)

            # shift to the beggining of album
            while current != 1:
                await page.click(
                    "//button[contains(@class,'icon-arr-left')]", timeout=0
                )
                current, _ = await get_current_image_order(page)

            # make screenshot of all pictures
            for i in range(num_of_pictures):
                await page.waitForTimeout(time_in_ms_between_every_screenshot)

                fn = f"{i}.png"  # I don't know what is your fn
                filepath = _path / fn
                with filepath.open("w", encoding="utf-8") as f:
                    await page.screenshot(path=filepath)

                await page.click(
                    "//button[contains(@class,'icon-arr-right')]", timeout=0
                )

import pathlib
import asyncio
from typing import List, Tuple

import playwright

from playwright import async_playwright
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__package__)

# My inrnet is terribly slow, so I use these variables to limit number of running browsers.
# Otherwise playwright commands fails on timeout or the screenshots are taken when the picture is being loaded.
number_of_running_tasks = 2
time_in_ms_between_every_screenshot = 5000


async def download(urls: List[str]) -> None:
    semaphore = asyncio.Semaphore(number_of_running_tasks)
    tasks_download_offer = [
        asyncio.create_task(download_offer(url, semaphore)) for url in urls
    ]
    await asyncio.gather(*tasks_download_offer)


async def get_current_image_order(page: playwright) -> Tuple[int, int]:
    number_of_pictures_element = await page.querySelector(
        "//span[contains(@class,'image-order')]"
    )
    number_of_pictures_element_text = await number_of_pictures_element.innerText()
    number_of_pictures_element_text = number_of_pictures_element_text.split("/")
    return (
        int(number_of_pictures_element_text[0]),
        int(number_of_pictures_element_text[1]),
    )


async def download_offer(url: str, semaphore: asyncio.Semaphore) -> None:

    async with semaphore:
        # create folder for output files
        _path = pathlib.Path(f"{url.replace('/','.')}/")
        _path.mkdir(parents=True, exist_ok=True)

        async with async_playwright() as p:
            browser_type = p.chromium
            browser = await browser_type.launch()
            page = await browser.newPage()
            await page.goto(url, timeout=0)

            # save the offer to PDF file
            fn = "offer.pdf"  # I don't know what is your fn
            filepath = _path / fn
            filepath.open("w", encoding="utf-8")
            await page.pdf(format="A4", path=filepath)
            await browser.close()

        async with async_playwright() as p:
            browser_type = p.chromium
            browser = await browser_type.launch(headless=False)
            page = await browser.newPage()
            await page.goto(url, timeout=0)

            # click on the main picture
            await page.click(
                "//div[contains(@class,'download-cover')][contains(@ng-click,'showEntity(SHOW_ENTITY.FULLSCREEN)')]",
                timeout=0,
            )

            # get current location in pictures
            current, num_of_pictures = await get_current_image_order(page)

            # shift to the beggining of album
            while current != 1:
                await page.click(
                    "//button[contains(@class,'icon-arr-left')]", timeout=0
                )
                current, _ = await get_current_image_order(page)

            # make screenshot of all pictures
            for i in range(num_of_pictures):
                await page.waitForTimeout(time_in_ms_between_every_screenshot)

                fn = f"{i}.png"  # I don't know what is your fn
                filepath = _path / fn
                with filepath.open("w", encoding="utf-8") as f:
                    await page.screenshot(path=filepath)

                await page.click(
                    "//button[contains(@class,'icon-arr-right')]", timeout=0
                )

def main():
    with open("links.txt", "r", encoding="utf-8") as f:
        urls = [url.strip() for url in f]
    asyncio.run(download(urls))

if __name__ == "__main__":
    main()
