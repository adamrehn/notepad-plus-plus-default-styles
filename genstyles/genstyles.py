#!/usr/bin/env python

#  "genstyles" Notepad++ to Atom Syntax Style Converter
#  Copyright (c) 2014, Adam Rehn
# 
#  Script to convert Notepad++ style XML files to LESS stylesheets for Atom.
#
#  Requires the following files in the current directory:
#
#    styleMappings.json - contains required conversion information
#    stylers.xml        - Notepad++ syntax styles XML file
# 
#  ---
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.

from __future__ import print_function
import xml.dom.minidom
import json

# Wraps an object in a list if is not a list already
def forceList(x):
	
	if x == None:
		return None
	elif isinstance(x, list):
		return x
	else:
		return [x]


# Writes the contents of a file
def putFileContents(filename, data):
	
	f = open(filename, "wb")
	f.write(data.encode("utf-8"))
	f.close()


# Parses a JSON file
def parseJSONFile(filename):
	
	f = open(filename, "r")
	decoded = json.load(f)
	f.close()
	return decoded


# Generates CSS from a WordsStyle XML element
def convertStyle(styleNode):
	
	fgColour = styleNode.getAttribute("fgColor")
	isBold   = (styleNode.getAttribute("fontStyle") == "1")
	
	css  = "\t\tcolor: #" + fgColour + ";\n"
	css += "\t\tfont-weight: " + ("bold" if isBold else "normal") + ";\n"
	
	return css


# Parse the style mappings JSON file
styleMappings = parseJSONFile("styleMappings.json")

# Parse the stylers.xml file with minidom
document = xml.dom.minidom.parse("stylers.xml")

# We will build the LESS stylesheet iteratively
styles = ""

# Iterate over the languages
for langNode in document.getElementsByTagName("LexerType"):
	
	# Determine if we have conversion details for the current language 
	langName = langNode.getAttribute("name")
	if (langName in styleMappings):
		
		# Open the selector block for the current language
		styles += "." + styleMappings[langName]["class"] + " {\n"
		
		# Iterate over the styles for the current language
		for styleNode in langNode.childNodes:
			if (styleNode.nodeType != styleNode.TEXT_NODE and styleNode.tagName == "WordsStyle"):
				
				# Determine if we have a conversion mapping for the current style
				styleName = styleNode.getAttribute("name")
				if (styleName in styleMappings[langName]["styles"]):
					mappings = forceList(styleMappings[langName]["styles"][styleName])
					if mappings != None:
						styles += "\t" + ",\n\t".join(mappings) + " {\n" + convertStyle(styleNode) + "\t}\n"
		
		# Close the selector block for the current language
		styles += "}\n"

# Write the generated stylesheet to the file language-styles.less
putFileContents("../stylesheets/language-styles.less", styles)