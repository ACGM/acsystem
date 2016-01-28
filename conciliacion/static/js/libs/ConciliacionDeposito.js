(function(_){
	angular.module('cooperativa.concDeposito', ['ngAnimate'])

	.factory('concDepositoServices', ['$http','$q','$filter', function ($http, $q, $filter) {
		var depositoApi='/conciliacion/depositos';

		function getDeposito(){
			var deferred = $q.defer();

			$http.get(depositoApi+'?format=json')
				.success(function (data){
					deferred.resolve(data);
				})

				.error(function (error){
					deferred.resolve(error);
				});

			 return deferred.promise;
			};

		function setDeposito(deposito){
				var deferred = $q.defer();
			
				$http.post(depositoApi, JSON.stringify({'deposito':deposito}))
	                .success(function (data){
	                    deferred.resolve(data);
	                })
	                .error(function (err){
	                    deferred.resolve(err);
	                });
	            return deferred.promise;
				};

		function getDepositoFecha(fechaI, fechaF){
			var deferred = $q.defer();

			$http.get(depositoApi+'?fechaI={fechaI}&fechaF={fechaF}'.replace('{fechaI}',fechaI).replace('{fechaF}',fechaF))
				.success(function (data){
					deferred.resolve(data);
				})
				.error(function (error){
					deferred.resolve(error);
				});

			return deferred.promise;
		};

		return {
			getDeposito : getDeposito,
			setDeposito : setDeposito,
			getDepositoFecha : getDepositoFecha
		};
	}]);

	.controller('DepositosCtrl', ['$scope','$filter', '$rootScope', 'concDepositoServices','$timeout',  
		function ($scope, $filter, $rootScope, concDepositoServices, $timeout) {
		
		$scope.depositosLs = [];
		$scope.regDeposito = {};
		$scope.fechai = null;
		$scope.fechaf = null;
		$scope.NwDeposito = false;
		$scope.LsDepts = true;

		$scope.getBancoList = function(){
			$scope.regBanco = {};
			concDepositoServices.getDeposito().then(function (data){
				$scope.LsDepts = data;
			});
		};

		$rootScope.mostrarError = function(error) {
			      $scope.errorMsg = error;
			      $scope.errorShow = true;
			      $timeout(function(){$scope.errorShow = false;}, 3000);   
		
		};
	}]);
	
})();