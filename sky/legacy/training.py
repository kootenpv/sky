import webbrowser
import requests
from selenium import webdriver
import os

try:
    from .helper import makeTree
except SystemError:
    from helper import makeTree

class Training():
    def __init__(self, name, path): 
        self.name = name + "/"
        self.path = path
        self.htmls = []
        self.targets = []
        self.trees = []
        self.links = []

    def __len__(self):
        return len(self.links)

    def __repr__(self):
        return 'Training: {}, targets --> {}'.format(self.name, str(self.targets))

    def addLinks(self, links, sel = True, startFrom = 0):
        self.links = links 
        if sel:
            driver = webdriver.Firefox() 
            for url in links:
                driver.get(url)
                self.htmls.append(driver.page_source)
            driver.close()    
        # save htmls
        else:
            for url in links:
                r = requests.get(url)
                self.htmls.append(r.text)
        if not os.path.exists(self.path + self.name):
            os.makedirs(self.path + self.name)
        for num, html in enumerate(self.htmls): 
            with open(self.path + self.name + str(num + startFrom) + ".html", "w") as f: 
                f.write(html)
        self.trees = [makeTree(" ".join(html.split()), url) for html, url in zip(self.htmls, self.links)] 
        
    def view(self, num): 
        webbrowser.open("file://" + self.path + self.name + str(num) + ".html") 

    def viewAll(self):
        for num, _ in enumerate(self.links):
            self.view(num)
        
    def classify(self, startFrom = 0):
        self.targets = []
        for num, link in enumerate(self.links):
            self.view(num + startFrom)
            target_value = input("Now visiting:\n" + link + "\nInsert the target value: ").strip()
            self.targets.append(target_value)    

    def save(self):
        # save links
        if not os.path.exists(self.path + self.name):
            os.makedirs(self.path + self.name)
        else:
            answer = input("Path already exists. Overwrite? (Y/N)")
            print(answer)
            if "n" in answer.lower():
                return

        with open(self.path + self.name + "sky.training.links", "w") as f: 
            f.write("\n".join(self.links))
            
        # save targets
        with open(self.path + self.name + "sky.training.targets", "w") as f: 
            f.write("sky\nsky".join(self.targets))
        
        # save htmls
        for num, html in enumerate(self.htmls): 
            with open(self.path + self.name + str(num) + ".html", "w") as f: 
                f.write(html)

    def load(self):
        obj = Training(self.name, self.path) 
        
        with open(obj.path + obj.name + "sky.training.links") as f: 
            obj.links = f.read().split('\n')
            
        # load targets
        with open(obj.path + obj.name + "sky.training.targets") as f: 
            targets = f.read()
            obj.targets = [" ".join(x.split()) for x in targets.split("sky\nsky")]
        
        # load htmls
        obj.htmls = []
        for num in range(len(obj.links)): 
            with open(obj.path + obj.name + str(num) + ".html") as f: 
                obj.htmls.append(f.read())

        obj.trees = [makeTree(" ".join(html.split()), url) for html, url in zip(obj.htmls, obj.links)]         
                
        return obj        

# tr = Training("marktplaats-testcase1", "/Users/pascal/egoroot/virtual-python/sky/sky/tests/")
# tr.addLinks(["http://www.marktplaats.nl/a/telecommunicatie/mobiele-telefoons-samsung/a1012265931-samsung-galaxy-s3-mini-16gb.html?c=17f70af2bde4a155c6d568ce3cad9ab7", "http://www.marktplaats.nl/a/telecommunicatie/mobiele-telefoons-apple-iphone/m859429930-apple-iphone-5s.html?c=178bad54c6700be11ff2d898a4d529b1&previousPage=lr"])

# tr = Training("nieuwsdumper-testcase1", "/Users/pascal/egoroot/virtual-python/sky/sky/tests/")
# links = ["http://www.nieuwsdumper.nl/nieuws/1454/eerste-volvo-fmx-410-8x4-tridem-betonmixer-voor-bck.html", 
#          "http://www.nieuwsdumper.nl/nieuws/1453/ihi-30vx-verbree-boogzinkers.html",
#          "http://www.nieuwsdumper.nl/nieuws/1448/volvo-fm-420-8x4-widespread-c-ride-voor-heitink-transport.html"]
# tr.addLinks(links)

# tr = Training("nieuwsdumper-testcase2", "/Users/pascal/egoroot/virtual-python/sky/sky/tests/")
# links = ["http://www.nieuwsdumper.nl/nieuws/1454/eerste-volvo-fmx-410-8x4-tridem-betonmixer-voor-bck.html", 
#          "http://www.nieuwsdumper.nl/nieuws/1453/ihi-30vx-verbree-boogzinkers.html",
#          "http://www.nieuwsdumper.nl/nieuws/1448/volvo-fm-420-8x4-widespread-c-ride-voor-heitink-transport.html"]
# tr.addLinks(links)

# tr = Training("bouwmaterieel-testcase1", "/Users/pascal/egoroot/virtual-python/sky/sky/tests/")
# links = ["http://www.bouwmaterieel-benelux.nl/matgidsweb/artikelserver/id/4308154815752565759/Franki-Construct-kiest-weer-voor-Sennebogen?site=null&language=nl2&style=bmb", "http://www.bouwmaterieel-benelux.nl/matgidsweb/artikelserver/id/-125635014634651648/Paccar-MX-11-motor-wint-Innovation-Award?site=null&language=nl2&style=bmb"]
# tr2.addLinks(links)
# tr2.classify()

# tr6 = Training("pypi-author", "/Users/pascal/egoroot/sky_package/sky/tests/")
# tr6.addLinks(["https://pypi.python.org/pypi/sky/", "https://pypi.python.org/pypi/scrapely/"])
# tr6.classify()
# tr6.save()

# tr = Training('betterdoctor-doctor-referalls', '/Users/pascal/egoroot/sky_package/sky/tests/')
# tr.addLinks(['https://betterdoctor.com/igor-grosman', 'https://betterdoctor.com/gary-gwertzman'])
# tr.classify()
# tr.save()



