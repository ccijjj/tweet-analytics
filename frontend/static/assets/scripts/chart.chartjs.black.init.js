/**
 * Theme: Ninja Admin Template
 * Author: NinjaTeam
 * Module/App: Chartist-Chart
 */

(function($) {
	"use strict";

	var ChartJs = {},
		randomScalingFactor = function() {
			return Math.round(Math.random() * 15) + 5;
		};

	$(document).ready(function(){
		if ($('#bar-chartjs-chart').length) ChartJs.bar('bar-chartjs-chart','top','bar');
		if ($('#bar-chartjs-chart1').length) ChartJs.bar1('bar-chartjs-chart1','top','bar');
		if ($('#horizontal-bar-chartjs-chart').length) ChartJs.bar('horizontal-bar-chartjs-chart','right','horizontalBar');
		if ($('#line-chartjs-chart').length) ChartJs.line('line-chartjs-chart',false);
		if ($('#line-chartjs-chart2').length) ChartJs.line2('line-chartjs-chart2',false);
		if ($('#line-chartjs-chart3').length) ChartJs.line3('line-chartjs-chart3',false);
		if ($('#pie-chartjs-chart').length) ChartJs.pie('pie-chartjs-chart','pie');
		if ($('#donut-chartjs-chart').length) ChartJs.pie2('donut-chartjs-chart','pie');
		if ($('#polar-chartjs-chart').length) ChartJs.polar('polar-chartjs-chart');
		if ($('#radar-chartjs-chart').length) ChartJs.radar('radar-chartjs-chart');
		return false;
	});

	ChartJs = {
		bar: function(container,position,type){
			var barChartData = {
					labels: ["2013-2015", "2014-2016", "2015-2017", "2016-2018",'2017-2019'],
					datasets: [{
						label: 'Male',
						backgroundColor: "rgba(249,200,81,0.3)",
						borderColor: "rgb(249, 200, 81)",
						borderWidth: 1,
						hoverBackgroundColor: "rgba(249,200,81,0.6)",
						hoverBorderColor: "rgb(249, 200, 81)",
						data: [81.9,82,82.3,82.9,82.5]
					}, {
						label: 'Female',
						backgroundColor: "rgba(127, 193, 252, 0.3)",
						borderColor: "#7fc1fc",
						borderWidth: 1,
						hoverBackgroundColor: "rgba(127, 193, 252, 0.6)",
						hoverBorderColor: "#7fc1fc",
						data: [85.4,85.5,85.7,86.1,86.1]
					}]
				};

			var ctx = document.getElementById(container).getContext("2d"),
				skip = (type == "bar") ? "bottom" : "left" ;
			new Chart(ctx, {
				type: type,
				data: barChartData,
				options: {
					// Elements options apply to all of the options unless overridden in a dataset
					// In this case, we are setting the border of each bar to be 2px wide and green
					
					hover: {
						mode: 'label'
					},
					responsive: true,
					legend: {
						position: position,
					},
					scales: {
						xAxes: [{
							ticks: {
								beginAtZero:true
							},
							gridLines: {
								color: 'rgba(255,255,255,0.2)',
								zeroLineColor: 'rgba(255,255,255,0.4)',
							}
						}],
						yAxes: [{
							ticks: {
								beginAtZero:true
							},
							gridLines: {
								color: 'rgba(255,255,255,0.2)',
								zeroLineColor: 'rgba(255,255,255,0.4)',
							}
						}],
					},

				}
			});
			return false;
		},
		bar1: function(container,position,type){
			var barChartData = {
					labels: ["2014", "2015", "2016", "2017"],
					datasets: [{
						label: 'Sensitivity Score',
						backgroundColor: "rgba(245,112,122,0.3)",
						borderColor: "#f5707a",
						borderWidth: 1,
						hoverBackgroundColor: "rgba(245,112,122,0.6)",
						hoverBorderColor: "#f5707a",
						data: [0.085792,-0.083812,0.037613,-0.113497]
					}]
				};

			var ctx = document.getElementById(container).getContext("2d"),
				skip = (type == "bar") ? "bottom" : "left" ;
			new Chart(ctx, {
				type: type,
				data: barChartData,
				options: {
					// Elements options apply to all of the options unless overridden in a dataset
					// In this case, we are setting the border of each bar to be 2px wide and green

					hover: {
						mode: 'label'
					},
					responsive: true,
					legend: {
						position: position,
					},
					scales: {
						xAxes: [{
							ticks: {
								beginAtZero:true
							},
							gridLines: {
								color: 'rgba(255,255,255,0.2)',
								zeroLineColor: 'rgba(255,255,255,0.4)',
							}
						}],
						yAxes: [{
							ticks: {
								beginAtZero:true
							},
							gridLines: {
								color: 'rgba(255,255,255,0.2)',
								zeroLineColor: 'rgba(255,255,255,0.4)',
							}
						}],
					},

				}
			});
			return false;
		},
		line: function(container,fill){
			var lineData = {
					labels: ['Melbourne Inner', 'Melbourne Inner East', 'Melbourne North East ', 'Melbourne Inner South' ,'Melbourne North West',
								'Melbourne Outer East','Melbourne South East' ,'Melbourne West' ,'Mornington Peninsula'],
					datasets: [{
						label: 'Income Mean',
						fill: fill,
						borderColor: "rgba(245,112,122,1)",
						pointBackgroundColor: "rgb(245,112,122)",
						backgroundColor: "rgba(245,112,122,0.3)",
						data: [76349.0,76902.0 ,77958.0 ,56915.0,53652.0 ,55815.0, 51562.0 ,53989.0 ,54752.0]
					},
					{
						label: 'RAI‰',
						fill: fill,
						borderColor: "rgb(112,130,245)",
						pointBackgroundColor: "rgb(112,145,245)",
						backgroundColor: "rgb(59,68,82)",
						data: [72770,95310 ,88040 ,126480 ,133020 ,124370 ,130370, 133840, 137130]
					}]
				};

			var ctx = document.getElementById(container).getContext("2d");
			new Chart(ctx, {
				type: 'line',
				data: lineData,
				options: {
					hover: {
						mode: 'label'
					},
					responsive: true,
					scales: {
						xAxes: [{
							ticks: {
								beginAtZero:true
							},
							gridLines: {
								color: 'rgba(255,255,255,0.2)',
								zeroLineColor: 'rgba(255,255,255,0.4)',
							}
						}],
						yAxes: [{
							ticks: {
								beginAtZero:true
							},
							gridLines: {
								color: 'rgba(255,255,255,0.2)',
								zeroLineColor: 'rgba(255,255,255,0.4)',
							}
						}]
					}
				}
			});
			return false;
		},
		line2: function(container,fill){
			var lineData = {
					labels: ['Melbourne Inner', 'Melbourne Inner East', 'Melbourne North East ', 'Melbourne Inner South' ,'Melbourne North West',
								'Melbourne Outer East','Melbourne South East' ,'Melbourne West' ,'Mornington Peninsula'],
					datasets: [{
						label: 'Total Unemployment',
						fill: fill,
						borderColor: "rgba(245,112,122,1)",
						pointBackgroundColor: "rgb(245,112,122)",
						backgroundColor: "rgba(245,112,122,0.3)",
						data: [22109,10568,12250,14321 ,10810 ,13101 ,28532, 34351, 12305]
					},
					{
						label: 'Total Earners',
						fill: fill,
						borderColor: "rgb(113,231,13)",
						pointBackgroundColor: "rgb(13,210,16)",
						backgroundColor: "rgb(109,134,110)",
						data: [361473 ,218151, 245053 ,265940 ,181742 ,293395, 390957 ,369904, 160516]

					}]
				};

			var ctx = document.getElementById(container).getContext("2d");
			new Chart(ctx, {
				type: 'line',
				data: lineData,
				options: {
					hover: {
						mode: 'label'
					},
					responsive: true,
					scales: {
						xAxes: [{
							ticks: {
								beginAtZero:true
							},
							gridLines: {
								color: 'rgba(255,255,255,0.2)',
								zeroLineColor: 'rgba(255,255,255,0.4)',
							}
						}],
						yAxes: [{
							ticks: {
								beginAtZero:true
							},
							gridLines: {
								color: 'rgba(255,255,255,0.2)',
								zeroLineColor: 'rgba(255,255,255,0.4)',
							}
						}]
					}
				}
			});
			return false;
		},
		line3: function(container,fill){
			var lineData = {
					labels: ['2014', '2015', '2016', '2017 '],
					datasets: [{
						label: 'Job Searching Weeks',
						fill: fill,
						borderColor: "rgb(35,234,229)",
						pointBackgroundColor: "rgb(13,238,204)",
						backgroundColor: "rgb(46,135,100)",
						data: [ 36.75 ,33.53 ,30.17 ,34.0]
					},
					]
				};

			var ctx = document.getElementById(container).getContext("2d");
			new Chart(ctx, {
				type: 'line',
				data: lineData,
				options: {
					hover: {
						mode: 'label'
					},
					responsive: true,
					scales: {
						xAxes: [{
							ticks: {
								beginAtZero:true
							},
							gridLines: {
								color: 'rgba(255,255,255,0.2)',
								zeroLineColor: 'rgba(255,255,255,0.4)',
							}
						}],
						yAxes: [{
							ticks: {
								beginAtZero:true
							},
							gridLines: {
								color: 'rgba(255,255,255,0.2)',
								zeroLineColor: 'rgba(255,255,255,0.4)',
							}
						}]
					}
				}
			});
			return false;
		},
		pie : function(container,type){
			var ctx = document.getElementById(container).getContext("2d"),
				config = {
					type: type,
					data: {
						datasets: [{
							data: [
								2781197,
								541275,
								107384,
								101849,
								101393,
								76581,
								49449,
								33664,
								30310,
								22402,
								17596,
								138117
							],
							backgroundColor: [
								"#f9c851",
								"#3ac9d6",
								"#ebeff2",
								"#f95151",
								"#1c2d6c",
								"#ce0cce",
								"#0ef635",
								"#132424",
								"#4e4b2b",
								"#99fccd",
								"#024449",
								"#f3afe2"
							],
							hoverBackgroundColor: [
								"#f9c851",
								"#3ac9d6",
								"#ebeff2",
								"#f95151",
								"#1c2d6c",
								"#ce0cce",
								"#0ef635",
								"#132424",
								"#4e4b2b",
								"#99fccd",
								"#024449",
								"#f3afe2"
							],
							hoverBorderColor: "#fff"
						}],
						labels: [
							'English',
							"Chinese",
							"Greek",
							'Italian',
							"Vietnamese",
							"Arabic",
							'Hindi',
							"Spanish",
							"Turkish",
							"Urdu",
							'French',
							"Others"
						]
					},
					options: {
						responsive: true
					}
				};
			new Chart(ctx, config);
			return false;
		},
		pie2: function(container,type){
			var ctx = document.getElementById(container).getContext("2d"),
				config = {
					type: type,
					data: {
						datasets: [{
							data: [
								2133643,
								135251,
								41858,
								37659,
								23288,
								22816,
								13869,
								11358,
								7693,
								72314
							],
							backgroundColor: [
								"#f9c851",
								"#3ac9d6",
								"#ebeff2",
								"#f95151",
								"#1c2d6c",
								"#ce0cce",
								"#0ef635",
								"#132424",
								"#4e4b2b",
								"#99fccd"

							],
							hoverBackgroundColor: [
								"#f9c851",
								"#3ac9d6",
								"#ebeff2",
								"#f95151",
								"#1c2d6c",
								"#ce0cce",
								"#0ef635",
								"#132424",
								"#4e4b2b",
								"#99fccd"


							],
							hoverBorderColor: "#fff"
						}],
						labels: [
							'English',
							"Unknown",
							"Indonesian",
							'Spanish',
							"Arabic",
							'Japanese',
							"Turkish",
							'French',
							"Portuguese",
							"Others"
						]
					},
					options: {
						responsive: true
					}
				};
			new Chart(ctx, config);
			return false;
		},
		polar: function(container){
			var ctx = document.getElementById(container).getContext("2d"),
				config = {
					data: {
						datasets: [{
							data: [
								randomScalingFactor(),
								randomScalingFactor(),
								randomScalingFactor(),
								randomScalingFactor(),
							],
							backgroundColor: [
								"#f5707a",
								"#188ae2",
								"#4bd396",
								"#8d6e63",
							],
							label: 'My dataset' // for legend
						}],
						labels: [
							"Red",
							"Blue",
							"Green",
							"Grey",
						]
					},
					options: {
						responsive: true,
						legend: {
							position: 'top',
						},
						scale: {
							ticks: {
								beginAtZero: true
							},
							gridLines: {
								color: 'rgba(255,255,255,0.2)',
								zeroLineColor: 'rgba(255,255,255,0.4)',
							}
						},
						animation: {
							animateRotate: false,
							animateScale: true
						}
					}
				};
			new Chart.PolarArea(ctx, config);
			return false;
		},
		radar: function(container){
			var ctx = document.getElementById(container).getContext("2d"),
				config = {
					type: 'radar',
					data: {
						labels: ["Eating", "Drinking", "Sleeping", "Designing", "Coding", "Cycling", "Running"],
						datasets: [{
							label: "Peter",
							backgroundColor: "rgba(179,181,198,0.2)",
							borderColor: "rgba(179,181,198,1)",
							pointBackgroundColor: "rgba(179,181,198,1)",
							pointBorderColor: "#fff",
							pointHoverBackgroundColor: "#fff",
							pointHoverBorderColor: "rgba(179,181,198,1)",
							data: [randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor()]
						}, {
							label: "John",
							 backgroundColor: "rgba(255,99,132,0.2)",
							borderColor: "rgba(255,99,132,1)",
							pointBackgroundColor: "rgba(255,99,132,1)",
							pointBorderColor: "#fff",
							pointHoverBackgroundColor: "#fff",
							pointHoverBorderColor: "rgba(255,99,132,1)",
							data: [randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor()]
						},]
					},
					options: {
						legend: {
							position: 'top',
						},
						scale: {
							reverse: false,
							gridLines: {
								color: ['black', 'red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']
							},
							ticks: {
								beginAtZero: true
							}
						}
					}
				};
			new Chart(ctx, config);
			return false;
		}
	}
	
})(jQuery);