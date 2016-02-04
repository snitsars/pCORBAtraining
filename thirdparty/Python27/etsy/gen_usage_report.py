import webbrowser
import storagesqlite
import json

storage = storagesqlite.Storage('etsy.db')

options = {
  'title' : 'Etsy two-hourly API usage',
  'vAxis': {'title': 'Calls'},
  'hAxis': {'title': 'Time'},
  'seriesType': 'line',
  'series': {
    0: {'type': 'bars'} 
  }
}

cd_template = "{data : google.visualization.arrayToDataTable(%s), options : %s}"

def get_data(hours):
  data = []
  for start in reversed(range(0, 48, 2)):
    result = storage.get_api_calls_count(start, hours)
    data.append([result[0], result[1], 10000*hours/24])
  return data


data = [['Time', 'Load per two hours', 'Average limit']]
data.extend(get_data(2))
cd =  [cd_template % (json.dumps(data), json.dumps(options))]

data = [['Time', 'Cumulative load', 'Daily limit']]
data.extend(get_data(24))
options['title'] = 'Cumulative API usage for last 24 hours'
options['series'] = None
cd.append(cd_template % (json.dumps(data), json.dumps(options)))

template = """
<html><head>
<script type="text/javascript" src="https://www.google.com/jsapi"></script>
<script type="text/javascript">
  google.load("visualization", "1", {packages:["corechart"]});
  google.setOnLoadCallback(function drawVisualization() {

    var chartsdata = [%s]

    for (i=0; i < chartsdata.length; ++i) {
      var chart = new google.visualization.ComboChart(document.getElementById('chart_div'+i));
      chart.draw(chartsdata[i].data, chartsdata[i].options);
    }
  })

</script>
</head>

  <body>
    <div id="chart_div0" style="width: 700px; height: 400px; float:right"></div>
    <div id="chart_div1" style="width: 700px; height: 400px;"></div>
  </body>
</html>
"""
s = template % ",".join(cd)


f = file('usage.htm', 'w')
f.write(s)
f.close()

webbrowser.open('usage.htm')