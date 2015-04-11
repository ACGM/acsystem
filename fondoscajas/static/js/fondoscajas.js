(function (_) {

  angular.module('cooperativa.fondoscajas', ['ngAnimate'])

    .factory('FondosCajasService', ['$http', '$q', '$filter', function ($http, $q, $filter) {

      //Guardar Desembolso Caja
      function guardaDesembolso(dataH, dataD) {
        var deferred = $q.defer();

        $http.post('/desembolso/', JSON.stringify({'cabecera': dataH, 'detalle': dataD})).
          success(function (data) {
            deferred.resolve(data);
          }).
          error(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;
      }

      //Llenar el listado de Desembolsos
      function all() {
        var deferred = $q.defer();

        $http.get('/api/desembolsos/?format=json')
          .success(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;
      }

      //Buscar un numero de cheque en especifico en listado de documentos
      function byNoCheque(NoCheque) {
        var deferred = $q.defer();
        all().then(function (data) {
          var result = data.filter(function (registro) {
            return registro.cheque == NoCheque;
          });

          if(result.length > 0) {
            deferred.resolve(result);
          } else {
            deferred.reject();
          }
        });
        return deferred.promise;
      }


      //Buscar un desembolso en especifico (Desglose) By Cheque
      function DocumentoByCheque(NoCheque) {
        var deferred = $q.defer();
        var doc = NoCheque != undefined? NoCheque : 0;

        $http.get('/desembolsojson/?nocheque={NoCheque}&format=json'.replace('{NoCheque}', doc))
          .success(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;
      }

      //Buscar un desembolso en especifico (Desglose) By ID
      function DocumentoById(Id) {
        var deferred = $q.defer();
        var doc = Id != undefined? Id : 0;

        $http.get('/desembolsojson/?id={id}'.replace('{id}', doc))
          .success(function (data) {
            deferred.resolve(data);
          });
        return deferred.promise;
      }

      //Impresion de Desembolso (incrementa el campo de IMPRESO)
      function impresionDesembolso(desembolso) {
        var deferred = $q.defer();

        $http.post('/desembolso/print/{desembolso}/'.replace('{desembolso}', desembolso), {'desembolso': desembolso}).
          success(function (data) {
            deferred.resolve(data);
          }).
          error(function (data) {
            deferred.resolve(data);
          });
        return deferred.promise;
      }


      return {
        all: all,
        guardaDesembolso: guardaDesembolso,
        byNoCheque: byNoCheque,
        DocumentoByCheque: DocumentoByCheque,
        DocumentoById: DocumentoById,
        impresionDesembolso: impresionDesembolso
      };

    }])


    //****************************************************
    //CONTROLLERS                                        *
    //****************************************************
    .controller('DesembolsosCajasCtrl', ['$scope', '$filter', '$window', 'FondosCajasService', 
                                        function ($scope, $filter, $window, FondosCajasService) {
      
      //Inicializacion de variables
      $scope.showLD = true;
      $scope.regAll = false;

      $scope.item = {};
      $scope.desembolsos = {};

      $scope.desembolsosSeleccionadas = [];
      $scope.reg = [];
      $scope.valoresChk = [];
      $scope.dataD = [];

      $scope.fecha = $filter('date')(Date.now(),'dd/MM/yyyy');
      $scope.ArrowLD = 'UpArrow';

      
      // Mostrar/Ocultar panel de Listado de Desembolsos
      $scope.toggleLD = function() {
        $scope.showLD = !$scope.showLD;

        if($scope.showLD === true) {
          $scope.ArrowLD = 'UpArrow';
        } else {
          $scope.ArrowLD = 'DownArrow';
        }
      }

      //Listado de todos los desembolsos
      $scope.listadoDesembolsos = function() {
        $scope.desembolsosSeleccionadas = [];
        $scope.valoresChk = [];

        FondosCajasService.all().then(function (data) {
          $scope.desembolsos = data;
          $scope.regAll = false;

          if(data.length > 0) {
            $scope.verTodos = 'ver-todos-ei';

            var i = 0;
            data.forEach(function (data) {
              $scope.valoresChk[i] = false;
              i++;
            });

          }
        });
      }

      //Buscar un cheque en especifico
      $scope.filtrarPorNoCheque = function(NoCheque) {
        try {
          FondosCajasService.byNoCheque(NoCheque).then(function (data) {
            $scope.desembolsos = data;

            if(data.length > 0) {
              $scope.verTodos = '';
              $scope.NoFoundDoc = '';
            }
          }, 
            (function () {
              $scope.NoFoundDoc = 'No se encontró el cheque #' + NoCheque;
            }
          ));          
        } catch (e) {
          console.log(e);
        }
      }

      //Buscar Cheque por ENTER
      $scope.buscarCheque = function($event, NoCheque) {
        if($event.keyCode == 13) {
          $scope.filtrarPorNoCheque(NoCheque);
        }
      }

      //Imprimir Desembolso
      $scope.printD = function(desembolso) {
        $window.sessionStorage['desembolso'] = JSON.stringify(desembolso);
        $window.open('/desembolso/print/{desembolso}'.replace('{desembolso}',desembolso.id), target='_blank'); 
      }

    }])


    //****************************************************
    //CONTROLLERS    IMPRESION                           *
    //****************************************************
    .controller('ImprimirDesembolsoCtrl', ['$scope', '$filter', '$window', 'FondosCajasService', 
                                        function ($scope, $filter, $window, FondosCajasService) {
      
      //Inicializacion de variables
      $scope.showLD = true;
      $scope.regAll = false;

      $scope.fecha = $filter('date')(Date.now(),'dd/MM/yyyy');

      $scope.desembolso = JSON.parse($window.sessionStorage['desembolso']);

      //Buscar un documento en especifico con detalle.
      $scope.getDocumentoById = function(Id) {
        try {
          FondosCajasService.DocumentoById(Id).then(function (data) {
            $scope.desembolsoDetalle = data[0];
            $scope.desglose = data[0]['detalle'];

            $scope.totalvalor();
          });

        } catch (e) {
          console.log(e);
        }
      }

      $scope.imprimirDesembolso = function() {

        FondosCajasService.impresionDesembolso($scope.desembolso.id).then(function (data) {
          console.log("DATA: " + data);

          document.getElementById('printBoton').style.display = "None";
          window.print();
          window.location.reload();
          document.getElementById('printBoton').style.display = "";
        });
      }

      $scope.totalvalor = function() {
        $scope.totalValor_ = 0;
        
        $scope.desglose.forEach(function (item) {
          $scope.totalValor_ += parseFloat(item.monto);
        });
      }


    }]);

})(_);