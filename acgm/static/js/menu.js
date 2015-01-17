(function () {

	angular.module('cooperativa.menu', ['ngAnimate'])
		.controller('MenuController', ['$scope', '$location', function($scope, $location) {
			$scope.menu = "0";


		    $scope.ShowSubMenuP = function() {
		    	$scope.SubMPrestamo = !$scope.SubMPrestamo;
		    }
		}]);
})();
