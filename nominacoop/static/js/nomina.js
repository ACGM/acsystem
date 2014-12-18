(function () {

  angular.module('cooperativa.nomina', [])
    


    .controller('GeneraNominaCtrl', ['$scope', function ($scope) {
      $scope.showGN = true;

      // Mostrar/Ocultar panel de Generar Nomina
      $scope.toggleGN = function() {
        $scope.showGN = !$scope.showGN;
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

})();