# What is that?
Just a small project i've made mostly for myself. As said in the description  it generates random fact from wikipedia using [Mangus Manske's random article tool](https://magnustools.toolforge.org/randomarticle.php) and wikipedia api. For ui PyQt5 package was used.
# How it works
<img width="440" alt="ui" src="https://user-images.githubusercontent.com/90620708/161583765-0dd71fbd-c373-4e46-8007-7c8adaffc7f5.png">

The blue link is clickable and will open the wikipedia page in your browser. The button **"More"** will generate another fact from one of selected categories. **"Add field"** will add category written nearby if it exists. **"Show"** will show or hide the category field and the **"Delete Selected"** button. The latter is for deleting selected categories. **"Save"** will save url in _saved_urls.txt_. To open it click **"Links"** button. Resolution of program window and language can be changed by editing config file.
## Config file
Contain 4 changeable  parameters:
- resolution - width and height of program window
- language - could be any en, ru, de etc
- Defalut_category - with language change you also must change this to any new_language.wikipedia category.
_(This is because with new language prog creates new lang_category.txt and must fill it with at least one existing category to generate a fact with next program start)_
- Depth - Integer numbers from 0 to 10. The bigger the number the wider range of subcategories. E.g. in the religion category, 1 would result in facts about saints, various churches, etc. while 5 could lead to historians researching Catholic protests in modern America.
### Is there any .exe file?
Yep, just look to the right to releases section.
