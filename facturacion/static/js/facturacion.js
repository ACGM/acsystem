(function () {

  angular.module('cooperativa.facturacion', [])

    .controller('ListadoFacturasCtrl', ['$scope', function ($scope) {
      $scope.showLF = true;

      // Mostrar/Ocultar panel de Listado de Facturas
      $scope.toggleLF = function() {
        $scope.showLF = !$scope.showLF;
      }

    }])

    .controller('DetalleFacturaCtrl', ['$scope', function ($scope) {
      $scope.fecha = Date.now();

    }]);

})();