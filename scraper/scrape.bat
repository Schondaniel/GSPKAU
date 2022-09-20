FOR /F "TOKENS=1,* DELIMS==" %%v IN ('WMIC Path Win32_LocalTime Get /FORMAT:VALUE') DO IF "%%v" == "DayOfWeek" SET DayOfWeek=%%w
IF %DayOfWeek% == 2 C:\Users\omsda\AppData\Local\Programs\Python\Python39\python.exe C:\Users\omsda\Desktop\workbench\scraper\scrape_coop.py
IF %DayOfWeek% == 2 C:\Users\omsda\AppData\Local\Programs\Python\Python39\python.exe C:\Users\omsda\Desktop\workbench\scraper\scrape_ica.py
IF %DayOfWeek% == 2 C:\Users\omsda\AppData\Local\Programs\Python\Python39\python.exe C:\Users\omsda\Desktop\workbench\scraper\scrape_lidl.py
