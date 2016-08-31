# 6.00 Problem Set 5
# RSS Feed Filter

import ps5_feedparser
import string
import time
from ps5_project_util import translate_html
from ps5_news_gui import Popup

#-----------------------------------------------------------------------
#
# Problem Set 5

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = ps5_feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        summary = translate_html(entry.summary)
        try:
            subject = translate_html(entry.tags[0]['term'])
        except AttributeError:
            subject = ""
        newsStory = NewsStory(guid, title, subject, summary, link)
        ret.append(newsStory)
    return ret

#======================
# Part 1
# Data structure design
#======================

# Problem 1

class NewsStory():
    def __init__(self, guid, title, subject, summary, link):
        self.guid = guid
        self.title = title
        self.subject = subject
        self.summary = summary
        self.link = link
    def get_guid(self):
        return self.guid
    def get_title(self):
        return self.title
    def get_subject(self):
        return self.subject
    def get_summary(self):
        return self.summary
    def get_link(self):
        return self.link

#======================
# Part 2
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        raise NotImplementedError

# Whole Word Triggers
# Problems 2-5

class WordTrigger(Trigger):
    def __init__(self, word): # word should be a string
        self.word = word.lower()
    def is_word_in(self,text):
        ''' text: type - str
            Returns True if self.word is in text, False otherwise
        '''
        text = text.lower()
        # Create translation table that maps punctuation to spaces
        out = ""
        for char in string.punctuation:
            out += " "
        trans = string.maketrans(string.punctuation, out)
        # Change all punctuation in the text to spaces,
        # then split the text at those spaces
        text = text.translate(trans)
        words = text.split()
        # Check for the trigger word
        return self.word in words

class TitleTrigger(WordTrigger):
    def __init__(self, word):
        WordTrigger.__init__(self, word)
    def evaluate(self,story):
        return self.is_word_in(story.get_title())
        
class SubjectTrigger(WordTrigger):
    def __init__(self, word):
        WordTrigger.__init__(self, word)
    def evaluate(self,story):
        return self.is_word_in(story.get_subject())
    
class SummaryTrigger(WordTrigger):
    def __init__(self, word):
        WordTrigger.__init__(self, word)
    def evaluate(self,story):
        return self.is_word_in(story.get_summary())


# Composite Triggers
# Problems 6-8

class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger = trigger
    def evaluate(self, story):
        return not self.trigger.evaluate(story)

class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2
    def evaluate(self, story):
        return self.trigger1.evaluate(story) and self.trigger2.evaluate(story)
    
class OrTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2
    def evaluate(self, story):
        return self.trigger1.evaluate(story) or self.trigger2.evaluate(story)


# Phrase Trigger
# Question 9

class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase
    def is_phrase_in(self,text):
        ''' text: type - str
            Returns True if self.phrase is in text, False otherwise
            self.phrase is case sensitive
        '''
        return self.phrase in text

    def evaluate(self, story):
        """ story: type - NewsStory
            Returns True if self.phrase is in the title, subject, or summary of the story
        """
        return self.is_phrase_in(story.get_title()) or \
               self.is_phrase_in(story.get_subject()) or \
               self.is_phrase_in(story.get_summary())

#======================
# Part 3
# Filtering
#======================

def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory-s.
    Returns only those stories for whom
    a trigger in triggerlist fires.
    """
    filtered = []
    for story in stories:
#        print "Title:", story.title
        for trigger in triggerlist:
            if trigger.evaluate(story):
                #print ">>Trigger activated"
                filtered.append(story)
                break
            
    return filtered

#======================
# Part 4
# User-Specified Triggers
#======================

def readTriggerConfig(filename):
    """
    Returns a list of trigger objects
    that correspond to the rules set
    in the file filename
    """
    # Here's some code that we give you
    # to read in the file and eliminate
    # blank lines and comments
    triggerfile = open(filename, "r")
    all = [ line.rstrip() for line in triggerfile.readlines() ]
    lines = []
    for line in all:
        if len(line) == 0 or line[0] == '#':
            continue
        lines.append(line)
    #print "lines:", lines

    # Build a set of triggers from 'lines' and return the appropriate ones
    triggers_final = []
    triggers_created = {} # t_name -> trigger
    for line in lines:
        #print ">> line:", line
        words = line.split()
        
        if words[0]!="ADD":    # Trigger definitions only
            t_name = words[0]
            t_type = words[1]

            # Create the trigger instance
            if t_type=='TITLE':
                new_trigger = TitleTrigger(words[2])
            elif t_type =='SUBJECT':
                new_trigger = SubjectTrigger(words[2])
            elif t_type =='SUMMARY':
                new_trigger = SummaryTrigger(words[2])
            elif t_type=='PHRASE':
                new_trigger = PhraseTrigger(" ".join(words[2:]))
            elif t_type=='NOT':
                t_negated = triggers_created[words[2]]
                new_trigger = NotTrigger(t_negated)
            elif t_type=='AND' or t_type=='OR':
                t_first = triggers_created[words[2]]
                t_second = triggers_created[words[3]]
                if t_type=='AND':
                    new_trigger = AndTrigger(t_first, t_second)
                elif t_type=='OR':
                    new_trigger = OrTrigger(t_first, t_second)
            else:
                raise KeywordError('Not a valid trigger type.')

            # Store the trigger
            triggers_created[t_name] = new_trigger
            #print "triggers_created:", triggers_created

        # Add the selected triggers to the list to return ('ADD')    
        else:                       
            for name in words[1:]:   # All the names of triggers to add
                    triggers_final.append(triggers_created[name])
    #print triggers_final
    return triggers_final
    
import thread

def main_thread(p):
    # A sample trigger list - you'll replace
    # this with something more configurable in Problem 11
    t1 = TitleTrigger("Obama")
    t2 = SummaryTrigger("MIT")
    t3 = PhraseTrigger("Supreme Court")
    t4 = OrTrigger(t2, t3)
    triggerlist = [t1, t4]
    
    triggerlist = readTriggerConfig("ps5_triggers.txt")

    guidShown = []
    
    while True:
        print "Polling..."

        # Get stories from Google's Top Stories RSS news feed
        stories = process("http://news.google.com/?output=rss")
        # Get stories from Yahoo's Top Stories RSS news feed
        stories.extend(process("http://rss.news.yahoo.com/rss/topstories"))

        # Only select stories we're interested in
        stories = filter_stories(stories, triggerlist)
    
        # Don't print a story if we have already printed it before
        newstories = []
        for story in stories:
            if story.get_guid() not in guidShown:
                newstories.append(story)
        
        for story in newstories:
            guidShown.append(story.get_guid())
            p.newWindow(story)

        print "Sleeping..."
        time.sleep(SLEEPTIME)

SLEEPTIME = 60 #seconds -- how often we poll
if __name__ == '__main__':
    p = Popup()
    thread.start_new_thread(main_thread, (p,))
    p.start()

