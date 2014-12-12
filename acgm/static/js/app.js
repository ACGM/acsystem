(function () {

  var app = angular.module('Menu', [])

	.config(function($interpolateProvider,$httpProvider){
  	  $interpolateProvider.startSymbol('[[').endSymbol(']]');

      $httpProvider.defaults.xsrfCookieName = 'csrftoken';
      $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

      // $resourceProvider.defaults.stripTrailingSlashes = false;
	});

  app.controller('MenuController', function ($scope) {
    
    // $scope.saluda = "HOLA"

    $scope.setMenu = function($op) {
      $('#menu' + $op + ' a').addClass('OpcionSeleccionada');
      $sib = $('#menu' + $op).siblings();
      $sib.find(' a').removeClass('OpcionSeleccionada')
    };

  });

})();