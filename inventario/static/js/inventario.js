(function () {

  angular.module('cooperativa.inventario', [])
    

    .controller('ListadoEntradaInvCtrl', ['$scope','$http', '$q', function ($scope, $http, $q) {
      $scope.showLEI = true;
      $scope.entradas = {};

      // Mostrar/Ocultar panel de Listado de Entrada Inventario
      $scope.toggleLEI = function() {
        $scope.showLEI = !$scope.showLEI;
      }

      $scope.seleccion = function() {
        for(i = 1; i < $scope.entradas.length; i++){
          $scope.entradas[i].posteo = 'N';
          console.log($scope.entradas[i]);
        }
      }


      $http.get('/api/inventario/?format=json').
        success( function(data) {
          $scope.entradas = data;
        })

    }])

    .controller('EntradaInvCtrl', ['$scope', function ($scope) {
      $scope.showEI = true;

      // Mostrar/Ocultar panel de Entrada de Inventario
      $scope.toggleEI = function() {
        $scope.showEI = !$scope.showEI;
      }

    }]);

})();