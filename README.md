Sreality offer scrapper

This is a quick project using playwright and asyncio that scrapes given offers on sreality.cz. 
I made this to quickly save offers since they might be gone pretty soon and I am lazy to save all the pictures manually.
For each URL it saves the post into PDF file and take screenshot of all pictures in the offer.

Use this project as follows:


Make venv and install dependancies.
```
python -m venv venv
source venv/bin/activate
pip install .
```

If you have not used playwright yet, install headless browsers for playwright. This should be installed outside of the venv.
```
python -m playwright install
```


Fill the links.txt with the links from sreality you wish to download.

Run the code

```
sreality_scrapper
```
