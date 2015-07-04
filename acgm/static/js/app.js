(function () {

  var app = angular.module('cooperativa', [
    'cooperativa.menu',
    'cooperativa.homepage',
    'cooperativa.nomina',
    'cooperativa.facturacion',
    'cooperativa.inventario',
    'cooperativa.inventarioRPT',
    'cooperativa.fondoscajas',
    'cooperativa.notadebito',
    'cooperativa.notacredito',
    'cooperativa.ahorro',
    'cooperativa.solicitudprestamo',
    'cooperativa.maestraprestamo',
    'cooperativa.solicitudod',
    'cooperativa.cxp',
    'cooperativa.desembolsoelectronico',
    'cooperativa.contabilidad'
    ]);

  app.factory('appService', ['$http', '$q', '$filter', function ($http, $q, $filter) {

    function generarArchivoBanco(header, detalle) {
      var deferred = $q.defer();

      $http.post('/generarArchivoBanco/', JSON.stringify({'CABECERA': header, 'DETALLE': detalle})).
        success(function (data) {
          deferred.resolve(data);
        }).
        error(function (data) {
          deferred.resolve(data)
        });
      return deferred.promise;
    }

    //Traer Cuentas Contables
    function allCuentasContables() {
      var deferred = $q.defer();

      $http.get('/api/cuentas/?format=json')
        .success(function (data) {
          deferred.resolve(data);
        });
      return deferred.promise;
    }

    //Traer Documentos Relacionados a Cuentas
    function getDocumentoCuentas(doc) {
      var deferred = $q.defer();

      $http.get('/api/documentoCuentas/{doc}/?format=json'.replace('{doc}', doc))
        .success(function (data) {
          deferred.resolve(data);
        });
      return deferred.promise;
    }

    return {
      generarArchivoBanco: generarArchivoBanco,
      allCuentasContables: allCuentasContables,
      getDocumentoCuentas: getDocumentoCuentas
    };

  }]);

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

  // Para color de icono de posteo ---> N = Mamey ----> S = Verde
  // y para bloquear o desbloquear checkbox de entrada de inventario
  app.filter('posteo', function() {
      return function (input) {
        if (!input) return "";

        input = input
                .replace('N', false)
                .replace('S', true);
        return input;
      }
  });

  // Para Posteos S / N  --> N = No posteado ---> S = Si posteado (Folder abierto/cerrado)
  app.filter('posteoFolderIcon', function() {
    return function (input) {
      if (!input) return "";

      input = input
              .replace('N', 'icon-folder-open')
              .replace('S', 'icon-folder')
      return input;
    }
  });

  // Filtro para llevar de numeros a letras.
  app.filter('NumLetra', function() {
      return function (input) {
        if (!input) return "";

        return NumeroALetras(input);
      }
  });

  // Filtro para retornar la fecha actual
  app.filter('currentdate',['$filter',  function($filter) {
    return function() {
        return $filter('date')(new Date(), 'dd/MM/yyyy');
    };
  }]);

  // Directiva para obtener el calendario cuando hay un focus en un campo de ese tipo
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

  // Directiva para los mensajes de error (estandarizacion)
  app.directive('mensajeerror', function () {
    return {
      restrict: 'E',
      templateUrl: '/mensajeError'
    }
  });

  // Directiva para los mensajes de posteo a contabilidad (estandarizacion)
  app.directive('mensajeinfo', function () {
    return {
      restrict: 'E',
      templateUrl: '/mensajeInfo'
    }
  });

  // Directiva para tabla de cuentas.
  app.directive('cuentassearch', function () {
    return {
      restrict: 'E',
      templateUrl: '/cuentasSearch'
    }
  });

  // Directiva para tabla de productos en caso de presentar el costo y no el precio.
  app.directive('productossearch', function () {
    return {
      restrict: 'E',
      templateUrl: '/productosSearch'
    }
  });

  // Directiva para tabla de prestamos.
  app.directive('prestamossearch', function () {
    return {
      restrict: 'E',
      templateUrl: '/prestamosSearch'
    }
  });

  // Directiva para tabla de Pago de Cuotas.
  app.directive('pagocuotassearch', function () {
    return {
      restrict: 'E',
      templateUrl: '/pagoCuotasSearch'
    }
  });

  // Directiva para cuando se haya focus en un campo se seleccione todo el texto automaticamente.
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

  app.directive('aDisabled', function() {
    return {
        compile: function(tElement, tAttrs, transclude) {
            //Disable ngClick
            tAttrs["ngClick"] = "!("+tAttrs["aDisabled"]+") && ("+tAttrs["ngClick"]+")";

            //return a link function
            return function (scope, iElement, iAttrs) {

                //Toggle "disabled" to class when aDisabled becomes true
                scope.$watch(iAttrs["aDisabled"], function(newValue) {
                    if (newValue !== undefined) {
                        iElement.toggleClass("disabled", newValue);
                    }
                });

                //Disable href on click
                iElement.on("click", function(e) {
                    if (scope.$eval(iAttrs["aDisabled"])) {
                        e.preventDefault();
                    }
                });
            };
        }
    };
  });

  // Directiva para darle formato numerico con separadores de miles mientras se escribe en un campo.
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