# image_to_text

An application to turn an image into an editable document.  

<h3>Overview</h3>
<br/>
<p style="font-size:14px">The aim of this project is to develop an application that can take an image of Ancient Greek (sometimes mixed with English) text and convert it into a text file that can be edited. The project itself solves 3 problems, and combines them together to create the final application:</p>
<ul style="font-size:14px">
	<li>Problem One: How can you take an image and split it into its distinct characters?</li>
	<li>Problem Two: Having split the image into its characters, how can you then identify each character?</li>
	<li>Problem Three: Once you have a prediction for each character, how can you then order them correctly in a text document such that you accurately reflect the original text?</li>
</ul>
<p style="font-size:14px">I will go through these problems in order, showing how I split an image into its component parts (individual characters or character clustsers). I will then talk a bit about how I generated my dataset and trained the image classifier. Finally I will discuss the approach I took at recreating the order of the characters in the text.</p>
<br/>

<h3>Problem One: How can you get the characters out of an image of text?</h3>
<p style="font-size:14px">The first problem I faced was how to get the individual character images out of a page like the one below<br/><img src="greek_pages/page_images/GK_RDR_PG3_2.jpeg" width="500" height="250" /><br/>
To solve this I figured that the best I could do was get all of the connected components within the image using the <a href="https://algs4.cs.princeton.edu/15uf/">Union Find algorithm</a> (implemented in <code>lib/graph/support.py</code>) where a connected component is defined as any contiguous set of black pixels.

In this case my definition would mean that to qualify as a character, there must be a set of black pixels, that are connected to each other by some continous path of other black pixels. This feels like a reasonable definition, and in fact it does an excellent job of getting individual characters. The two areas where it doesn't quite work are for characters that have faded ink and are split into multiple parts, such as the Eta in this image:<br/>
<img src="imgs/letter_parts.png" width="70" height="50" /> <br/> and for characters that are connected to each other by the typeface, and thus create a cluster of two or more characters: <br/>
<img src="imgs/multi_letters.png" width="70" height="50" /><br/>

All in all however, the methodology seemed to work great, and I decided to allow the existence of letter parts and letter clusters, and classify them as such. To see how I handle each in the final application, please see the <a href="https://github.com/nickybangs/image_to_text/blob/master/nbs/image_splitting.ipynb">image splitting notebook</a> and the image mergine notebook (coming soon). 

After I split the image into its connected components (code defined in <code>get_components</code> in <code>lib/graph/image_graph.py</code>, I take note of the four corners of each component and store them in a <code>.yaml</code> file to be used in the labeling process (see labeling section below as well as notebook called <a href="https://github.com/nickybangs/image_to_text/blob/master/nbs/greek_tagging_tool.ipynb">greek tagging tool notebook</a>).

Problem one solved, now on to problem two.</p>

<h3>Problem Two: Predicting a character from an image</h3>
<p style="font-size:14px">This section shouldn't contain any surprises. In order to predict what character a given image represents I used a CNN classifier. In particular I used the <a href="https://docs.fast.ai/vision.html">fastai library</a> to train my model, see the notebook (coming soon).</p>
<p style="font-size:14px">To train my model I had to first generate an initial data set. I did this by taking a picture of a page of greek text and splitting it into its component characters. I used a widget that I created (see <a href="https://github.com/nickybangs/image_to_text/blob/master/nbs/greek_tagging_tool.ipynb">greek tagging tool notebook</a>) to quickly label all of the characters either as the chacter name, a letter part, or a multi-letter. 
Once the first data set was gathered, I trained a preliminary model to help automatically tag future characters. This model is used in <code>lib/preprocess.py</code> which takes an image, breaks it into components, predicts each image, automatically labels anything with a probability of greater than .85, and stores all unlabeled components in a new <code>.yaml</code> file. All automatically labeled components are reviewed and anything that was incorrect is corrected. All unlabeled components are then labeled using the widget in the <code>greek_tagging_tool</code> notebook.</p>

<h3>Problem Three: How do you preserve the order of the characters in the image.</h3>
<p style="font-size:14px">For each character component, I store the four corner pixel locations in the image. To preserve the order of the characters, I have found the easiest method is to first split the lines, and then order the components accroding to their left bounds. This also helps determine the spaces between words, any left and right boundaries that are next to each other (within some threshold of pixels) are placed next to each other in the text, and any that have a distance greater than the threshold are separated by a space. 
This enables me to only worry about placing characters in the right order within one line, and not have to worry about what line they fall into based on the corner locations. For special characters such as accents and diacritics, I used the left and right boundaries to determine where to place them, for example an accute accent will be placed over the letter within whose boundaries it falls, provided that it is above that letter. This condition is to ensure that the special character doesn't belong to the line below, which will sometimes occur using the line splitting technique I have adopted (see next secion)</p><br/>

<h3>Splitting Lines In an Image</h3>
<p style="font-size:14px">To split an image into its lines, I employ the following technique. First I find the most likely row numbers for the line splits (see <a href="https://github.com/nickybangs/image_to_text/blob/master/nbs/find_line_splits.ipynb">find line splits notebook</a> for details).

Each subgraph that I identify as a likely linesplit will contain the pixels for the bottom of the line above the line split as well as the top of the line below the line split. Between these two lines will be the white space reprepresenting the line split. 

In most cases you can't just create a straight line at this split to separate the lines because some characters might extend above the line split, the image of the page might have a curve in it such that the straight line found will cut off letter parts or include letter parts from neighboring lines. To combat this I use <a href="https://algs4.cs.princeton.edu/44sp/">Dijkstra's shortest path algorithm</a> which will find a path of only white space between the lines. 

This solves the problem of cutting off or including incorrect letter parts because the shortest path will always go around any letter in the way to find the white space. The only issue is that sometimes accents are included in the line above, but this is generally solved by identifying the relative position of an accent to the letter is associated with. For example if an accute accent is below some letter, it will clearly belong to the line below, in the same column. For more info on this process see <a href="https://github.com/nickybangs/image_to_text/blob/master/nbs/get_lines.ipynb">get_line_splits</a></p>
