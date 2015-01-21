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

      //Traer los distritos
      function distritos() {
        var deferred = $q.defer();

        $http.get('/api/distritos/?format=json')
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


      //Buscar un desembolso en especifico (Desglose)
      function DocumentoById(NoCheque) {
        var deferred = $q.defer();
        var doc = NoCheque != undefined? NoCheque : 0;

        $http.get('/desembolsojson/?nocheque={NoCheque}&format=json'.replace('{NoCheque}', doc))
          .success(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;
      }


      return {
        all: all,
        distritos: distritos,
        guardaDesembolso: guardaDesembolso,
        byNoCheque: byNoCheque,
        DocumentoById: DocumentoById
      };

    }])


    //****************************************************
    //CONTROLLERS                                        *
    //****************************************************
    .controller('DesembolsosCajasCtrl', ['$scope', '$filter', 'FondosCajasService', 
                                        function ($scope, $filter, FondosCajasService) {
      
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

    }]);

})(_);