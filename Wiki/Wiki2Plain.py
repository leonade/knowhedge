# -*- coding: utf-8 -*-
## transform wiki markup language into plain text
## created on Feb 1, 2015 by Li
## last modified Feb 1, 2015 by Li
## adopted from http://stackoverflow.com/questions/4460921/extract-the-first-paragraph-from-a-wikipedia-article-python?rq=1

import re

class Wiki2Plain:
    def __init__(self, wiki):
        self.wiki = wiki
        
        self.text = wiki
        self.text = self.unhtml(self.text)
        self.text = self.unwiki(self.text)
        self.text = self.punctuate(self.text)
    
    def __str__(self):
        return self.text
    
    def unwiki(self, wiki):
        """
        Remove wiki markup from the text.
        """
        wiki = re.sub(r'(?i)\{\{IPA(\-[^\|\{\}]+)*?\|([^\|\{\}]+)(\|[^\{\}]+)*?\}\}', lambda m: m.group(2), wiki)
        wiki = re.sub(r'(?i)\{\{Lang(\-[^\|\{\}]+)*?\|([^\|\{\}]+)(\|[^\{\}]+)*?\}\}', lambda m: m.group(2), wiki)
        wiki = re.sub(r'\{\{[^\{\}]+\}\}', '', wiki)
        wiki = re.sub(r'(?m)\{\{[^\{\}]+\}\}', '', wiki)
        wiki = re.sub(r'(?m)\{\|[^\{\}]*?\|\}', '', wiki)
        wiki = re.sub(r'(?i)\[\[Category:[^\[\]]*?\]\]', '', wiki)
        wiki = re.sub(r'(?i)\[\[Image:[^\[\]]*?\]\]', '', wiki)
        wiki = re.sub(r'(?i)\[\[File:[^\[\]]*?\]\]', '', wiki)
        wiki = re.sub(r'\[\[[^\[\]]*?\|([^\[\]]*?)\]\]', lambda m: m.group(1), wiki)
        wiki = re.sub(r'\[\[([^\[\]]+?)\]\]', lambda m: m.group(1), wiki)
        wiki = re.sub(r'\[\[([^\[\]]+?)\]\]', '', wiki)
        wiki = re.sub(r'(?i)File:[^\[\]]*?', '', wiki)
        wiki = re.sub(r'\[[^\[\]]*? ([^\[\]]*?)\]', lambda m: m.group(1), wiki)
        wiki = re.sub(r"''+", '', wiki)
        wiki = re.sub(r'(?m)^\*$', '', wiki)
        wiki = re.sub(r'(?m)<!--([^>])*>', '', wiki)
		
        return wiki
    
    def unhtml(self, html):
        """
        Remove HTML from the text.
        """
        html = re.sub(r'(?i)&amp;', '&', html)
		# added by Li 2015-2-1 13:59:33 ->
        html = re.sub(r'&lt;', '<', html)
        html = re.sub(r'&gt;', '>', html)
        html = re.sub(r'&quot;', '"', html)
		# added by Li 2015-2-1 13:59:33 <-        
        html = re.sub(r'(?i)&nbsp;', ' ', html)
        html = re.sub(r'(?i)<br[ \\]*?>', '\n', html)
        html = re.sub(r'(?m)<!--.*?--\s*>', '', html)
        html = re.sub(r'(?i)<ref[^>]*>[^>]*<\/ ?ref>', '', html)
        html = re.sub(r'(?m)<.*?>', '', html)
        
        return html
    
    def punctuate(self, text):
        """
        Convert every text part into well-formed one-space
        separate paragraph.
        """
        text = re.sub(r'\r\n|\n|\r', '\n', text)
        text = re.sub(r'\n\n+', '\n\n', text)
        
        parts = text.split('\n\n')
        partsParsed = []
        
        for part in parts:
            part = part.strip()
            
            if len(part) == 0:
                continue
            
            partsParsed.append(part)
        
        return '\n\n'.join(partsParsed)
    
    def image(self):
        """
        Retrieve the first image in the document.
        """
        # match = re.search(r'(?i)\|?\s*(image|img|image_flag)\s*=\s*(<!--.*-->)?\s*([^\\/:*?<>"|%]+\.[^\\/:*?<>"|%]{3,4})', self.wiki)
        match = re.search(r'(?i)([^\\/:*?<>"|% =]+)\.(gif|jpg|jpeg|png|bmp)', self.wiki)
        
        if match:
            return '%s.%s' % match.groups()
        
        return None

if __name__ == '__main__':
    # @link http://simple.wikipedia.org/w/index.php?action=raw&title=Uruguay
    wiki = """{{Redirect2|Anarchist|Anarchists|the fictional character|Anarchist (comics)|other uses|Anarchists (disambiguation)}}
{{Use British English|date=January 2014}}
{{pp-move-indef}}
{{Anarchism sidebar}}

'''Anarchism''' is a [[political philosophy]] that advocates [[stateless society|stateless societies]] often defined as [[self-governance|self-governed]] voluntary institutions,&lt;ref&gt;&quot;ANARCHISM, a social philosophy that rejects authoritarian government and maintains that voluntary institutions are best suited to express man's natural social tendencies.&quot; George Woodcock. &quot;Anarchism&quot; at The Encyclopedia of Philosophy&lt;/ref&gt;&lt;ref&gt;&quot;In a society developed on these lines, the voluntary associations which already now begin to cover all the fields of human activity would take a still greater extension so as to substitute themselves for the state in all its functions.&quot; [http://www.theanarchistlibrary.org/HTML/Petr_Kropotkin___Anarchism__from_the_Encyclopaedia_Britannica.html Peter Kropotkin. &quot;Anarchism&quot; from the Encyclopædia Britannica]&lt;/ref&gt;&lt;ref&gt;&quot;Anarchism.&quot; The Shorter Routledge Encyclopedia of Philosophy. 2005. p. 14 &quot;Anarchism is the view that a society without the state, or government, is both possible and desirable.&quot;&lt;/ref&gt;&lt;ref&gt;Sheehan, Sean. Anarchism, London: Reaktion Books Ltd., 2004. p. 85&lt;/ref&gt; but that several authors have defined as more specific institutions based on non-[[Hierarchy|hierarchical]] [[Free association (communism and anarchism)|free associations]].&lt;ref&gt;&quot;as many anarchists have stressed, it is not government as such that they find objectionable, but the hierarchical forms of government associated with the nation state.&quot; Judith Suissa. ''Anarchism and Education: a Philosophical Perspective''. Routledge. New York. 2006. p. 7&lt;/ref&gt;&lt;ref name=&quot;iaf-ifa.org&quot;/&gt;&lt;ref&gt;&quot;That is why Anarchy, when it works to destroy authority in all its aspects, when it demands the abrogation of laws and the abolition of the mechanism that serves to impose them, when it refuses all hierarchical organisation and preaches free agreement — at the same time strives to maintain and enlarge the precious kernel of social customs without which no human or animal society can exist.&quot; [[Peter Kropotkin]]. [http://www.theanarchistlibrary.org/HTML/Petr_Kropotkin__Anarchism__its_philosophy_and_ideal.html Anarchism: its philosophy and ideal]&lt;/ref&gt;&lt;ref&gt;&quot;anarchists are opposed to irrational (e.g., illegitimate) authority, in other words, hierarchy — hierarchy being the institutionalisation of authority within a society.&quot; [http://www.theanarchistlibrary.org/HTML/The_Anarchist_FAQ_Editorial_Collective__An_Anarchist_FAQ__03_17_.html#toc2 &quot;B.1 Why are anarchists against authority and hierarchy?&quot;] in [[An Anarchist FAQ]]&lt;/ref&gt; Anarchism holds the [[state (polity)|state]] to be undesirable, unnecessary, or harmful.&lt;ref name=&quot;definition&quot;&gt;"""
    
    Wiki2Plain = Wiki2Plain(wiki)
    content = Wiki2Plain.text
    image = Wiki2Plain.image()
    
    print '---'
    print content
    print '---'
    print image
    print '---'