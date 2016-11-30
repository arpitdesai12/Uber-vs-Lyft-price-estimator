angular.module('starter', ['ionic'])
    .run(function($ionicPlatform) {
        $ionicPlatform.ready(function() {
            if (window.cordova && window.cordova.plugins.Keyboard) {
                cordova.plugins.Keyboard.hideKeyboardAccessoryBar(true);
                cordova.plugins.Keyboard.disableScroll(true);
            }
            if (window.StatusBar) {
                StatusBar.styleDefault();
            }
        });
    })
    .controller('MapCtrl', ['$scope', function($scope) {
    	$scope.nof = 0;
    	
        $scope.inputFields = [{
        	id: 'field1',
        	show: true
        },
        {
        	id: 'field2',
        	show: false
        },
        {
        	id: 'field3',
        	show: false
        },
        {
        	id: 'field4',
        	show: false
        },
        {
        	id: 'field5',
        	show: false
        },
        {
        	id: 'field6',
        	show: false
        },
        {
        	id: 'field7',
        	show: false
        }];
        $scope.addField = function() {
    		var i = $scope.nof;
    		$scope.inputFields[i].show = true;
    		$scope.nof++;
    		$scope.$apply();
    	}
        //$scope.addField();
		function initialize() {
		// Create the autocomplete object, restricting the search
		// to geographical location types.
		 for (i=0;i<$scope.inputFields.length; i++){

		      autocomplete = new google.maps.places.Autocomplete((document.getElementById($scope.inputFields[i].id)),
		  { types: ['geocode'] })
		  }

		// When the user selects an address from the dropdown,
		// populate the address fields in the form.
		google.maps.event.addListener(autocomplete, 'place_changed', function() {
			$scope.apply();
		});

		}
        // Run the initialize function when the window has finished loading.
        google.maps.event.addDomListener(window, 'load', initialize);
    }])