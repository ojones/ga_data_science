
PLAY = {}

$(document).ready(function(){

	PLAY = appStart()

})


function appStart(){

	app = {
		methods: { }
		, currentSection: undefined
		, tweets: undefined
		, processed: undefined
		, featureVectors: undefined
		, metrics: undefined
		, classifications: undefined
	}

	var message = "hello world"
		, currentSection = 0
		, methods = {}
		, $sections = $('.section')
		, $keywords = $('#keywords')
		, tweets = []
		, processed = []
		, featureVectors = []
		, metrics = {}
		, classifications = []
		, choices = {}

	var more = app.methods.more = function(){

		var $next = undefined
		if (currentSection < $sections.length-1){
			$next = $sections.eq(currentSection+1)
        	currentSection = currentSection+1
		} else {
			$next = $sections.eq(0)
			currentSection = 0
		}

		$('html, body').animate({
            scrollTop: $next.offset().top
        }, 200)

        app.currentSection = currentSection
	}

	var query = app.methods.query = function(queryTerm){
		
		var $data = $('#dataQuery')

        $.getJSON('/_query', {
	          keywords: queryTerm
	        }
	        , function(data) {

	        	app.tweets = tweets = data.tweets

	        	for (var i in data.tweets) {
	        		;(function(x){
	        			$item = $('<div>'+data.tweets[x]+'</div>')
	        			$data.append($item)
	        		}(i))
				}
        })

        return false
	}

	var process = app.methods.process = function($options){

		var $data = $('#dataProcess').html('')
			, options = [ ]

		$options.each(function(k,v){
			var $this = $(this)

			if ($this.is(':checked')){
				options.push($this.val())
			}
		})

		choices['process'] = options

        $.getJSON('/_process', {
        		tweets: JSON.stringify(tweets)
        		, options: JSON.stringify(options)
        	}
	        , function(data) {
	        	
	        	app.processed = processed = data.processed

	        	for (var i in data.processed) {
	        		;(function(x){
	        			$item = $('<div>'+data.processed[x]+'</div>')
	        			$data.append($item)
	        		}(i))
	        	}
        })

        return false
	}

	var features = app.methods.features = function($options){

		var $data = $('#dataFeatures').html('')
			, options = [ ]

		$options.each(function(k,v){
			var $this = $(this)

			if ($this.is(':checked')){
				options.push($this.val())
			}
		})

		choices['features'] = options

        $.getJSON('/_features', {
        		processed: JSON.stringify(processed)
        		, options: JSON.stringify(options)
        	}
	        , function(data) {
	        	
	        	app.featureVectors = featureVectors = data.features

	        	for (var i in data.features) {
	        		;(function(x){
	        			$item = $('<div>'+JSON.stringify(data.features[x])+'</div>')
	        			$data.append($item)
	        		}(i))
	        	}
        });

        return false
	}

	var learn = app.methods.learn = function($options){

		var $data = $('#dataLearn').html('')
			, options = [ ]
			, accuracy = 0
			, feature = ''
		$options.each(function(k,v){
			var $this = $(this)

			if ($this.is(':checked')){
				options.push($this.val())
			}
		})
		
		if (choices['features'] && choices['features'].length > 0){
			feature =	choices['features'][0]
		} 

		metrics = get_metrics(feature, options[0])

		// Retrieve the object from storage
		var retrievedObject = localStorage.getItem('metrics');
		if (retrievedObject) {
			jsonObj = JSON.parse(retrievedObject)
			jsonObj.push(metrics)
			localStorage.setItem('metrics', JSON.stringify(jsonObj));
		} else {
			metricsArray = []
			metricsArray.push(metrics)
        	// Put the object into storage
			localStorage.setItem('metrics', JSON.stringify(metricsArray))
		}
		var html = ""
		html += '<div class="confusionMatrix">'
		html += '<div class="chartTitle">Confusion Matrix</div>'
		html += '<div class="labelY">actual value</div>'
		html += '<div class="labelX">prediction outcome</div>'
		html += '<div class="counts">'
		html += '<div class="count truePos">'+ metrics.confusionMatrix[0][0] +'</div>'
		html += '<div class="count trueNeg">'+ metrics.confusionMatrix[0][1] +'</div><br/>'
		html += '<div class="count falsePos">'+ metrics.confusionMatrix[1][0] +'</div>'
		html += '<div class="count falseNeg">'+ metrics.confusionMatrix[1][1] +'</div>'
		html += '</div>'
		html += '</div>'
	    $data.append($(html))

	    //$data.append($('<div> accuracy: ' + accuracy + '</div>'))

        return false
	}

	var test = app.methods.test = function(){

		var $data = $('#dataTest')

        $.getJSON('/_test', {
        		tweets: JSON.stringify(app.tweets)
        	}
	        , function(data) {
	          
	          	app.classifcations = classifications = data.classifications

	        	for (var i in data.classifications) {
	        		;(function(x){
	        			var classification = ""
	        			if (data.classifications[x] == 1){
	        				classification = "positive"
	        			}
	        			//if (data.classifications[x] == 2){
	        			//	classification = "neutral"
	        			//}
	        			if (data.classifications[x] == 0){
	        				classification = "negative"
	        			}
	        			$item = $('<div class="'+classification+'"><b>'+classification+':</b> '+tweets[x]+'</div>')
	        			$data.append($item)
	        		}(i))
	        	}
        });

        return false
	}

	var report = app.methods.report = function(){

		var $data = $('#dataReport')

		// Retrieve the object from storage
		var retrievedObject = localStorage.getItem('metrics');

    	if (retrievedObject){
    		var data = []
			jsonObj = JSON.parse(retrievedObject)
    		for (var x in jsonObj){
    			var dataPoint = []
    			//dataPoint.push(80)//jsonObj[x].pos_fmeasure*100)
    			//dataPoint.push(80)//jsonObj[x].neg_fmeasure*100)
    			dataPoint.push(jsonObj[x].accuracy*100)
    			data.push(dataPoint)
    		}
    		app.plotData = data
			makePlot(data, '#barChart')
    	}

        return false
	}

	var clear = app.methods.clear = function(){
		localStorage.clear()
	}

	function get_metrics(feature, classifier) {
		
		var data = get_metric_data()
			, metrics = {
				accuracy: 0
				, confusionMatrix: []
			}

		switch(feature) {
			case 'bigrams':
				switch(classifier){
					case 'nb':
						metrics.accuracy = data.nb.bigrams.accuracy
						metrics.confusionMatrix = data.nb.bigrams.confusionMatrix
						break
					case 'svm':
						metrics.accuracy = data.svm.bigrams.accuracy
						metrics.confusionMatrix = data.svm.bigrams.confusionMatrix
						break
					case 'nn':
						metrics.accuracy = data.nn.bigrams.accuracy
						metrics.confusionMatrix = data.nn.bigrams.confusionMatrix
						break
					default: //'lr'
						metrics.accuracy = data.lr.bigrams.accuracy
						metrics.confusionMatrix = data.lr.bigrams.confusionMatrix
				}
				break
			default: // 'uingrams'
				switch(classifier){
					case 'nb':
						metrics.accuracy = data.nb.unigrams.accuracy
						metrics.confusionMatrix = data.nb.bigrams.confusionMatrix
						break
					case 'svm':
						metrics.accuracy = data.svm.unigrams.accuracy
						metrics.confusionMatrix = data.svm.bigrams.confusionMatrix
						break
					case 'nn':
						metrics.accuracy = data.nn.unigrams.accuracy
						metrics.confusionMatrix = data.nn.bigrams.confusionMatrix
						break
					default: //'lr'
						metrics.accuracy = data.lr.unigrams.accuracy
						metrics.confusionMatrix = data.lr.bigrams.confusionMatrix
				}
		}

		return metrics
	}

	function get_metric_data(){
	
		var metrics = {}

		metrics.nb = {
			unigrams: {
				accuracy: 0.77146422312629837
				, confusionMatrix: [[237094,  52320],[ 79914, 209286]]
			}
			, bigrams: {
				accuracy: 0.78759760392938993
				, confusionMatrix: [[243051,  46347],[ 76552, 212664]]
			}
		}

		metrics.svm = {
			unigrams: {
				accuracy: 0.73226883552765742
				, confusionMatrix: [[201341,  87292],[ 67621, 222360]]
			}
			, bigrams: {
				accuracy: 0.67059386741420013
				, confusionMatrix: [[254961,  33672],[156927, 133054]]

			}
		}

		metrics.lr = {
			unigrams: {
				accuracy: 0.80181606390443372
				, confusionMatrix: [[229074,  59559],[ 55113, 234868]]
			}
			, bigrams: {
				accuracy: 0.79202369800938099
				, confusionMatrix: [[223220,  65413],[ 54925, 235056]]
			}
		}

		metrics.nn = {
			unigrams: {
				accuracy: 0.72820913424148048
				, confusionMatrix: [[209430,  79144],[ 78118, 211922]]
			}
			, bigrams:{
				accuracy: 0.75271078819385639
				, confusionMatrix: [[216796,  71837],[ 71248, 218733]]
			}
		}

		return metrics

	}

	function events(){
		$('.btn.next').click(function(){
			more()
		})
		$('#btnQuery').click(function(e){
			query($keywords.val())
		})
		$('#btnProcess').click(function(e){
			process($('input[name="processOpt"]'))
		})
		$('#btnFeatures').click(function(e){
			features($('input[name="featureOpt"]'))
		})
		$('#btnLearn').click(function(e){
			learn($('input[name="learnOpt"]'))
		})
		$('#btnTest').click(function(e){
			test()
		})
		$('#btnReport').click(function(e){
			report()
		})
		$('#btnClear').click(function(e){
			clear()
		})
	}

	events()
	
	return app
	
}