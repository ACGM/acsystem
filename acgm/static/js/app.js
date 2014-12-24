(function () {

  var app = angular.module('cooperativa', [
    'cooperativa.menu',
    'cooperativa.nomina',
    'cooperativa.facturacion'
    ]);

	app.config(function($interpolateProvider,$httpProvider){
  	  $interpolateProvider.startSymbol('[[').endSymbol(']]');

      $httpProvider.defaults.xsrfCookieName = 'csrftoken';
      $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

      // $resourceProvider.defaults.stripTrailingSlashes = false;
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