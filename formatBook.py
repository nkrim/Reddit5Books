#def format(filename, output):
#	f=open(filename)
#	lines=f.readlines()
#	result=open(output,"w")
def formatplaintext(input):
	lines=input.split('\n')
	result=""
	i=0
	for line in lines:
		if (len(lines)<=1):
			line="<br> "
		result=result+"<div id=\"line"+str(i)+"\">"+line[:-1]+"</div>\n"
		i+=1
	return result

def formatcomments(comments):
	string=""
	i=0
	for comment in comments:
		string=string+"comments["+str(i)+"]=new Comment("+str(comment["start"])+","+str(comment["end"])+","+comment["subject"]+","+comment["details"]+");\n"
	return string