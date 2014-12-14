(function () {

	angular.module('cooperativa.menu', [])
		.controller('MenuController', ['$scope', function($scope) {
			$scope.menu = "0";

		    $scope.setMenu = function($op) {
		      $scope.menu = $op;

		      $('#menu' + $scope.menu + ' a').addClass('OpcionSeleccionada');
		      $sib = $('#menu' + $scope.menu).siblings();
		      $sib.find(' a').removeClass('OpcionSeleccionada')
		    }
		}]);
})();
