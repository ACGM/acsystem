(function (_) {

  angular.module('cooperativa.Ahorro.controllers', [])
    .controller('AhorroController', ['$rootScope', '$scope', '$routeParams', 'AhorroService', function ($rootScope, $scope, $routeParams, AhorroService) {
      var type = $routeParams.type;
      var dataAhorro = [];

      $rootScope.title = "";

	  AhorroService.allAhorro.then(function (data) {
	    $scope.ahorro = ahorro = data;
	    console.log(data);
        });

    }]);

})(_);
