'''
Code by Armin Okic - Viral Virtual
Heatmaps, dots and lines with Flask and GMaps API
'''


from flask import Flask, make_response, render_template, request, send_from_directory
import pandas
import os

app = Flask(__name__)
#printing the root folder
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
print(APP_ROOT)

#Objects Points and Lines
class Points:
    def __init__(self, point_id, label,lat, long, heatmaps_value=None,value_info=None):
        """
        Object to hold set of points
        :param point_id: The id of the point forwarded to the map
        :param label: The label of the point forwarded to the map
        :param lat: latitude of the point
        :param long: longitude of the point
        :param heatmap_value: Details about the point forwarded to the map
        :param value_info: Details about the point forwarded to the map
        """
        self.point_id = point_id
        self.label = label
        self.lat = lat
        self.long = long
        self.heatmap_value = heatmap_value
        self.value_info = value_info

class Lines:
    def __init__(self, x1, y1, x2, y2, value):
        """
        Object to hold lines
        :param x1: longitude of first dot
        :param y1: latitude of first dot
        :param x2: longitude of second dot
        :param y2: longitude of second dot
        :param value: some value for the line, e.g. tickness, opacity etc.
        """
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.value = value


# Example data
center_y = 43.84864
center_x = 18.35644
df_lines = pandas.DataFrame(data={'x1': [center_x, center_x, center_x, center_x],
                                  'y1': [center_y, center_y, center_y, center_y],
                                  'x2': [center_x, center_x-0.02,center_x+0.02,center_x],
                                  'y2': [center_y+0.02, center_y+0.02,center_y-0.02,center_y-0.02],
                                  'value':[1,2,4,6]})
df_points = pandas.DataFrame(data={'point_id': [1,2,3,4,5,6,7,8],
                                   'label': [1,2,3,4,1,2,3,4],
                                   'lat': [center_y,center_y-0.02,center_y+0.02,center_y,center_y,center_y-0.01,center_y+0.01,center_y],
                                   'long': [center_x,center_x-0.02,center_x,center_x+0.02,center_x,center_x-0.01,center_x,center_x+0.01],
                                   'heatmap_value': [35,20,25,30,15,20,27,30],
                                   'value_info': [22,33,22,11,11,22,33,22]
                                   })
points = list()
lines = list()


# making list of points object
for i in range(0, df_points.shape[0]):
    label = df_points.iloc[i]["label"]
    point_id = df_points.iloc[i]["point_id"]
    long = df_points.iloc[i]["long"]
    lat = df_points.iloc[i]["lat"]
    heatmap_value = df_points.iloc[i]["heatmap_value"]
    value_info = df_points.iloc[i]["value_info"]
    points.append(Points(point_id,label,lat,long,heatmap_value,value_info))

# making list of lines object
for i in range(0, df_lines.shape[0]):
    x1 = df_lines.iloc[i]["x1"]
    y1 = df_lines.iloc[i]["y1"]
    x2 = df_lines.iloc[i]["x2"]
    y2 = df_lines.iloc[i]["y2"]
    value = df_lines.iloc[i]["value"]
    lines.append(Lines(x1,y1,x2,y2,value))

@app.route('/')
def index():
    #the forwarded value points= is the variable that will be forwarded to the html file
    return render_template("index.html", points=points, lines=lines) #points and lines are forwarded

if __name__ == '__main__':
    app.run(debug=True)
