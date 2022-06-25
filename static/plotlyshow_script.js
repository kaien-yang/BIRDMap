function generate_graph(date_str, lon, lat, date_ind, title) {
    var tickvals = [15.5, 46.5, 77.5, 108.5, 139.5, 170.5, 201.5, 232.5, 263.5, 294.5, 325.5, 356.5];
    var ticktext = ["January", "February", "March", "April", "May", "June", "July",
                    "August", "September", "October", "November", "December"];

    var colors = [[0, 'rgb(18,7,135)'], [0.25, 'rgb(198,65,124)'], [0.5, 'rgb(239,247,33)'], [0.75, 'rgb(198,65,124)'], [1.0, 'rgb(18,7,135)']];
    var data = [{
        type: "scattergeo",
        mode: "markers",
        text: date_str,
        lon: lon,
        lat: lat,
        hovertemplate: '(%{lat:.2f}\u00B0, %{lon:.2f}\u00B0) <br> %{text}<extra></extra>',
        marker: {
            color: date_ind,
            colorscale: colors,
            cmin: 0,
            cmax: 365,
            size: 5,
            colorbar:{
                tickmode: "array",
                thickness: 10,
                titleside: 'right',
                outlinecolor: 'rgba(68,68,68,0)',
                ticks: 'outside',
                ticklen: 3,
                tickvals: tickvals,
                ticktext: ticktext
            }
        }
    }];

    var layout = {
        geo: {
            scope: 'world',
            showland: true,
            landcolor: 'rgb(212,212,212)',
            showlakes: true,
            lakecolor: 'rgb(255,255,255)',
            resolution: 50,
            projection_type: "natural earth"
        },
        longaxis: {
            showgrid: true,
            gridwidth: 0.5,
            range: [ -180, 180 ],
            dtick: 5
        },
        lataxis: {
            showgrid: true,
            gridwidth: 0.5,
            range: [ 20.0, 60.0 ],
            dtick: 5
        },
        title: title,
        autosize: true
    };

    var config = {responsive: true};

    return [data, layout, config];
}