# tablecreator
Это проект для отделов подбора персонала, с помощью которого можно облегчить учет резюме при поиске сотрудников на сайте hh.ru. Так как на самом сайте нет возможности учитывать найденные резюме, то эта программа генерирует таблицу, где вы можете отмечать одобрен или нет кандидат, кто просматривал и когда.
***
**В чем суть**
-----------------------------------
В папке all находятся 3 файла: код "HRcreate_v0_1.py", инструкция по использованию и пустой текстовый файл, который использует программа. Сам скрипт запускается непосредственно через python, потому что делать exe-шник было немного трудно и он занимал очень много места, это требует некоторой доработки, которую я буду выкладывать.
***
**Как работает**
-----------------------------------
Для корректной работы приложению нужны права администратора, которые он собственно и запрашивает. Этот кусок я писал не сам, но он очень важен. Далее код использует файл htmltext.txt как буфер обмена, потому что от туда он берет данные для обработки. К сожалению, для работы с этим приложением придется вручную делат запрос на сайте hh.ru по поиску кандидатов, так как подключения к API сейчас еще нет. Поэтому весь код страницы, где были найдены резюме необходимо скопировать в этот текстовый файл. Код ищет в этом файле совпадения по шаблону ссылки и затем делает таблицу. Также я сделал простенький интерфейс для всего, чтобы можно было понятно указать название и дату создания таблицы.
