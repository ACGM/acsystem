(function () {

  var app = angular.module('cooperativa', [
    'cooperativa.menu',
    'cooperativa.nomina',
    'cooperativa.facturacion',
    'cooperativa.inventario',
    'cooperativa.inventarioRPT',
    'cooperativa.fondoscajas',
    'cooperativa.ahorro',
    'cooperativa.solicitudprestamo',
    'cooperativa.maestraprestamo',
    'cooperativa.solicitudod'
    ]);

	app.config(function($interpolateProvider,$httpProvider){
  	  $interpolateProvider.startSymbol('[[').endSymbol(']]');

      $httpProvider.defaults.xsrfCookieName = 'csrftoken';
      $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

      // $resourceProvider.defaults.stripTrailingSlashes = false;
	});

  
  //Filtro para rellenar con ceros a la izquierda
  app.filter('numberFixedLen', function () {
    return function (n, len) {
      var num = parseInt(n, 10);
      len = parseInt(len, 10);
      if (isNaN(num) || isNaN(len)) {
        return n;
      }
      num = ''+num;
      while (num.length < len) {
        num = '0'+num;
      }
      return num;
    };
  });

  app.filter('posteo', function() {
      return function (input) {
        if (!input) return "";

        input = input
                .replace('N', false)
                .replace('S', true);
        return input;
      }
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

  app.directive('mensajeerror', function () {
    return {
      restrict: 'E',
      templateUrl: '/mensajeError'
    }
  });

  app.directive('mensajeinfo', function () {
    return {
      restrict: 'E',
      templateUrl: '/mensajeInfo'
    }
  });

  app.directive('productossearch', function () {
    return {
      restrict: 'E',
      templateUrl: '/productosSearch'
    }
  });

  app.directive('selectOnClick', function () {
    return {
        restrict: 'A',
        link: function (scope, element, attrs) {
            element.on('click', function () {
                this.select();
            });
        }
    };
  });

  app.directive('format', ['$filter', function ($filter) {
    return {
        require: '?ngModel',
        link: function (scope, elem, attrs, ctrl) {
            if (!ctrl) return;


            ctrl.$formatters.unshift(function (a) {
                return $filter(attrs.format)(ctrl.$modelValue)
            });

            ctrl.$parsers.unshift(function (viewValue) {
                var plainNumber = viewValue.replace(/[^\d|\-+|\.+]/g, '');
                elem.val($filter(attrs.format)(plainNumber));
                return plainNumber;
            });
        }
    };
  }]);

})();