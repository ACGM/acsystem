(function () {

	angular.module('cooperativa.menu', ['ngAnimate'])
		.controller('MenuController', ['$scope', '$location', function($scope, $location) {

		    $scope.ShowSubMenuP = function(valor) {
		    	$scope.SubMPrestamo = valor;
		    }

		    $scope.ShowSubMenuInv = function(valor) {
		    	$scope.SubMInventario = valor;
		    }

		    $scope.ShowSubMenuFact = function(valor) {
		    	$scope.SubMFacturacion = valor;
		    }

		    $scope.ShowSubMenuNomina = function(valor) {
		    	$scope.SubMNomina = valor;
		    }

		    $scope.ShowSubMenuCxp = function(valor){
		    	$scope.SubCxp = valor;
		    }

		    $scope.ShowSubMenuCont = function(valor){
		    	$scope.SubCont = valor;
		    }

		}]);
})();
