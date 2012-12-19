#!/usr/bin/python

import os

bloglist = open('/web/crypto.is/templates/bloglist.txt', 'r')
lines = bloglist.readlines()
posts = []
for p in lines:
    f = open('/web/crypto.is/templates/blog/' + p.strip() + '.html', 'r')
    posts.append((p.strip(), f.readlines()))
                 
    
rss = open('tmp-news.xml', 'w')
rss.write("""<?xml version="1.0\"?>
<rss version=\"2.0\">
<channel>
<title>crypto.is</title>
<link>https://crypto.is</link>
<description></description>\n\n""")
                 
def indexOfCon(item, array):
    return array.index([i for i in array if item in i][0])

for p in posts:
    rss.write("\t<item>\n")

    rss.write("\t\t<guid>https://crypto.is/blog/")
    rss.write(p[0])
    rss.write("</guid>\n")
    
    lines = p[1]
    title = [i for i in lines if '<h1>' in i][0].replace('</', '').replace('<', '').replace('h1>', '').strip()

    rss.write("\t\t<title>")
    rss.write(title)
    rss.write("</title>\n")
    
    pubdate = [i for i in lines if 'blogdate' in i][0].replace('<div class="blogdate">', '').replace('</div>', '').strip()
    rss.write("\t\t<pubDate>")
    rss.write(pubdate)
    rss.write("</pubDate>\n")

    contentlines = lines[indexOfCon('blogdate', lines) + 1 : indexOfCon('{% end', lines)]
    rss.write("\t\t<description><![CDATA[\n")
    rss.write("".join(contentlines))
    rss.write("\n\t\t]]></description>\n")
    
    rss.write("\t</item>\n\n")
    

rss.write("</channel>")
rss.write("</rss>")
