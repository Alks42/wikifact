# What is that?
Just a small project for generating random facts from specific wikipedia category using [Mangus Manske's random article tool](https://magnustools.toolforge.org/randomarticle.php) and wikipedia api. For ui PyQt5 was used.
## Requirements
PyQt5.
# How it works
<img width="440" alt="ui" src="https://user-images.githubusercontent.com/90620708/163584483-d5de2f57-f280-4031-b6f5-9e80b2077738.jpg">

The blue link is clickable and will open the wikipedia page in your browser. The button **"More"** will generate another fact from one of selected categories. **"Add field"** will add category written nearby if it exists. **"Show"** will show or hide the category field and the **"Delete Selected"** button. The latter is for deleting selected categories. **"Save"** will save url in _saved_urls.txt_. To open it click **"Links"** button. Resolution of program window and language can be changed by editing config file.
## Config file
Contain 3 changeable  parameters:
- resolution - width and height of program window
- language - could be any en, ru, de etc
- Depth - Integer numbers from 0 to 10. The bigger the number the wider range of subcategories. E.g. in the religion category, 1 would result in facts about saints, various churches, etc. while 5 could lead to historians researching Catholic protests in modern America.
- avoid-descriptions - list of page descriptions to avoid.
### Is there any .exe file?
Yep, just look to the right to releases section.
