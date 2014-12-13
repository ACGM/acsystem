(function () {

  var app = angular.module('Menu', [])

	.config(function($interpolateProvider,$httpProvider){
  	  $interpolateProvider.startSymbol('[[').endSymbol(']]');

      $httpProvider.defaults.xsrfCookieName = 'csrftoken';
      $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

      // $resourceProvider.defaults.stripTrailingSlashes = false;
	});

  app.controller('MenuController', function ($scope) {
    
    $scope.menu = "0";

    $scope.setMenu = function($op) {
      $scope.menu = $op;

      $('#menu' + $scope.menu + ' a').addClass('OpcionSeleccionada');
      $sib = $('#menu' + $scope.menu).siblings();
      $sib.find(' a').removeClass('OpcionSeleccionada')
    };

  });

})();