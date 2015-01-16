(function (_) {

  angular.module('cooperativa.nomina', ['ngAnimate'])
    
    .factory('NominaService', ['$http', '$q', '$filter', function ($http, $q, $filter) {

      // Retornar las nominas generadas
      function nominasGeneradas() {
        var deferred = $q.defer();

        $http.get('/api/nominasgeneradas/?format=json')
          .success(function (data) {
            deferred.resolve(data);
          });

          return deferred.promise;
      }

      return {
        nominasGeneradas: nominasGeneradas
      };

    }])

    //****************************************************
    //CONTROLLERS                                        *
    //****************************************************
    .controller('GeneraNominaCtrl', ['$scope', 'NominaService', function ($scope, NominaService) {
      $scope.showGN = true;

      // Mostrar/Ocultar panel de Generar Nomina
      $scope.toggleGN = function() {
        $scope.showGN = !$scope.showGN;
      }

      // Todas las nominas generadas
      $scope.getNominasGeneradas = function() {
        NominaService.nominasGeneradas().then(function (data) {
          $$scope.nominas = data;
        });
      }

    }])

    .controller('ConsultarNominaCtrl', ['$scope', function ($scope) {
      $scope.showCN = true;

      // Mostrar/Ocultar panel de Consultar Nomina
      $scope.toggleCN = function() {
        $scope.showCN = !$scope.showCN;
      }

    }])

    .controller('DetalleNominaCtrl', ['$scope', function ($scope) {
      

    }])

})(_);