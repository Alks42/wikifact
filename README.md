# What is that?
Just a small project i've made mostly for myself. As said in the description  it generates random fact from wikipedia using [Mangus Manske's random article tool](https://magnustools.toolforge.org/randomarticle.php) and wikipedia api. For ui PyQt5 package was used.
# Config file
Contain 4 changeable  parameters:
- resolution - width and height of program window
- language - could be any en, ru, de etc
- Defalut_category - with language change you also must to change this to any new_language.wikipedia category.
_(This is because with new language prog creates new lang_category.txt and must fill it with at least one existing category to generate a fact with next program start)_
- Depth - Integer numbers from 1 to 10. The bigger the number the wider range of subcategories. E.g. in the religion category, 1 would result in facts about saints, various churches, etc. while 5 could lead to historians researching Catholic protests in modern America.
