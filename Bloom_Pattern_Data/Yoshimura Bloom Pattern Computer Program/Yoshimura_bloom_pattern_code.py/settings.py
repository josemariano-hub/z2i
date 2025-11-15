'''
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
USER GUIDE:

Please enter your preferences within bracketed quotation marks, ["_______"], below.
Please DO NOT change anything except for numbers in bracketed quotation marks. They represent your preferences for computing and graphing the Yoshimura bloom pattern.

m - the number of sides of the central polygon. Enter an integer greater than or equal to 4.

h - the height order of the pattern. Enter an integer greater than or equal to 0.

s - the scale of the pattern. By default, the length of a side of the central polygon is 1. Enter a decimal greater than 0.

Show Origin - enter 1 to show the origin of the graph or 0 otherwise.

Show Points - enter 1 to show points (vertices) or 0 otherwise. There will be points that belong to different wedges but occupy the same coordinates. 

Show facets - enter 1 to to show facets or 0 otherwise. The central polygon is yellow and wedge facets are lime.

Show Lines - enter 1 to show lines or 0 otherwise. Lines include both creases and edges.

Line Width - enter a decimal factor of 1. Default width is 1. 

Line Style - enter 1 for colored lines or 0 for monochromatic lines. Blue or solid lines represent mountain folds, red or dashed lines represent valley folds, and black or thick lines represent edges. The default line style is monochromatic.

Invert Creases - enter 1 for yes or 0 for no. They produce opposite mountain/valley assignment of creases. The default setting is 0. 
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
'''
import Bloom_Yoshimura
def main():



    ''' ENTER YOUR PREFERENCES HERE: '''

    m = ["     6     "] # example values: 5, 6, 8, 12 #

    h = ["     2     "] # example values: 1, 2, 3 #

    s = ["     1     "] # example values: 1, 4, 50, 27.5, 1001 #

    Show_Origin = ["     1     "] # enter 1 to show origin or 0 to hide origin.

    Show_Points = ["     1     "] # enter 1 to show points or 0 to hide points.

    Show_facets = ["     1     "] # enter 1 to show facets or 0 to hide facets.

    Show_Lines = ["     1     "] # enter 1 to show lines or 0 to hide lines.

    Line_Width = ["     1     "]  # example values: 0.7, 2.5, 0.625, 5 #

    Line_Style = ["     1     "]  # enter 1 for colored lines and 0 for black lines.

    Invert_Creases = ["      0      "]  # enter 1 to invert creases or 0 for no change.

    ''' END OF PREFERENCES '''


























    m = int(m[0])
    h = int(h[0])
    s = float(s[0])
    Show_Origin = bool(int(Show_Origin[0]))
    Show_Points = bool(int(Show_Points[0]))
    Show_facets = bool(int(Show_facets[0]))
    Show_Lines = bool(int(Show_Lines[0]))
    Line_Width = float(Line_Width[0])
    Line_Style = bool(int(Line_Style[0]))
    Invert_Creases = bool(int(Invert_Creases[0]))

    bloom = Bloom_Yoshimura.Bloom_Yoshimura(m,h,s) # M,H,S
    bloom.plot_origin = Show_Origin
    bloom.plot_points = Show_Points
    bloom.plot_facets = Show_facets
    bloom.plot_lines = Show_Lines
    bloom.line_width = Line_Width
    bloom.line_style = Line_Style
    bloom.crease_is_invert = Invert_Creases
    

    bloom.graph()

'''program written by Kelvin Wang'''
