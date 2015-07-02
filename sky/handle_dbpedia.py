import re

resources = {}
with open('/Users/pascal/Downloads/instance_types_en.nt') as f: 
    for line in f:
        try:
            parts = line.split()
            first_part = parts[0]
            if first_part.count('/') == 4:
                name = first_part.split('/')[-1].replace('_', ' ').lower()[:-1]
                if len(name.split()) > 3:
                    continue
                pos = name.find('  ')
                if pos > -1:
                    name = name[:pos]       
                if 'ontologydesignpatterns' in parts[2]:                    
                    continue
                if 'w3.org' in parts[2]:                    
                    continue
                if name not in resources: 
                    resources[name] = set() 
                resources[name].add(parts[2].split('/')[-1][:-1]) 
        except IndexError:
            pass    

# resources start with 'http://dbpedia.org/resource/'

# types = set()
# for name in resources:
#     m = re.search(r'(\(.+\))', name)
#     if m:
#         types.add(m.groups()[0].lower())            

stripped_resources = {}
for x in resources:
    if any([y in x for y in '0123456789']): 
        if '%' not in x: 
            continue
    pos = x.find('(') 
    if pos > -1:
        stripped_resources[x[:pos].strip()] = resources[x]
    else:    
        stripped_resources[x.strip()] = resources[x]

#######################################################################################################################        

from ZODB.FileStorage import FileStorage
from ZODB.DB import DB

import transaction
from BTrees.OOBTree import OOBTree
        
storage = FileStorage('/Users/pascal/GDrive/appear/Data.fs')
db = DB(storage)
connection = db.open()
root = connection.root()

root['dbpedia'] = OOBTree(stripped_resources)
transaction.commit()

    



a="""The Otto Group Product Classification Challenge was the most popular competition in Kaggle's history. It was also one of the first competitions with Kaggle scripts enabled, making it even easier for the 3,415 participants to publicly share and collaborate on code. Data scientists with very different backgrounds and varying levels of machine learning experience posted code in Otto's scripts repository. We've selected a handful of scripts that we believe highlight important machine learning techniques, interesting packages, new approaches, and the creativity Kagglers are known for in the data science community. Thanks to the authors of these scripts for providing more context on their code and what we can learn from it! Created by: Christophe Bourguignat Language: Python What motivated you to create this script? During the competition, some Kagglers were discussing in the forum about calibration for Random Forests. It was a brand new functionality of the last scikit-learn version (0.16), and I was puzzled about it. Calibration makes the output of the models give a true probability that a sample belongs to a particular class. For instance, a well calibrated (binary) classifier should classify the samples such that among the samples to which it gave a predict_proba value close to 0.8, approximately 80% actually belong to the positive class. It makes machine learning models outputs more in line with the common sense idea of probability. The Otto Group challenge was the perfect opportunity to test this new feature on a real case! What did you learn from the code / output? Quickly, in our context, it appeared that calibration indeed boosted performance a lot (15 to 20%), particularly for random forests. My partner (the great champion Xavier Conort) and I used an ensemble of models so the final impact was less, but this trick helped us gain severals dozens of ranks on the leaderboard. I’m not sure if calibration is available in other libraries (e.g. R), but it strengthens my idea that scikit-learn is a top-notch machine learning library. I’m a big fan of it! What can other data scientists learn from your experience? At the end of the competition, I wanted to share with the community what I learned. First, I wrote a blog post. Then, I met Michaël Benesty at the Paris Machine Learning meetup that I co-organized at AXA Data Innovation Lab. He was the author of an amazing script, the most viewed of the challenge, Understanding XGBoost Model on Otto Data. He gave me the idea to leverage scripts, this great new functionality of the Kaggle platform. top Created by: Henning Sperr Language: Python What motivated you to create this script? This was one of my first Kaggle competitions and although I kind of knew a lot about ML from lectures and talks, once you start using algorithms on real problems a lot of questions come up. From the competition it was clear relatively quickly that gains could be achieved by ensembling multiple classifiers, but then the question is: how do you do that? I learned a lot about hard and soft voting, but I couldn't find out why having equal weights for all classifiers is a valid thing to do. I found many sources that gave different methods on how to ensemble classifiers, but they all leave the details out. Its more like: "Yeah just take the predictions of all your classifiers and train a OLS/SVM/RF on it and that gives you the weights" but never why and when you use actual probabilities and when do you use predictions etc. Long story short, I saw that in the forums more and more people were struggling with the same issues and I found that SciPy has solvers that can give us the best weights so I thought I'd give it a shot and contribute it. It was really nice to see that I got good feedback and made me want to share more code and ideas in the future! What did you learn from the code / output? I learned an awful lot about SciPy (minimizing arbitrary functions), NumPy, and ensembling. I see in many works people actually just average predictions which seems to work reasonably well already. (I still wonder if there is a paper about that that I couldn't find.) Maybe the cost of having a small held-out dataset to find the find the optimal weights is not worth the gain, although the performance difference between the best weight and 0.5 weights can be quite big. Another thing I actually learned is that sharing code and participating in the discussions in the forums is a lot of fun and a great learning experience. Thank you, Kaggle team! What can other data scientists learn from your script? I think its good to ask yourself how you actually combine classifiers and why that works. Understanding what happens in the script can also help you a lot with NumPy/SciPy and knowing that you can minimize your own functions using the scipy solvers can open up new ideas. As it is shown in my script, when ensembling two random forests with logistic regression, the regression performs much worse and only gets a small weight which sometimes will even be zero. Then you know that your new classifier does not add any value to your ensemble. How did the output of this script help you in the competition? I remember being stuck in the higher 0.4s log-loss scores for quite a bit until I started to ensemble my classifiers. Just averaging them didn't work very well for me though so I learned proper weights for them. I think I ended up somewhere around 0.42 log-loss while my best classifier was 0.45 log-loss so the ensemble made it quite a bit better. In a future project, ensembling by using other classifiers might be worth a script! top Created by: Michaël Benesty & Posted by: Tianqi Chen Language: RMarkdown What motivated you to create this script? A few weeks before the competition ended, Tianqi asked me if I had time to write some documentation for the challenge. He highlighted the fact that Kagglers didn't seem aware of the existence of the embedded visualization functions I worked on. So the initial idea was to highlight these functions. The main motivation of writing the script was the same that I had when I contributed to the XGboost R package documentation: showing newbies like me a real way to proceed. No magic ultra optimized ready-to-use parameters or some very compact code. For instance, I rewrote several parts of the initial script making it longer, adding some steps, so the meaning of each variable is obvious. I also try to write in such a way that readers can do the same thing at work with another dataset. Many of the scripts I see on the forum are really specialized for the challenge. They take one very specific point and go deep. This script is a more general approach. Another reason was making people use more viz functions. Using viz means understanding the model. Sometimes boosting is called a black box, but I don't think it is. I mean it is much easier to have a feeling about the model than with nnet for instance. Viz helps to have this understanding. The 3rd reason is to make XGboost more used. It is already very well known among Kagglers, but I have met many ML practitioners who are not trying anything other than scikit. Showing that you can do serious ML with R and XGboost was one of the goals. (I like R as much as XGboost!). What is your data science background? I am tax lawyer for the Paris office of a big firm. Before that I was CPA and financial auditor. So, I have no data scientist training at all. I discovered ML 4/5 years ago and loved the idea a lot. Then I tried to find a way to use it at work. I made many mistakes, and searched for a good lib able to manage large dataset and having a model interpretable. After many tries, I finally found XGboost on a Kaggle forum (of course!).I added all the features I was missing to the XGboost R package. I really liked the project and Tianqi (the main author of XGBoost) was nice enough to answer all of my newbie questions so I started to contribute much more to the source code than what I needed to do for my work. Then I started working on the documentation, wrote two vignettes (in R this is a documentation with details) and completed the function documentation. It took me quite some time but I am happy with the result right now. top Created by: JMT5802 Language: R What motivated you to create this script? I wanted some way to gauge how my submissions compared to the others and specifically to the team in the leader position. What did you learn from the code / output? The key thing I learned was how to use the grid package in R to combine several ggplot plots into a single visualization. How did this script help you in the competition? I used the leaderboard visualizations to help motivate me to try harder to improve my submissions. In addition to motivating me, I used the visualization as means to keep my colleagues at work abreast about how I was progressing in the competition. I downloaded the leaderboard data everyday, generated the charts and posted the charts outside my office. Sometimes a co-worker would stop by and ask about the charts. I took this opportunity to tell them about Kaggle and how much fun it was in competing and gaining experience in machine learning algorithms to develop predictive models."""


