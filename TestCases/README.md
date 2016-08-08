TestCases package
- 將 test case 放在這個 package 內,test case 須名稱為 XXXCase.py.
- XXXCase.py 須登記在 __init__.py 內.
- XXXCase.py 內可含數個 case ,一個類別一個 case ,該類別須繼承 Case.py 內的 Case class
- Global setUp and tearDown 請實作於上一層 pi_tester.py 呼叫的 py 中的 00 and 99
- 須於上一層 pi_tester.py 呼叫的 py 中於對應測試編號的類別繼承 XXXCase.py 內的 case class 即可執行測試

Test architecture
![Preview](TestArch.png) 
