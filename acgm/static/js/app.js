(function () {

  var app = angular.module('cooperativa', [
    'cooperativa.menu',
    'cooperativa.nomina'
    ]);

	app.config(function($interpolateProvider,$httpProvider){
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

  app.controller('GNominaCtrl', function ($scope) {
    
    $scope.gNomina = "";

    $scope.GeneraNomina = function() {
      $scope.gNomina = !$scope.gNomina;

    };

  });

  app.directive('datepicker', function() {
    return {
        restrict: 'A',
        require : 'ngModel',
        link : function (scope, element, attrs, ngModelCtrl) {
            $(function(){
                element.datepicker({
                    dateFormat:'dd/mm/yy',
                    onSelect:function (date) {
                        scope.$apply(function () {
                            ngModelCtrl.$setViewValue(date);
                        });
                    }
                });
            });
        }
    }
  });

})();