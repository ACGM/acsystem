(function () {

  angular.module('cooperativa.nomina', [])
    .controller('GeneraNominaCtrl', ['$scope','$window', function ($scope, $window) {

      $scope.mostrarGN = function() {
        if($window.sessionStorage.getItem('GN') == 'true'){
          $window.sessionStorage.setItem('GN', 'false');
          $scope.mostrar = 'false';
        }
        else {
          $window.sessionStorage.setItem('GN', 'true');
          $scope.mostrar = 'true';
        }
        return $scope.mostrar;
      }
    }]);
})();